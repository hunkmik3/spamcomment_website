#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flask Web App - Spam Comment Facebook Tool
@origin 250724-01 (Plants1.3)
"""

import os
import logging
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room
from werkzeug.utils import secure_filename
from werkzeug.middleware.proxy_fix import ProxyFix

# Import custom modules
from models.token_manager import WebTokenManager
from models.facebook_api import WebFacebookAPI
from models.spam_manager import SpamManager
from utils.helpers import allowed_file, generate_session_id

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask app configuration
app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.environ.get('SECRET_KEY', 'your-secret-key-here-change-in-production'),
    UPLOAD_FOLDER='uploads/images',
    MAX_CONTENT_LENGTH=50 * 1024 * 1024,  # 50MB max file size
    SESSION_PERMANENT=False,
    SESSION_TYPE='filesystem'
)

# Create upload directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('uploads/temp', exist_ok=True)

# Initialize SocketIO for real-time communication
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Initialize managers
token_manager = WebTokenManager()
spam_manager = SpamManager(socketio, token_manager)

# Proxy fix for deployment
app.wsgi_app = ProxyFix(app.wsgi_app)

@app.before_request
def before_request():
    """Initialize session if needed"""
    if 'session_id' not in session:
        session['session_id'] = generate_session_id()

@app.route('/')
def index():
    """Trang chủ - Dashboard chính"""
    return render_template('index.html')

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0',
        'description': 'Spam Comment Facebook Web Tool'
    })

# API Routes cho Token Management
@app.route('/api/tokens', methods=['GET'])
def get_tokens():
    """Lấy danh sách tokens"""
    session_id = session.get('session_id')
    tokens = token_manager.get_tokens(session_id)
    return jsonify({
        'success': True,
        'tokens': tokens,
        'total': len(tokens)
    })

@app.route('/api/tokens', methods=['POST'])
def add_tokens():
    """Thêm tokens mới"""
    try:
        data = request.get_json()
        tokens_text = data.get('tokens', '')
        session_id = session.get('session_id')
        
        if not tokens_text.strip():
            return jsonify({'success': False, 'message': 'Không có token nào được nhập!'})
        
        tokens = [token.strip() for token in tokens_text.splitlines() if token.strip()]
        if not tokens:
            return jsonify({'success': False, 'message': 'Không có token hợp lệ nào!'})
        
        added_count = token_manager.add_tokens(session_id, tokens)
        return jsonify({
            'success': True,
            'message': f'Đã thêm {added_count} token thành công!',
            'added_count': added_count
        })
    except Exception as e:
        logger.error(f"Error adding tokens: {e}")
        return jsonify({'success': False, 'message': 'Lỗi khi thêm token!'})

@app.route('/api/tokens/check', methods=['POST'])
def check_tokens():
    """Kiểm tra trạng thái tokens"""
    try:
        data = request.get_json()
        token_ids = data.get('token_ids', [])
        session_id = session.get('session_id')
        
        if not token_ids:
            return jsonify({'success': False, 'message': 'Không có token nào được chọn!'})
        
        # Start checking tokens in background
        def check_tokens_background():
            results = token_manager.check_tokens_status(session_id, token_ids, socketio)
            socketio.emit('tokens_checked', {
                'success': True,
                'results': results
            }, room=session_id)
        
        socketio.start_background_task(check_tokens_background)
        
        return jsonify({
            'success': True,
            'message': f'Đang kiểm tra {len(token_ids)} token...'
        })
    except Exception as e:
        logger.error(f"Error checking tokens: {e}")
        return jsonify({'success': False, 'message': 'Lỗi khi kiểm tra token!'})

@app.route('/api/tokens/delete', methods=['POST'])
def delete_tokens():
    """Xóa tokens"""
    try:
        data = request.get_json()
        action = data.get('action')
        token_ids = data.get('token_ids', [])
        session_id = session.get('session_id')
        
        deleted_count = 0
        if action == 'selected':
            deleted_count = token_manager.delete_tokens(session_id, token_ids)
        elif action == 'all':
            deleted_count = token_manager.delete_all_tokens(session_id)
        elif action == 'die':
            deleted_count = token_manager.delete_die_tokens(session_id)
        elif action == 'duplicates':
            deleted_count = token_manager.delete_duplicate_tokens(session_id)
        
        return jsonify({
            'success': True,
            'message': f'Đã xóa {deleted_count} token!',
            'deleted_count': deleted_count
        })
    except Exception as e:
        logger.error(f"Error deleting tokens: {e}")
        return jsonify({'success': False, 'message': 'Lỗi khi xóa token!'})

# API Routes cho File Upload
@app.route('/api/upload', methods=['POST'])
def upload_images():
    """Upload ảnh"""
    try:
        if 'images' not in request.files:
            return jsonify({'success': False, 'message': 'Không có file nào được chọn!'})
        
        files = request.files.getlist('images')
        session_id = session.get('session_id')
        
        # Create session folder
        session_folder = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
        os.makedirs(session_folder, exist_ok=True)
        
        uploaded_files = []
        for file in files:
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(session_folder, filename)
                file.save(filepath)
                uploaded_files.append(filename)
        
        return jsonify({
            'success': True,
            'message': f'Đã upload {len(uploaded_files)} ảnh thành công!',
            'uploaded_count': len(uploaded_files),
            'files': uploaded_files
        })
    except Exception as e:
        logger.error(f"Error uploading images: {e}")
        return jsonify({'success': False, 'message': 'Lỗi khi upload ảnh!'})

@app.route('/api/images')
def get_images():
    """Lấy danh sách ảnh đã upload"""
    try:
        session_id = session.get('session_id')
        session_folder = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
        
        if not os.path.exists(session_folder):
            return jsonify({'success': True, 'images': []})
        
        images = []
        for filename in os.listdir(session_folder):
            if allowed_file(filename):
                images.append({
                    'filename': filename,
                    'url': f'/uploads/images/{session_id}/{filename}'
                })
        
        return jsonify({'success': True, 'images': images})
    except Exception as e:
        logger.error(f"Error getting images: {e}")
        return jsonify({'success': False, 'message': 'Lỗi khi lấy danh sách ảnh!'})

# API Routes cho Page Info
@app.route('/api/page-info', methods=['POST'])
def get_page_info():
    """Lấy thông tin page từ UID"""
    try:
        data = request.get_json()
        post_uid = data.get('post_uid', '').strip()
        session_id = session.get('session_id')
        
        if not post_uid:
            return jsonify({'success': False, 'message': 'Post UID không được để trống!'})
        
        # Get available token
        token_info = token_manager.get_available_token(session_id)
        if not token_info:
            return jsonify({'success': False, 'message': 'Không có token khả dụng!'})
        
        page_name = WebFacebookAPI.fetch_page_name(token_info['token'], post_uid)
        if page_name:
            return jsonify({
                'success': True,
                'page_name': page_name,
                'formatted_uid': f"{post_uid} ({page_name})"
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Không thể lấy thông tin page!'
            })
    except Exception as e:
        logger.error(f"Error getting page info: {e}")
        return jsonify({'success': False, 'message': 'Lỗi khi lấy thông tin page!'})

# API Routes cho Spam Management
@app.route('/api/spam/start', methods=['POST'])
def start_spam():
    """Bắt đầu spam comments"""
    try:
        data = request.get_json()
        session_id = session.get('session_id')
        
        # Validate input
        post_uids = [uid.strip() for uid in data.get('post_uids', '').splitlines() if uid.strip()]
        comments = [cmt.strip() for cmt in data.get('comments', '').splitlines() if cmt.strip()]
        
        settings = {
            'min_delay': int(data.get('min_delay', 500)),
            'max_delay': int(data.get('max_delay', 2500)),
            'max_threads': int(data.get('max_threads', 10)),
            'num_comments': int(data.get('num_comments', 1)),
            'num_image_comments': int(data.get('num_image_comments', 0)),
            'auto_like': data.get('auto_like', False)
        }
        
        # Validation
        if not post_uids:
            return jsonify({'success': False, 'message': 'Vui lòng nhập Post UID!'})
        if not comments:
            return jsonify({'success': False, 'message': 'Vui lòng nhập nội dung comment!'})
        if len(comments) < settings['num_comments']:
            return jsonify({'success': False, 'message': 'Số comment trong box ít hơn số comment muốn chạy!'})
        if settings['min_delay'] >= settings['max_delay']:
            return jsonify({'success': False, 'message': 'Min Delay phải nhỏ hơn Max Delay!'})
        
        # Check tokens
        if not token_manager.has_available_tokens(session_id):
            return jsonify({'success': False, 'message': 'Không có token LIVE nào khả dụng!'})
        
        # Start spam process
        success = spam_manager.start_spam(session_id, post_uids, comments, settings)
        if success:
            return jsonify({'success': True, 'message': 'Đã bắt đầu spam comments!'})
        else:
            return jsonify({'success': False, 'message': 'Tool đang chạy hoặc có lỗi xảy ra!'})
        
    except Exception as e:
        logger.error(f"Error starting spam: {e}")
        return jsonify({'success': False, 'message': f'Lỗi khi bắt đầu spam: {str(e)}'})

@app.route('/api/spam/stop', methods=['POST'])
def stop_spam():
    """Dừng spam comments"""
    try:
        session_id = session.get('session_id')
        success = spam_manager.stop_spam(session_id)
        if success:
            return jsonify({'success': True, 'message': 'Đã dừng spam comments!'})
        else:
            return jsonify({'success': False, 'message': 'Tool chưa chạy hoặc đã dừng!'})
    except Exception as e:
        logger.error(f"Error stopping spam: {e}")
        return jsonify({'success': False, 'message': 'Lỗi khi dừng spam!'})

@app.route('/api/spam/status')
def get_spam_status():
    """Lấy trạng thái spam"""
    session_id = session.get('session_id')
    status = spam_manager.get_status(session_id)
    return jsonify(status)



# Serve uploaded files
@app.route('/uploads/images/<session_id>/<filename>')
def uploaded_file(session_id, filename):
    """Serve uploaded images"""
    from flask import send_from_directory
    return send_from_directory(
        os.path.join(app.config['UPLOAD_FOLDER'], session_id),
        filename
    )

# SocketIO Events
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    session_id = session.get('session_id')
    if session_id:
        join_room(session_id)
        emit('connected', {'message': 'Kết nối thành công!'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    session_id = session.get('session_id')
    if session_id:
        leave_room(session_id)

@socketio.on('join_room')
def handle_join_room():
    """Join room for real-time updates"""
    session_id = session.get('session_id')
    if session_id:
        join_room(session_id)
        emit('joined_room', {'room': session_id})

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({
        'success': False,
        'message': 'File quá lớn! Kích thước tối đa là 50MB.'
    }), 413

if __name__ == '__main__':
    # Development server
    socketio.run(
        app,
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=os.environ.get('FLASK_ENV') == 'development',
        allow_unsafe_werkzeug=True
    )
