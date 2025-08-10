#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vercel entry point - Minimal Flask App
@origin 250724-01 (Plants1.3)
"""

from flask import Flask, render_template, jsonify

# Create Flask app
app = Flask(__name__)

@app.route('/')
def index():
    """Main dashboard"""
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
        <div class="container mt-5">
            <div class="row">
                <div class="col-12 text-center">
                    <h1 class="display-4 text-primary">
                        <i class="fab fa-facebook me-3"></i>
                        FB Spam Tool - Web Version
                    </h1>
                    <p class="lead text-muted">Tool quản lý và auto spam Facebook - Phiên bản Web</p>
                    <div class="alert alert-success mt-4" role="alert">
                        <i class="fas fa-check-circle me-2"></i>
                        <strong>Deployment thành công!</strong> Website đã hoạt động trên Vercel.
                    </div>
                    
                    <div class="row mt-5">
                        <div class="col-md-4">
                            <div class="card h-100">
                                <div class="card-body text-center">
                                    <i class="fas fa-key fa-3x text-primary mb-3"></i>
                                    <h5 class="card-title">Quản lý Token</h5>
                                    <p class="card-text">Thêm, xóa và kiểm tra trạng thái Facebook tokens</p>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="card h-100">
                                <div class="card-body text-center">
                                    <i class="fas fa-comments fa-3x text-success mb-3"></i>
                                    <h5 class="card-title">Auto Spam</h5>
                                    <p class="card-text">Tự động comment và like bài viết Facebook</p>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="card h-100">
                                <div class="card-body text-center">
                                    <i class="fas fa-image fa-3x text-warning mb-3"></i>
                                    <h5 class="card-title">Upload Ảnh</h5>
                                    <p class="card-text">Upload và quản lý ảnh cho comment</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="mt-5">
                        <a href="/api/test" class="btn btn-primary btn-lg">
                            <i class="fas fa-flask me-2"></i>Test API
                        </a>
                    </div>
                </div>
            </div>
        </div>
        
        <footer class="mt-5 py-4 bg-light text-center">
            <p class="text-muted mb-0">
                <i class="fas fa-heart text-danger"></i> 
                Phát triển bởi FB Spam Tool Team - Deployed on Vercel
            </p>
        </footer>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    '''

@app.route('/api/test')
def test_api():
    """Test API endpoint"""
    return jsonify({
        'success': True,
        'message': 'API hoạt động bình thường!',
        'version': '1.0.0',
        'platform': 'Vercel',
        'features': [
            'Token Management',
            'Auto Spam',
            'Image Upload',
            'Facebook API Integration'
        ]
    })

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'FB Spam Tool',
        'timestamp': '2024-01-01T00:00:00Z'
    })

# For Vercel
application = app

if __name__ == "__main__":
    app.run(debug=True)