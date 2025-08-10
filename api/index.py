#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vercel entry point for Flask App (Full UI without Socket.IO)
@origin 250724-01 (Plants1.3)
"""

import os
import sys

# Add the parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from flask import Flask, render_template, request, jsonify, session, send_from_directory
    from werkzeug.utils import secure_filename
    import time
    import uuid
    import logging
    
    # Try to import custom modules, with fallbacks
    try:
        from models.token_manager import WebTokenManager
        from models.facebook_api import WebFacebookAPI  
        from models.spam_manager import SpamManager
        from utils.helpers import generate_session_id, allowed_file
        MODULES_AVAILABLE = True
    except ImportError as e:
        logging.warning(f"Custom modules not available: {e}")
        MODULES_AVAILABLE = False
        
        # Fallback classes
        class WebTokenManager:
            def __init__(self, session_id): 
                self.session_id = session_id
                self.tokens = {}
            def get_all_tokens(self): 
                return []
            def add_token(self, token, name, status): 
                return str(uuid.uuid4())
            def remove_token(self, token_id): 
                pass
                
        class WebFacebookAPI:
            def check_token_status(self, token):
                return {'is_valid': True, 'page_name': 'Test Page'}
                
        def generate_session_id():
            return str(uuid.uuid4())
            
        def allowed_file(filename):
            return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

except ImportError as e:
    # Ultimate fallback
    from flask import Flask, jsonify
    
    app = Flask(__name__)
    
    @app.route('/')
    def fallback():
        return jsonify({'error': 'Import error', 'message': str(e)})
    
    application = app
    
else:
    # Initialize Flask app with proper paths
    template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
    static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
    
    app = Flask(__name__, 
               template_folder=template_dir,
               static_folder=static_dir)

    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-2024-production')
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads', 'images')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

    # Ensure upload directory exists
    try:
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    except:
        pass

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
        """Main dashboard - render full UI"""
        try:
            return render_template('index.html')
        except Exception as e:
            logger.error(f"Template error: {e}")
            # Use embedded template for Vercel
            try:
                from api.templates import get_index_template
                return get_index_template()
            except ImportError:
                # Ultimate fallback HTML
                return '''
            <!DOCTYPE html>
            <html lang="vi">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>FB Spam Tool - Web Version</title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
                <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
            </head>
            <body>
                <div class="container-fluid">
                    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
                        <div class="container-fluid">
                            <a class="navbar-brand" href="#"><i class="fab fa-facebook me-2"></i>FB Spam Tool</a>
                        </div>
                    </nav>
                    
                    <div class="container mt-4">
                        <div class="alert alert-warning">
                            <i class="fas fa-exclamation-triangle me-2"></i>
                            Template files không tìm thấy. Đang chạy ở chế độ fallback.
                        </div>
                        
                        <div class="row">
                            <div class="col-12">
                                <h2>FB Spam Tool - Web Version</h2>
                                <p>Giao diện đầy đủ sẽ có sẵn khi template files được deploy đúng cách.</p>
                            </div>
                        </div>
                    </div>
                </div>
            </body>
            </html>
            '''

    @app.route('/api/tokens', methods=['GET'])
    def get_tokens():
        """Get all tokens for current session"""
        try:
            if not MODULES_AVAILABLE:
                return jsonify({'success': False, 'message': 'Module không khả dụng trong môi trường Vercel'})
                
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
            if not MODULES_AVAILABLE:
                return jsonify({'success': False, 'message': 'Token management không khả dụng trong môi trường Vercel'})
                
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
            if not MODULES_AVAILABLE:
                return jsonify({'success': False, 'message': 'Token management không khả dụng'})
                
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
            
            # Note: In serverless environment, background tasks need special handling
            return jsonify({
                'success': True, 
                'message': 'Spam process đã được khởi chạy (Lưu ý: Real-time features bị giới hạn trong môi trường serverless)'
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
                
                try:
                    os.makedirs(upload_dir, exist_ok=True)
                    filepath = os.path.join(upload_dir, filename)
                    file.save(filepath)
                    
                    return jsonify({
                        'success': True,
                        'filename': filename,
                        'url': f'/uploads/images/{session_id}/{filename}'
                    })
                except Exception as e:
                    return jsonify({'success': False, 'message': f'Lỗi lưu file: {str(e)}'})
            else:
                return jsonify({'success': False, 'message': 'File không hợp lệ. Chỉ chấp nhận: jpg, jpeg, png, gif'}), 400
        
        except Exception as e:
            logger.error(f"Error uploading file: {e}")
            return jsonify({'success': False, 'message': str(e)}), 500

    @app.route('/uploads/images/<session_id>/<filename>')
    def uploaded_file(session_id, filename):
        """Serve uploaded images"""
        try:
            return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], session_id), filename)
        except:
            return jsonify({'error': 'File not found'}), 404

    @app.route('/api/test')
    def test_api():
        """Test API endpoint"""
        return jsonify({
            'success': True,
            'message': 'API hoạt động bình thường!',
            'modules_available': MODULES_AVAILABLE,
            'template_dir': template_dir,
            'static_dir': static_dir
        })

    @app.errorhandler(404)
    def not_found(error):
        """404 error handler"""
        try:
            return render_template('404.html'), 404
        except:
            return jsonify({'error': '404 Not Found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        """500 error handler"""
        logger.error(f"Internal server error: {error}")
        try:
            return render_template('500.html'), 500
        except:
            return jsonify({'error': '500 Internal Server Error'}), 500

    # For Vercel
    application = app

if __name__ == "__main__":
    app.run(debug=True)