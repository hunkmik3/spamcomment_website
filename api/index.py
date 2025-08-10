#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vercel entry point for Flask App (Simplified without Socket.IO)
@origin 250724-01 (Plants1.3)
"""

import os
import sys

# Add the parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import Flask app without Socket.IO for Vercel compatibility
from flask import Flask, render_template, request, jsonify, session, send_from_directory
from werkzeug.utils import secure_filename
import uuid
import logging
import time

# Import custom modules
from models.token_manager import WebTokenManager
from models.facebook_api import WebFacebookAPI
from models.spam_manager import SpamManager
from utils.helpers import generate_session_id, allowed_file, get_image_path, delete_image_file

# Initialize Flask app
app = Flask(__name__, 
           template_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates'),
           static_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static'))

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-2024-production')
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads', 'images')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.before_request
def before_request():
    """Initialize session if not exists"""
    if 'session_id' not in session:
        session['session_id'] = generate_session_id()

@app.route('/')
def dashboard():
    """Main dashboard"""
    return render_template('index.html')

@app.route('/api/tokens', methods=['GET'])
def get_tokens():
    """Get all tokens for current session"""
    try:
        session_id = session.get('session_id')
        token_manager = WebTokenManager(session_id)
        tokens = token_manager.get_all_tokens()
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
        
        session_id = session.get('session_id')
        token_manager = WebTokenManager(session_id)
        facebook_api = WebFacebookAPI()
        
        # Parse tokens
        tokens = [token.strip() for token in tokens_text.split('\n') if token.strip()]
        
        results = []
        for token in tokens:
            try:
                # Check token status
                status_info = facebook_api.check_token_status(token)
                page_name = status_info.get('page_name', 'Unknown')
                status = 'LIVE' if status_info.get('is_valid') else 'DIE'
                
                # Add token
                token_id = token_manager.add_token(token, page_name, status)
                results.append({
                    'token_id': token_id,
                    'page_name': page_name,
                    'status': status,
                    'token': token[:20] + '...' if len(token) > 20 else token
                })
            except Exception as e:
                logger.error(f"Error checking token {token[:10]}...: {e}")
                results.append({
                    'token': token[:20] + '...' if len(token) > 20 else token,
                    'status': 'ERROR',
                    'error': str(e)
                })
        
        return jsonify({'success': True, 'results': results})
    
    except Exception as e:
        logger.error(f"Error adding tokens: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/tokens/<token_id>', methods=['DELETE'])
def delete_token(token_id):
    """Delete a token"""
    try:
        session_id = session.get('session_id')
        token_manager = WebTokenManager(session_id)
        token_manager.remove_token(token_id)
        return jsonify({'success': True, 'message': 'Token đã được xóa'})
    except Exception as e:
        logger.error(f"Error deleting token: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/spam/start', methods=['POST'])
def start_spam():
    """Start spamming process"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['target_url', 'comment_text', 'delay_min', 'delay_max']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'message': f'Thiếu trường {field}'}), 400
        
        session_id = session.get('session_id')
        token_manager = WebTokenManager(session_id)
        
        # Check if we have tokens
        tokens = token_manager.get_all_tokens()
        if not tokens:
            return jsonify({'success': False, 'message': 'Vui lòng thêm token trước khi spam'}), 400
        
        # Note: In serverless environment, we can't run background tasks
        # This would need to be handled differently (e.g., queue system)
        return jsonify({
            'success': True, 
            'message': 'Spam process started (Note: Full functionality requires WebSocket support)'
        })
    
    except Exception as e:
        logger.error(f"Error starting spam: {e}")
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
            
            session_id = session.get('session_id')
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

@app.route('/uploads/images/<session_id>/<filename>')
def uploaded_file(session_id, filename):
    """Serve uploaded images"""
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], session_id), filename)

@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """500 error handler"""
    logger.error(f"Internal server error: {error}")
    return render_template('500.html'), 500

# For Vercel
application = app

if __name__ == "__main__":
    app.run(debug=True)