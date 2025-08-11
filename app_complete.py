#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Complete Flask app with full functionality matching local version exactly
@origin 250724-01 (Plants1.3)
"""

import os
import logging
import uuid
import time
import threading
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_from_directory
from flask_socketio import SocketIO, emit, join_room, leave_room
from werkzeug.utils import secure_filename
from werkzeug.middleware.proxy_fix import ProxyFix

# Import custom modules
from models.token_manager import WebTokenManager
from models.facebook_api import WebFacebookAPI
from models.spam_manager import SpamManager
from utils.helpers import generate_session_id, allowed_file, get_image_path, delete_image_file

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-2024-production')
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads', 'images')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# For production deployment
app.wsgi_app = ProxyFix(app.wsgi_app)

# Initialize SocketIO
socketio = SocketIO(
    app, 
    cors_allowed_origins="*",
    logger=True,
    engineio_logger=True,
    async_mode='threading'
)

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Global managers - thread-safe
token_manager = WebTokenManager()
spam_managers = {}  # session_id -> SpamManager
active_sessions = set()

# Thread safety
managers_lock = threading.Lock()

def get_spam_manager(session_id: str) -> SpamManager:
    """Get or create spam manager for session"""
    with managers_lock:
        if session_id not in spam_managers:
            spam_managers[session_id] = SpamManager(
                session_id=session_id,
                token_manager=token_manager,
                socketio=socketio
            )
        return spam_managers[session_id]

@app.before_request
def before_request():
    """Initialize session if not exists"""
    if 'session_id' not in session:
        session['session_id'] = generate_session_id()
        logger.info(f"Created new session: {session['session_id']}")

# ==================== ROUTES ====================

@app.route('/')
def index():
    """Main dashboard"""
    return render_template('index.html')

@app.route('/api/tokens', methods=['GET'])
def get_tokens():
    """Get all tokens for current session"""
    try:
        session_id = session['session_id']
        tokens = token_manager.get_tokens(session_id)
        
        # Add comment count to each token
        for token in tokens:
            token['comments_sent'] = token_manager.get_comment_count(session_id, token['id'])
        
        return jsonify({'success': True, 'tokens': tokens})
    except Exception as e:
        logger.error(f"Error getting tokens: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/tokens', methods=['POST'])
def add_tokens():
    """Add new tokens"""
    try:
        data = request.get_json()
        tokens_text = data.get('tokens', '')
        
        if not tokens_text.strip():
            return jsonify({'success': False, 'message': 'Vui lòng nhập token'}), 400
        
        session_id = session['session_id']
        tokens = [token.strip() for token in tokens_text.split('\n') if token.strip()]
        
        added_count = token_manager.add_tokens(session_id, tokens)
        
        return jsonify({
            'success': True, 
            'message': f'Đã thêm {added_count} tokens thành công!'
        })
    except Exception as e:
        logger.error(f"Error adding tokens: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/tokens/check', methods=['POST'])
def check_tokens():
    """Check selected tokens status"""
    try:
        data = request.get_json()
        token_ids = data.get('token_ids', [])
        
        if not token_ids:
            return jsonify({'success': False, 'message': 'Vui lòng chọn tokens để kiểm tra'}), 400
        
        session_id = session['session_id']
        
        # Start checking in background
        def check_tokens_background():
            try:
                results = token_manager.check_tokens_status(session_id, token_ids, socketio)
                socketio.emit('tokens_checked', {
                    'success': True,
                    'results': results
                }, room=session_id)
            except Exception as e:
                logger.error(f"Error in background token check: {e}")
                socketio.emit('tokens_checked', {
                    'success': False,
                    'message': str(e)
                }, room=session_id)
        
        threading.Thread(target=check_tokens_background, daemon=True).start()
        
        return jsonify({
            'success': True, 
            'message': f'Đang kiểm tra {len(token_ids)} tokens...'
        })
    except Exception as e:
        logger.error(f"Error starting token check: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/tokens/<token_id>', methods=['DELETE'])
def delete_token(token_id):
    """Delete a specific token"""
    try:
        session_id = session['session_id']
        deleted_count = token_manager.delete_tokens(session_id, [token_id])
        
        if deleted_count > 0:
            return jsonify({'success': True, 'message': 'Token đã được xóa'})
        else:
            return jsonify({'success': False, 'message': 'Token không tồn tại'}), 404
    except Exception as e:
        logger.error(f"Error deleting token: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/tokens/delete-selected', methods=['POST'])
def delete_selected_tokens():
    """Delete selected tokens"""
    try:
        data = request.get_json()
        token_ids = data.get('token_ids', [])
        
        if not token_ids:
            return jsonify({'success': False, 'message': 'Vui lòng chọn tokens để xóa'}), 400
        
        session_id = session['session_id']
        deleted_count = token_manager.delete_tokens(session_id, token_ids)
        
        return jsonify({
            'success': True, 
            'message': f'Đã xóa {deleted_count} tokens'
        })
    except Exception as e:
        logger.error(f"Error deleting selected tokens: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/tokens/delete-all', methods=['POST'])
def delete_all_tokens():
    """Delete all tokens"""
    try:
        session_id = session['session_id']
        deleted_count = token_manager.delete_all_tokens(session_id)
        
        return jsonify({
            'success': True, 
            'message': f'Đã xóa tất cả {deleted_count} tokens'
        })
    except Exception as e:
        logger.error(f"Error deleting all tokens: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/tokens/delete-die', methods=['POST'])
def delete_die_tokens():
    """Delete tokens with DIE status"""
    try:
        session_id = session['session_id']
        deleted_count = token_manager.delete_die_tokens(session_id)
        
        return jsonify({
            'success': True, 
            'message': f'Đã xóa {deleted_count} tokens DIE'
        })
    except Exception as e:
        logger.error(f"Error deleting DIE tokens: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/tokens/delete-duplicates', methods=['POST'])
def delete_duplicate_tokens():
    """Delete duplicate tokens"""
    try:
        session_id = session['session_id']
        deleted_count = token_manager.delete_duplicate_tokens(session_id)
        
        return jsonify({
            'success': True, 
            'message': f'Đã xóa {deleted_count} tokens trùng lặp'
        })
    except Exception as e:
        logger.error(f"Error deleting duplicate tokens: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/spam/start', methods=['POST'])
def start_spam():
    """Start spam process"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['post_uids', 'comment_texts']
        for field in required_fields:
            if field not in data or not data[field].strip():
                return jsonify({'success': False, 'message': f'Vui lòng nhập {field}'}), 400
        
        session_id = session['session_id']
        
        # Check if we have available tokens
        if not token_manager.has_available_tokens(session_id):
            return jsonify({
                'success': False, 
                'message': 'Không có tokens LIVE khả dụng. Vui lòng thêm và kiểm tra tokens trước.'
            }), 400
        
        # Get spam manager
        spam_manager = get_spam_manager(session_id)
        
        # Check if already running
        if spam_manager.is_running():
            return jsonify({
                'success': False, 
                'message': 'Spam đang chạy. Vui lòng dừng trước khi bắt đầu lại.'
            }), 400
        
        # Parse data
        post_uids = [uid.strip() for uid in data['post_uids'].split('\n') if uid.strip()]
        comment_texts = [text.strip() for text in data['comment_texts'].split('\n') if text.strip()]
        
        settings = {
            'min_delay': data.get('min_delay', 5000),
            'max_delay': data.get('max_delay', 15000),
            'max_threads': data.get('max_threads', 10),
            'auto_like': data.get('auto_like', True)
        }
        
        # Start spam in background
        def start_spam_background():
            try:
                spam_manager.start_spam(post_uids, comment_texts, settings)
            except Exception as e:
                logger.error(f"Error in background spam: {e}")
                socketio.emit('spam_error', {
                    'message': str(e)
                }, room=session_id)
        
        threading.Thread(target=start_spam_background, daemon=True).start()
        
        return jsonify({
            'success': True, 
            'message': f'Đã bắt đầu spam {len(comment_texts)} comments cho {len(post_uids)} posts'
        })
    except Exception as e:
        logger.error(f"Error starting spam: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/spam/stop', methods=['POST'])
def stop_spam():
    """Stop spam process"""
    try:
        session_id = session['session_id']
        spam_manager = get_spam_manager(session_id)
        
        if spam_manager.is_running():
            spam_manager.stop_spam()
            return jsonify({'success': True, 'message': 'Đã dừng spam'})
        else:
            return jsonify({'success': False, 'message': 'Spam không đang chạy'})
    except Exception as e:
        logger.error(f"Error stopping spam: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Upload image file"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'message': 'Không có file được chọn'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'message': 'Không có file được chọn'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Add timestamp to avoid conflicts
            timestamp = str(int(time.time()))
            filename = f"{timestamp}_{filename}"
            
            session_id = session['session_id']
            upload_dir = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
            os.makedirs(upload_dir, exist_ok=True)
            
            filepath = os.path.join(upload_dir, filename)
            file.save(filepath)
            
            return jsonify({
                'success': True,
                'filename': filename,
                'url': f'/uploads/images/{session_id}/{filename}'
            })
        else:
            return jsonify({'success': False, 'message': 'File không hợp lệ. Chỉ chấp nhận: jpg, jpeg, png, gif'}), 400
    
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/images', methods=['GET'])
def get_images():
    """Get uploaded images for current session"""
    try:
        session_id = session['session_id']
        upload_dir = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
        
        images = []
        if os.path.exists(upload_dir):
            for filename in os.listdir(upload_dir):
                if allowed_file(filename):
                    images.append({
                        'filename': filename,
                        'url': f'/uploads/images/{session_id}/{filename}'
                    })
        
        return jsonify({'success': True, 'images': images})
    except Exception as e:
        logger.error(f"Error getting images: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/images/<filename>', methods=['DELETE'])
def delete_image(filename):
    """Delete an uploaded image"""
    try:
        session_id = session['session_id']
        filepath = get_image_path(session_id, filename, app.config['UPLOAD_FOLDER'])
        
        if delete_image_file(filepath):
            return jsonify({'success': True, 'message': 'Đã xóa ảnh'})
        else:
            return jsonify({'success': False, 'message': 'Không thể xóa ảnh'}), 404
    except Exception as e:
        logger.error(f"Error deleting image: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get session statistics"""
    try:
        session_id = session['session_id']
        stats = token_manager.get_session_stats(session_id)
        
        # Add spam status
        spam_manager = get_spam_manager(session_id)
        stats['spam_running'] = spam_manager.is_running()
        
        return jsonify({'success': True, 'stats': stats})
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

# Serve uploaded files
@app.route('/uploads/images/<session_id>/<filename>')
def uploaded_file(session_id, filename):
    """Serve uploaded images"""
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], session_id), filename)

# ==================== WEBSOCKET EVENTS ====================

@socketio.on('connect')
def handle_connect(auth):
    """Handle client connection"""
    session_id = session.get('session_id')
    if session_id:
        join_room(session_id)
        active_sessions.add(session_id)
        emit('connection_status', {'status': 'connected'})
        logger.info(f"Client connected to session: {session_id}")

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    session_id = session.get('session_id')
    if session_id:
        leave_room(session_id)
        active_sessions.discard(session_id)
        logger.info(f"Client disconnected from session: {session_id}")

@socketio.on('join_room')
def handle_join_room():
    """Handle join room request"""
    session_id = session.get('session_id')
    if session_id:
        join_room(session_id)
        emit('room_joined', {'session_id': session_id})

@socketio.on('test_connection')
def handle_test_connection():
    """Test WebSocket connection"""
    emit('test_response', {'message': 'WebSocket connection working!'})

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """500 error handler"""
    logger.error(f"Internal server error: {error}")
    return render_template('500.html'), 500

# ==================== BACKGROUND TASKS ====================

def cleanup_old_data():
    """Background task to cleanup old data"""
    while True:
        try:
            # Cleanup old sessions
            token_manager.cleanup_old_sessions()
            
            # Cleanup old spam managers
            with managers_lock:
                old_managers = []
                for session_id, manager in spam_managers.items():
                    if session_id not in active_sessions and not manager.is_running():
                        old_managers.append(session_id)
                
                for session_id in old_managers:
                    del spam_managers[session_id]
                    logger.info(f"Cleaned up spam manager for session: {session_id}")
            
            time.sleep(3600)  # Run every hour
        except Exception as e:
            logger.error(f"Error in cleanup task: {e}")
            time.sleep(300)  # Wait 5 minutes on error

# Start cleanup task
cleanup_thread = threading.Thread(target=cleanup_old_data, daemon=True)
cleanup_thread.start()

# ==================== RUN APP ====================

if __name__ == '__main__':
    # Development mode
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
else:
    # Production mode - for Gunicorn
    application = app
