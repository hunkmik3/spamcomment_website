#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Complete Template content for Vercel deployment - Match Local Version EXACTLY
@origin 250724-01 (Plants1.3)
"""

def get_index_template():
    """Return COMPLETE HTML content matching local version exactly"""
    return '''
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 Tool Spam FB Token - Professional Web Edition</title>
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    
    <!-- Socket.IO -->
    <script src="https://cdn.socket.io/4.7.2/socket.io.min.js"></script>
    
    <!-- Custom CSS -->
    <style>
        /* Custom Properties */
        :root {
            --primary-color: #007bff;
            --success-color: #28a745;
            --warning-color: #ffc107;
            --danger-color: #dc3545;
            --info-color: #17a2b8;
            --dark-color: #343a40;
            --light-color: #f8f9fa;
            
            --border-radius: 8px;
            --box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
            --box-shadow-lg: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
        }

        /* Global Styles */
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f5f5f5;
            line-height: 1.6;
        }

        /* Card Enhancements */
        .card {
            border: none;
            border-radius: var(--border-radius);
            box-shadow: var(--box-shadow);
            transition: all 0.3s ease;
        }

        .card:hover {
            box-shadow: var(--box-shadow-lg);
            transform: translateY(-2px);
        }

        .card-header {
            border-bottom: none;
            border-radius: var(--border-radius) var(--border-radius) 0 0 !important;
        }

        /* Gradient Backgrounds */
        .bg-gradient-primary {
            background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
        }

        /* Token Table Styles */
        .token-row {
            transition: all 0.2s ease;
        }

        .token-row:hover {
            background-color: #f8f9fa;
        }

        .token-row.selected {
            background-color: #e3f2fd;
        }

        .token-row.live {
            border-left: 4px solid #28a745;
        }

        .token-row.die {
            border-left: 4px solid #dc3545;
        }

        /* Status Badge Styles */
        .status-badge {
            font-size: 0.8em;
            font-weight: bold;
            padding: 0.25em 0.6em;
            border-radius: 10px;
        }

        .status-badge.live {
            background-color: #28a745;
            color: white;
        }

        .status-badge.die {
            background-color: #dc3545;
            color: white;
        }

        /* Log Styles */
        .log-entry {
            padding: 4px 8px;
            margin: 1px 0;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 0.85em;
            line-height: 1.4;
        }

        .log-info {
            color: #0d6efd;
        }

        .log-success {
            color: #198754;
        }

        .log-warning {
            color: #fd7e14;
        }

        .log-error {
            color: #dc3545;
        }

        /* Connection Status */
        #connection-status.connected {
            color: #28a745 !important;
        }

        #connection-status.disconnected {
            color: #dc3545 !important;
        }

        /* Modal Styles */
        .modal-content {
            border: none;
            border-radius: var(--border-radius);
            box-shadow: var(--box-shadow-lg);
        }

        /* Image Preview */
        .image-thumbnail {
            width: 100px;
            height: 100px;
            object-fit: cover;
            border-radius: var(--border-radius);
            border: 2px solid #dee2e6;
            transition: all 0.2s ease;
        }

        .image-thumbnail:hover {
            border-color: #007bff;
            transform: scale(1.05);
        }

        /* Drag & Drop Area */
        .upload-dropzone {
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .upload-dropzone:hover {
            background-color: #f8f9fa;
            border-color: #007bff !important;
        }

        .upload-dropzone.dragover {
            background-color: #e3f2fd;
            border-color: #007bff !important;
        }

        /* Progress Bar */
        .progress {
            height: 10px;
            border-radius: 5px;
        }

        /* Button Enhancements */
        .btn {
            border-radius: var(--border-radius);
            transition: all 0.2s ease;
        }

        .btn:hover {
            transform: translateY(-1px);
        }

        /* Navbar */
        .navbar-brand {
            font-weight: bold;
            font-size: 1.2em;
        }

        /* Responsive */
        @media (max-width: 768px) {
            .container-fluid {
                padding: 0.5rem;
            }
            
            .card-body {
                padding: 1rem;
            }
            
            .btn {
                margin-bottom: 0.5rem;
            }
        }
    </style>
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary sticky-top">
        <div class="container-fluid">
            <a class="navbar-brand fw-bold" href="#">
                <i class="fas fa-rocket me-2"></i>
                FB Spam Tool - Web Edition
            </a>
            
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="#token-management">
                            <i class="fas fa-key me-1"></i>Tokens
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#spam-section">
                            <i class="fas fa-comments me-1"></i>Auto Spam
                        </a>
                    </li>
                    <li class="nav-item">
                        <button class="btn btn-outline-light btn-sm me-2" id="emergency-cleanup" 
                                onclick="forceCleanupModal()" title="Khắc phục lỗi giao diện">
                            <i class="fas fa-broom"></i>
                        </button>
                    </li>
                    <li class="nav-item">
                        <span class="nav-link text-light" id="connection-status">
                            <i class="fas fa-circle text-success me-1" id="status-icon"></i>
                            <span id="status-text">Đã kết nối</span>
                        </span>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <div class="container-fluid py-4">
        <!-- Alert Container -->
        <div id="alert-container"></div>

        <!-- Page Header -->
        <div class="row mb-4">
            <div class="col-12">
                <div class="card bg-gradient-primary text-white">
                    <div class="card-body">
                        <h1 class="card-title mb-0">
                            <i class="fas fa-rocket me-2"></i>
                            Tool Spam FB Token - Professional Web Edition
                        </h1>
                        <p class="card-text mb-0 opacity-75">
                            Quản lý tokens, spam comments tự động và live chat - Phiên bản web chuyên nghiệp
                        </p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Statistics Cards -->
        <div class="row mb-4">
            <div class="col-md-3">
                <div class="card border-0 shadow-sm">
                    <div class="card-body text-center">
                        <i class="fas fa-key fa-2x text-primary mb-2"></i>
                        <h4 class="fw-bold mb-1" id="total-tokens">0</h4>
                        <small class="text-muted">Tổng Tokens</small>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card border-0 shadow-sm">
                    <div class="card-body text-center">
                        <i class="fas fa-check-circle fa-2x text-success mb-2"></i>
                        <h4 class="fw-bold mb-1" id="live-tokens">0</h4>
                        <small class="text-muted">Tokens LIVE</small>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card border-0 shadow-sm">
                    <div class="card-body text-center">
                        <i class="fas fa-comments fa-2x text-info mb-2"></i>
                        <h4 class="fw-bold mb-1" id="total-comments">0</h4>
                        <small class="text-muted">Comments Đã Gửi</small>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card border-0 shadow-sm">
                    <div class="card-body text-center">
                        <i class="fas fa-cog fa-2x text-warning mb-2"></i>
                        <h4 class="fw-bold mb-1" id="tool-status">Sẵn Sàng</h4>
                        <small class="text-muted">Trạng Thái Tool</small>
                    </div>
                </div>
            </div>
        </div>

        <!-- Token Management Section -->
        <div class="row mb-4" id="token-management">
            <div class="col-12">
                <div class="card shadow-sm">
                    <div class="card-header bg-primary text-white">
                        <h5 class="card-title mb-0">
                            <i class="fas fa-key me-2"></i>
                            🔑 Quản Lý Tài Khoản
                        </h5>
                    </div>
                    <div class="card-body">
                        <!-- Token Actions -->
                        <div class="row mb-3">
                            <div class="col-md-6">
                                <button class="btn btn-success me-2" id="btn-add-tokens">
                                    <i class="fas fa-plus me-1"></i>➕ Nhập Token
                                </button>
                                <button class="btn btn-info me-2" id="btn-check-selected">
                                    <i class="fas fa-check me-1"></i>🔍 Kiểm Tra Đã Chọn
                                </button>
                                <button class="btn btn-warning me-2" id="btn-upload-images">
                                    <i class="fas fa-image me-1"></i>📁 Upload Ảnh
                                </button>
                            </div>
                            <div class="col-md-6 text-end">
                                <div class="btn-group">
                                    <button class="btn btn-outline-danger dropdown-toggle" type="button" data-bs-toggle="dropdown">
                                        <i class="fas fa-trash me-1"></i>Xóa Tokens
                                    </button>
                                    <ul class="dropdown-menu">
                                        <li><a class="dropdown-item" href="#" id="btn-delete-selected">Xóa Đã Chọn</a></li>
                                        <li><a class="dropdown-item" href="#" id="btn-delete-die">Xóa Tokens DIE</a></li>
                                        <li><a class="dropdown-item" href="#" id="btn-delete-duplicates">Xóa Tokens Trùng</a></li>
                                        <li><hr class="dropdown-divider"></li>
                                        <li><a class="dropdown-item text-danger" href="#" id="btn-delete-all">Xóa Tất Cả</a></li>
                                    </ul>
                                </div>
                                <div class="form-check form-check-inline ms-3">
                                    <input class="form-check-input" type="checkbox" id="auto-like">
                                    <label class="form-check-label" for="auto-like">
                                        👍 Auto Like
                                    </label>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Tokens Table -->
                        <div class="table-responsive">
                            <table class="table table-hover">
                                <thead class="table-dark">
                                    <tr>
                                        <th width="5%">
                                            <input type="checkbox" id="select-all-tokens" class="form-check-input">
                                        </th>
                                        <th width="5%">STT</th>
                                        <th width="20%">👤 Page Name</th>
                                        <th width="40%">🔑 Token</th>
                                        <th width="10%">📊 Trạng Thái</th>
                                        <th width="10%">⚡ Comments</th>
                                        <th width="10%">🛠️ Thao Tác</th>
                                    </tr>
                                </thead>
                                <tbody id="tokens-table-body">
                                    <tr>
                                        <td colspan="7" class="text-center text-muted py-4">
                                            <i class="fas fa-info-circle me-2"></i>
                                            Chưa có tokens nào. Hãy thêm tokens để bắt đầu.
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                        
                        <!-- Image Gallery -->
                        <div class="mt-3" id="image-gallery" style="display: none;">
                            <h6><i class="fas fa-images me-2"></i>Ảnh Đã Upload</h6>
                            <div class="row" id="image-gallery-content"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Settings and Auto Spam Section -->
        <div class="row mb-4" id="spam-section">
            <div class="col-lg-8">
                <div class="card shadow-sm">
                    <div class="card-header bg-success text-white">
                        <h5 class="card-title mb-0">
                            <i class="fas fa-rocket me-2"></i>
                            🚀 Post & Comment - Auto Spam
                        </h5>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-6">
                                <label class="form-label fw-bold">📝 Post UID</label>
                                <textarea class="form-control" id="post-uids" rows="4" 
                                        placeholder="Nhập Post UID, mỗi UID một dòng..."></textarea>
                            </div>
                            <div class="col-md-6">
                                <label class="form-label fw-bold">💬 Comment</label>
                                <textarea class="form-control" id="comment-texts" rows="4" 
                                        placeholder="Nhập nội dung comment, mỗi comment một dòng..."></textarea>
                            </div>
                        </div>
                        
                        <div class="row mt-3">
                            <div class="col-12 text-center">
                                <button class="btn btn-success btn-lg me-2" id="btn-start-spam">
                                    <i class="fas fa-play me-1"></i>🚀 Bắt Đầu Spam
                                </button>
                                <button class="btn btn-danger btn-lg me-2" id="btn-stop-spam" style="display: none;">
                                    <i class="fas fa-stop me-1"></i>⏹️ Dừng Spam
                                </button>
                                <button class="btn btn-warning btn-lg" id="btn-pause-spam" style="display: none;">
                                    <i class="fas fa-pause me-1"></i>⏸️ Tạm Dừng
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="col-lg-4">
                <div class="card shadow-sm">
                    <div class="card-header bg-warning text-dark">
                        <h5 class="card-title mb-0">
                            <i class="fas fa-cog me-2"></i>
                            ⚙️ Cài Đặt & Trạng Thái
                        </h5>
                    </div>
                    <div class="card-body">
                        <div class="row g-3">
                            <div class="col-6">
                                <label class="form-label small">⏱️ Min Delay (ms)</label>
                                <input type="number" class="form-control form-control-sm" id="min-delay" value="500">
                            </div>
                            <div class="col-6">
                                <label class="form-label small">⏱️ Max Delay (ms)</label>
                                <input type="number" class="form-control form-control-sm" id="max-delay" value="2500">
                            </div>
                            <div class="col-6">
                                <label class="form-label small">🔄 Max Threads</label>
                                <input type="number" class="form-control form-control-sm" id="max-threads" value="10">
                            </div>
                            <div class="col-6">
                                <label class="form-label small">💬 Số Comment</label>
                                <input type="number" class="form-control form-control-sm" id="num-comments" value="0">
                            </div>
                            <div class="col-12">
                                <label class="form-label small">🖼️ Comment + Ảnh</label>
                                <input type="number" class="form-control form-control-sm" id="num-image-comments" value="0">
                            </div>
                        </div>
                        
                        <hr>
                        
                        <div class="status-cards">
                            <div class="alert alert-success mb-2" id="status-alert">
                                <i class="fas fa-check-circle me-2"></i>
                                <strong>✅ Tool Đã Sẵn Sàng Chạy</strong>
                            </div>
                            
                            <div class="alert alert-info mb-2">
                                <i class="fas fa-chart-bar me-2"></i>
                                <strong id="progress-text">📊 Comment 0/0</strong>
                            </div>
                            
                            <div class="alert alert-warning mb-0">
                                <i class="fas fa-chart-line me-2"></i>
                                <strong id="total-posted-text">📈 Tổng comment đã chạy: 0</strong>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Logs Section -->
        <div class="row">
            <div class="col-12">
                <div class="card shadow-sm">
                    <div class="card-header bg-dark text-white d-flex justify-content-between align-items-center">
                        <h5 class="card-title mb-0">
                            <i class="fas fa-terminal me-2"></i>
                            📋 Logs & Hoạt Động
                        </h5>
                        <button class="btn btn-outline-light btn-sm" id="btn-clear-logs">
                            <i class="fas fa-trash me-1"></i>Xóa Logs
                        </button>
                    </div>
                    <div class="card-body p-0">
                        <div id="logs-container" class="p-3 bg-dark text-light font-monospace" 
                             style="height: 300px; overflow-y: auto; font-size: 0.9em;">
                            <div class="text-success">
                                <i class="fas fa-info-circle me-2"></i>
                                [INFO] Tool khởi động thành công. Sẵn sàng sử dụng!
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Add Tokens Modal -->
    <div class="modal fade" id="addTokensModal" tabindex="-1">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header bg-success text-white">
                    <h5 class="modal-title">
                        <i class="fas fa-plus me-2"></i>
                        ➕ Nhập Token Facebook
                    </h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <div class="alert alert-info">
                        <i class="fas fa-info-circle me-2"></i>
                        <strong>Hướng dẫn:</strong> Nhập các token Facebook, mỗi token một dòng. Tool sẽ tự động kiểm tra và loại bỏ token trùng lặp.
                    </div>
                    
                    <label class="form-label fw-bold">🔑 Nhập Token - Mỗi token một dòng:</label>
                    <textarea class="form-control font-monospace" id="tokens-input" rows="12" 
                             placeholder="Nhập token ở đây, mỗi token một dòng...
Ví dụ:
EAAG...
EAAG...
EAAG..."></textarea>
                    
                    <div class="mt-3">
                        <small class="text-muted">
                            <i class="fas fa-shield-alt me-1"></i>
                            Token sẽ được mã hóa và chỉ lưu trữ trong phiên làm việc hiện tại.
                        </small>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                        <i class="fas fa-times me-1"></i>❌ Hủy
                    </button>
                    <button type="button" class="btn btn-success" id="btn-save-tokens">
                        <i class="fas fa-save me-1"></i>✅ Thêm Token
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- Upload Images Modal -->
    <div class="modal fade" id="uploadImagesModal" tabindex="-1">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header bg-warning text-dark">
                    <h5 class="modal-title">
                        <i class="fas fa-image me-2"></i>
                        📁 Upload Ảnh cho Comment
                    </h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <div class="alert alert-info">
                        <i class="fas fa-info-circle me-2"></i>
                        <strong>Hướng dẫn:</strong> Upload ảnh để sử dụng cho comment kèm ảnh. 
                        Hỗ trợ: JPG, JPEG, PNG, GIF, WEBP. Tối đa 50MB mỗi file.
                    </div>
                    
                    <!-- File Upload Area -->
                    <div class="mb-3">
                        <label class="form-label fw-bold">🖼️ Chọn ảnh để upload:</label>
                        <input type="file" class="form-control" id="images-input" 
                               accept="image/*" multiple>
                        <div class="form-text">
                            <i class="fas fa-info-circle me-1"></i>
                            Có thể chọn nhiều ảnh cùng lúc (Ctrl + Click)
                        </div>
                    </div>
                    
                    <!-- Drag & Drop Area -->
                    <div class="border border-2 border-dashed border-primary rounded p-4 text-center upload-dropzone" 
                         id="upload-dropzone">
                        <i class="fas fa-cloud-upload-alt fa-3x text-primary mb-3"></i>
                        <h5>Kéo thả ảnh vào đây</h5>
                        <p class="text-muted mb-0">hoặc click để chọn file</p>
                    </div>
                    
                    <!-- Upload Progress -->
                    <div class="mt-3" id="upload-progress-container" style="display: none;">
                        <label class="form-label">📈 Tiến độ upload:</label>
                        <div class="progress">
                            <div class="progress-bar progress-bar-striped progress-bar-animated" 
                                 id="upload-progress" role="progressbar" style="width: 0%">
                                0%
                            </div>
                        </div>
                    </div>
                    
                    <!-- Selected Files Preview -->
                    <div class="mt-3" id="selected-files-preview" style="display: none;">
                        <h6><i class="fas fa-images me-2"></i>Files đã chọn:</h6>
                        <div class="row" id="selected-files-list"></div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                        <i class="fas fa-times me-1"></i>❌ Hủy
                    </button>
                    <button type="button" class="btn btn-warning" id="btn-upload-images-confirm">
                        <i class="fas fa-upload me-1"></i>📤 Upload Ảnh
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- Token Details Modal -->
    <div class="modal fade" id="tokenDetailsModal" tabindex="-1">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header bg-info text-white">
                    <h5 class="modal-title">
                        <i class="fas fa-info-circle me-2"></i>
                        📊 Chi Tiết Token
                    </h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body" id="token-details-content">
                    <!-- Token details will be loaded here -->
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                        <i class="fas fa-times me-1"></i>Đóng
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- Loading Modal -->
    <div class="modal fade" id="loadingModal" tabindex="-1" data-bs-backdrop="static" data-bs-keyboard="false">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-body text-center py-4">
                    <div class="spinner-border spinner-border-lg text-primary mb-3" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <h5 id="loading-text">Đang xử lý...</h5>
                    <p class="text-muted mb-0" id="loading-detail">Vui lòng đợi</p>
                </div>
            </div>
        </div>
    </div>

    <!-- Scripts -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    
    <script>
        // Global variables - Match local version exactly
        let socket = null;
        let tokensData = [];
        let imagesData = [];
        let spamStatus = { is_running: false };
        let autoRefreshInterval = null;
        
        // Initialize Socket.IO connection (graceful fallback for Vercel)
        function initializeSocketIO() {
            try {
                socket = io();
                
                socket.on('connect', function() {
                    showConnectionStatus('connected', 'Đã kết nối');
                    addLog('Kết nối WebSocket thành công!', 'success');
                    socket.emit('join_room');
                });
                
                socket.on('disconnect', function() {
                    showConnectionStatus('disconnected', 'Mất kết nối');
                    addLog('Mất kết nối WebSocket. Đang thử kết nối lại...', 'warning');
                });
                
                socket.on('reconnect', function() {
                    showConnectionStatus('connected', 'Đã kết nối');
                    addLog('Đã kết nối lại WebSocket!', 'success');
                });
                
                // Token checking events
                socket.on('token_check_progress', function(data) {
                    updateLoadingModal(`Đang kiểm tra token ${data.current}/${data.total}`, 
                                      `Token: ${data.token_id}`);
                });
                
                socket.on('tokens_checked', function(data) {
                    hideLoadingModal();
                    if (data.success) {
                        loadTokensData();
                        showAlert('Kiểm tra token hoàn tất!', 'success');
                    }
                });
                
                // Spam events
                socket.on('spam_started', function(data) {
                    spamStatus.is_running = true;
                    updateSpamUI();
                    addLog(`Bắt đầu spam ${data.total_comments} comments cho ${data.posts} posts`, 'info');
                });
                
                socket.on('spam_progress', function(data) {
                    updateSpamProgress(data.comments_sent, data.total_comments);
                    addLog(`Comment #${data.comments_sent}: ${data.comment_id} - Post ${data.post_uid}${data.with_image ? ' (có ảnh)' : ''}`, 'success');
                });
                
                socket.on('spam_error', function(data) {
                    addLog(`Lỗi spam: ${data.error}`, 'error');
                });
                
                socket.on('spam_completed', function(data) {
                    spamStatus.is_running = false;
                    updateSpamUI();
                    hideLoadingModal();
                    addLog(`Hoàn thành spam! Total: ${data.total_comments}`, 'success');
                });
                
            } catch (e) {
                console.log('Socket.IO not available:', e);
                showConnectionStatus('disconnected', 'Chế độ HTTP');
                addLog('Chạy ở chế độ HTTP (không có WebSocket)', 'info');
            }
        }
        
        function showConnectionStatus(status, text) {
            const statusIcon = $('#status-icon');
            const statusText = $('#status-text');
            const connectionDiv = $('#connection-status');
            
            if (status === 'connected') {
                statusIcon.removeClass('text-danger').addClass('text-success');
                connectionDiv.removeClass('disconnected').addClass('connected');
            } else {
                statusIcon.removeClass('text-success').addClass('text-danger');
                connectionDiv.removeClass('connected').addClass('disconnected');
            }
            statusText.text(text);
        }
        
        // Initialize main application - Match local version exactly
        function initializeApp() {
            // Token management events
            $('#btn-add-tokens').click(() => $('#addTokensModal').modal('show'));
            $('#btn-upload-images').click(() => $('#uploadImagesModal').modal('show'));
            
            // Add tokens
            $('#btn-save-tokens').click(addTokens);
            
            // Token table events
            $('#select-all-tokens').change(toggleAllTokens);
            $('#btn-check-selected').click(checkSelectedTokens);
            $('#btn-delete-selected').click(() => deleteTokens('selected'));
            $('#btn-delete-all').click(() => deleteTokens('all'));
            $('#btn-delete-die').click(() => deleteTokens('die'));
            $('#btn-delete-duplicates').click(() => deleteTokens('duplicates'));
            
            // Spam management
            $('#btn-start-spam').click(startSpam);
            $('#btn-stop-spam').click(stopSpam);
            
            // Image upload
            $('#btn-upload-images-confirm').click(uploadImages);
            $('#images-input').change(previewSelectedFiles);
            
            // Logs
            $('#btn-clear-logs').click(clearLogs);
            
            // Auto fetch page names
            $('#post-uids').on('input', handleUIDChange);
            
            // File drag & drop
            setupFileDragDrop();
            
            // Setup modal event handlers
            setupModalHandlers();
            
            // Setup emergency cleanup
            setupEmergencyCleanup();
        }
        
        function setupModalHandlers() {
            // Handle loading modal events
            $('#loadingModal').on('hidden.bs.modal', function() {
                // Reset modal state when hidden
                $('#loading-text').text('Đang xử lý...');
                $('#loading-detail').text('Vui lòng đợi');
            });
            
            // Prevent loading modal from being closed by user
            $('#loadingModal').on('hide.bs.modal', function(e) {
                // Only allow programmatic hiding
                if (!$(this).data('allow-hide')) {
                    e.preventDefault();
                    return false;
                }
            });
        }
        
        function setupEmergencyCleanup() {
            // Emergency cleanup when clicking anywhere on page
            $(document).on('click', function(e) {
                // Check if there's a backdrop but no visible modal
                if ($('.modal-backdrop').length > 0 && !$('.modal.show').length) {
                    console.log('Detected stuck modal backdrop, cleaning up...');
                    forceCleanupModal();
                }
            });
            
            // Emergency cleanup on ESC key
            $(document).keydown(function(e) {
                if (e.keyCode === 27) { // ESC key
                    if ($('body').hasClass('modal-open') && !$('.modal.show').length) {
                        console.log('ESC pressed with modal-open but no visible modal, cleaning up...');
                        forceCleanupModal();
                    }
                }
                
                // Ctrl+Shift+F for manual cleanup
                if (e.ctrlKey && e.shiftKey && e.keyCode === 70) {
                    forceCleanupModal();
                }
            });
            
            // Periodic check for stuck modals
            setInterval(function() {
                if ($('body').hasClass('modal-open') && !$('.modal.show').length) {
                    console.log('Periodic check: detected stuck modal state, cleaning up...');
                    forceCleanupModal();
                }
            }, 5000);
        }
        
        function setupFileDragDrop() {
            const dropzone = $('#upload-dropzone');
            
            dropzone.on('click', function() {
                $('#images-input').click();
            });
            
            dropzone.on('dragover', function(e) {
                e.preventDefault();
                $(this).addClass('dragover');
            });
            
            dropzone.on('dragleave', function(e) {
                e.preventDefault();
                $(this).removeClass('dragover');
            });
            
            dropzone.on('drop', function(e) {
                e.preventDefault();
                $(this).removeClass('dragover');
                
                const files = e.originalEvent.dataTransfer.files;
                $('#images-input')[0].files = files;
                previewSelectedFiles();
            });
        }
        
        // Token management functions - Match local version exactly
        function addTokens() {
            const tokensText = $('#tokens-input').val().trim();
            if (!tokensText) {
                showAlert('Vui lòng nhập token!', 'warning');
                return;
            }
            
            showLoadingModal('Đang thêm tokens...', 'Vui lòng đợi');
            
            $.ajax({
                url: '/api/tokens',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ tokens: tokensText }),
                timeout: 30000, // 30 second timeout
                success: function(response) {
                    if (response.success) {
                        $('#addTokensModal').modal('hide');
                        $('#tokens-input').val('');
                        loadTokensData(); // This will not show loading modal
                        showAlert(response.message || 'Đã thêm tokens thành công!', 'success');
                    } else {
                        showAlert(response.message, 'danger');
                    }
                },
                error: function(xhr, status, error) {
                    console.error('Add tokens error:', status, error);
                    if (status === 'timeout') {
                        showAlert('Timeout khi thêm tokens! Vui lòng thử lại.', 'warning');
                    } else {
                        showAlert('Lỗi khi thêm tokens: ' + error, 'danger');
                    }
                },
                complete: function() {
                    // Always hide loading modal regardless of success or error
                    hideLoadingModal();
                }
            });
        }
        
        // Load tokens data WITHOUT loading modal (like local version)
        function loadTokensData() {
            $.ajax({
                url: '/api/tokens',
                method: 'GET',
                timeout: 10000,
                success: function(response) {
                    if (response.success) {
                        tokensData = response.tokens;
                        renderTokensTable();
                        updateStatistics();
                    } else {
                        console.error('Load tokens error:', response.message);
                        showAlert('Lỗi tải tokens: ' + response.message, 'danger');
                    }
                },
                error: function(xhr, status, error) {
                    console.error('Error loading tokens data:', status, error);
                    // Don't show alert for load errors, just log them
                    tokensData = [];
                    renderTokensTable();
                    updateStatistics();
                }
            });
        }
        
        function loadImagesData() {
            // Load images data - placeholder for now
            imagesData = [];
            renderImageGallery();
        }
        
        function renderTokensTable() {
            const tbody = $('#tokens-table-body');
            tbody.empty();
            
            if (!tokensData || tokensData.length === 0) {
                tbody.append(`
                    <tr>
                        <td colspan="7" class="text-center text-muted py-4">
                            <i class="fas fa-info-circle me-2"></i>
                            Chưa có tokens nào. Hãy thêm tokens để bắt đầu.
                        </td>
                    </tr>
                `);
                return;
            }
            
            tokensData.forEach((token, index) => {
                const statusClass = token.status === 'LIVE' ? 'live' : 'die';
                const statusBadge = token.status === 'LIVE' ? 
                    '<span class="badge bg-success">LIVE</span>' : 
                    '<span class="badge bg-danger">DIE</span>';
                
                const tokenDisplay = token.token ? token.token.substring(0, 30) + '...' : 'N/A';
                const commentsCount = token.comments_sent || 0;
                
                tbody.append(`
                    <tr class="token-row ${statusClass}" data-token-id="${token.id}">
                        <td><input type="checkbox" class="form-check-input token-checkbox" value="${token.id}"></td>
                        <td>${index + 1}</td>
                        <td>
                            <div class="d-flex align-items-center">
                                <i class="fab fa-facebook-square text-primary me-2"></i>
                                <span>${token.page_name || 'Unknown'}</span>
                            </div>
                        </td>
                        <td><code class="small">${tokenDisplay}</code></td>
                        <td>${statusBadge}</td>
                        <td>
                            <span class="badge bg-info">${commentsCount}</span>
                        </td>
                        <td>
                            <button class="btn btn-sm btn-outline-info me-1" onclick="viewTokenDetails('${token.id}')" title="Chi tiết">
                                <i class="fas fa-eye"></i>
                            </button>
                            <button class="btn btn-sm btn-outline-danger" onclick="deleteToken('${token.id}')" title="Xóa">
                                <i class="fas fa-trash"></i>
                            </button>
                        </td>
                    </tr>
                `);
            });
        }
        
        function renderImageGallery() {
            const gallery = $('#image-gallery');
            const content = $('#image-gallery-content');
            
            if (!imagesData || imagesData.length === 0) {
                gallery.hide();
                return;
            }
            
            content.empty();
            gallery.show();
            
            imagesData.forEach((image, index) => {
                content.append(`
                    <div class="col-md-2 mb-2">
                        <div class="card">
                            <img src="${image.url}" class="card-img-top image-thumbnail" alt="Image ${index + 1}">
                            <div class="card-body p-2">
                                <button class="btn btn-sm btn-outline-danger w-100" onclick="deleteImage('${image.id}')">
                                    <i class="fas fa-trash"></i>
                                </button>
                            </div>
                        </div>
                    </div>
                `);
            });
        }
        
        function deleteToken(tokenId) {
            if (!confirm('Bạn có chắc muốn xóa token này?')) return;
            
            showLoadingModal('Đang xóa token...');
            
            $.ajax({
                url: '/api/tokens/' + tokenId,
                method: 'DELETE',
                timeout: 10000,
                success: function(response) {
                    if (response.success) {
                        showAlert('Đã xóa token thành công!', 'success');
                        loadTokensData();
                    } else {
                        showAlert('Lỗi: ' + response.message, 'danger');
                    }
                },
                error: function(xhr, status, error) {
                    console.error('Delete token error:', error);
                    showAlert('Không thể xóa token: ' + error, 'danger');
                },
                complete: function() {
                    hideLoadingModal();
                }
            });
        }
        
        function updateStatistics() {
            const totalTokens = tokensData.length;
            const liveTokens = tokensData.filter(token => token.status === 'LIVE').length;
            const totalComments = tokensData.reduce((sum, token) => sum + (token.comments_sent || 0), 0);
            
            $('#total-tokens').text(totalTokens);
            $('#live-tokens').text(liveTokens);
            $('#total-comments').text(totalComments);
        }
        
        function startSpam() {
            const postUIDs = $('#post-uids').val().trim();
            const commentTexts = $('#comment-texts').val().trim();
            
            if (!postUIDs) {
                showAlert('Vui lòng nhập Post UIDs!', 'warning');
                return;
            }
            
            if (!commentTexts) {
                showAlert('Vui lòng nhập nội dung comment!', 'warning');
                return;
            }
            
            const data = {
                post_uids: postUIDs,
                comment_texts: commentTexts,
                min_delay: parseInt($('#min-delay').val()),
                max_delay: parseInt($('#max-delay').val()),
                max_threads: parseInt($('#max-threads').val()),
                auto_like: $('#auto-like').is(':checked')
            };
            
            showLoadingModal('Đang bắt đầu spam...', 'Chuẩn bị các comment tasks');
            
            $.ajax({
                url: '/api/spam/start',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(data),
                timeout: 30000,
                success: function(response) {
                    if (response.success) {
                        showAlert(response.message, 'success');
                        spamStatus.is_running = true;
                        updateSpamUI();
                        addLog('Đã khởi chạy spam process', 'success');
                    } else {
                        showAlert(response.message, 'danger');
                    }
                },
                error: function(xhr, status, error) {
                    console.error('Start spam error:', status, error);
                    if (status === 'timeout') {
                        showAlert('Timeout khi bắt đầu spam! Vui lòng thử lại.', 'warning');
                    } else {
                        showAlert('Lỗi khi bắt đầu spam: ' + error, 'danger');
                    }
                },
                complete: function() {
                    // Fallback to hide modal after 10 seconds
                    setTimeout(function() {
                        hideLoadingModal();
                    }, 10000);
                }
            });
        }
        
        function stopSpam() {
            if (!confirm('Bạn có chắc muốn dừng spam?')) return;
            spamStatus.is_running = false;
            updateSpamUI();
            addLog('Đã dừng spam', 'warning');
        }
        
        function updateSpamUI() {
            if (spamStatus.is_running) {
                $('#btn-start-spam').hide();
                $('#btn-stop-spam, #btn-pause-spam').show();
                $('#tool-status').text('Đang Chạy');
                $('#status-alert').removeClass('alert-success').addClass('alert-warning').html('<i class="fas fa-play me-2"></i><strong>🚀 Tool Đang Chạy</strong>');
            } else {
                $('#btn-start-spam').show();
                $('#btn-stop-spam, #btn-pause-spam').hide();
                $('#tool-status').text('Sẵn Sàng');
                $('#status-alert').removeClass('alert-warning').addClass('alert-success').html('<i class="fas fa-check-circle me-2"></i><strong>✅ Tool Đã Sẵn Sàng Chạy</strong>');
            }
        }
        
        function updateSpamProgress(current, total) {
            $('#progress-text').text(`📊 Comment ${current}/${total}`);
            $('#total-posted-text').text(`📈 Tổng comment đã chạy: ${current}`);
        }
        
        function addLog(message, type = 'info') {
            const timestamp = new Date().toLocaleTimeString();
            const logClass = 'log-' + type;
            const icon = {
                'info': 'fa-info-circle',
                'success': 'fa-check-circle',
                'warning': 'fa-exclamation-triangle',
                'error': 'fa-times-circle'
            }[type] || 'fa-info-circle';
            
            const logEntry = `
                <div class="log-entry ${logClass}">
                    <i class="fas ${icon} me-2"></i>
                    <span class="me-2">[${timestamp}]</span>
                    ${message}
                </div>
            `;
            
            $('#logs-container').append(logEntry);
            $('#logs-container').scrollTop($('#logs-container')[0].scrollHeight);
        }
        
        function clearLogs() {
            $('#logs-container').empty();
            addLog('Logs đã được xóa', 'info');
        }
        
        function showLoadingModal(title, detail = '') {
            $('#loading-text').text(title);
            $('#loading-detail').text(detail);
            
            // Reset allow-hide flag
            $('#loadingModal').data('allow-hide', false);
            $('#loadingModal').modal('show');
            
            // Auto-hide modal after 2 minutes as absolute fallback
            setTimeout(function() {
                hideLoadingModal();
            }, 120000);
        }
        
        function updateLoadingModal(title, detail = '') {
            $('#loading-text').text(title);
            $('#loading-detail').text(detail);
        }
        
        function hideLoadingModal() {
            try {
                // Set flag to allow hiding
                $('#loadingModal').data('allow-hide', true);
                $('#loadingModal').modal('hide');
                
                // Immediately force cleanup
                setTimeout(function() {
                    // Force remove modal classes and backdrop
                    $('#loadingModal').removeClass('show');
                    $('.modal-backdrop').remove();
                    $('body').removeClass('modal-open');
                    $('body').css('overflow', ''); // Reset body overflow
                    $('body').css('padding-right', ''); // Reset padding
                    
                    // Reset flag
                    $('#loadingModal').data('allow-hide', false);
                    
                    // Re-enable all buttons and inputs
                    $('button, input, select, textarea').prop('disabled', false);
                    
                    console.log('Loading modal cleanup completed');
                }, 100);
            } catch (error) {
                console.error('Error hiding loading modal:', error);
                // Force cleanup even if there's an error
                forceCleanupModal();
            }
        }
        
        function forceCleanupModal() {
            try {
                console.log('Starting force cleanup...');
                
                // Hide all modals
                $('.modal').modal('hide').removeClass('show in').hide();
                
                // Remove all backdrops
                $('.modal-backdrop, .modal-backdrop.fade, .modal-backdrop.show, .modal-backdrop.fade.show').remove();
                
                // Reset body
                $('body').removeClass('modal-open').css({
                    'overflow': '',
                    'overflow-x': '',
                    'overflow-y': '',
                    'padding-right': '',
                    'padding-left': '',
                    'margin-right': '',
                    'position': ''
                });
                
                // Reset html
                $('html').css({
                    'overflow': '',
                    'padding-right': ''
                });
                
                // Re-enable all interactive elements
                $('button, input, select, textarea, a, [tabindex]').prop('disabled', false);
                
                // Reset any z-index issues
                $('.modal').css('z-index', '');
                
                // Clear any stuck event handlers
                $(document).off('focusin.modal');
                
                // Show success message
                showAlert('Đã khắc phục lỗi giao diện thành công!', 'success');
                
                console.log('Force cleanup completed successfully');
            } catch (error) {
                console.error('Force cleanup failed:', error);
                // Last resort - reload page
                if (confirm('Không thể khắc phục lỗi giao diện. Bạn có muốn reload trang?')) {
                    location.reload();
                }
            }
        }
        
        function showAlert(message, type = 'info') {
            const alertClass = {
                'success': 'alert-success',
                'danger': 'alert-danger',
                'warning': 'alert-warning',
                'info': 'alert-info'
            }[type] || 'alert-info';
            
            const alertHtml = `
                <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
                    ${message}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            `;
            
            // Add to alert container
            $('#alert-container').prepend(alertHtml);
            
            // Auto remove after 5 seconds
            setTimeout(() => {
                $('#alert-container .alert').first().alert('close');
            }, 5000);
        }
        
        function startAutoRefresh() {
            // Auto refresh every 30 seconds
            autoRefreshInterval = setInterval(function() {
                if (!spamStatus.is_running) {
                    loadTokensData();
                }
            }, 30000);
        }
        
        // Placeholder functions for features being developed
        function checkSelectedTokens() {
            const selectedTokens = $('.token-checkbox:checked').length;
            if (selectedTokens === 0) {
                showAlert('Vui lòng chọn ít nhất một token!', 'warning');
                return;
            }
            showAlert(`Đang kiểm tra ${selectedTokens} tokens... (Tính năng đang phát triển cho môi trường serverless)`, 'info');
        }
        
        function deleteTokens(action) {
            showAlert(`Tính năng xóa ${action} tokens đang phát triển...`, 'info');
        }
        
        function toggleAllTokens() {
            const isChecked = $('#select-all-tokens').is(':checked');
            $('.token-checkbox').prop('checked', isChecked);
        }
        
        function viewTokenDetails(tokenId) {
            const token = tokensData.find(t => t.id === tokenId);
            if (!token) return;
            
            $('#token-details-content').html(`
                <div class="row">
                    <div class="col-md-6">
                        <h6>🔑 Token Info</h6>
                        <p><strong>Token:</strong> <code>${token.token.substring(0, 50)}...</code></p>
                        <p><strong>Page Name:</strong> ${token.page_name}</p>
                        <p><strong>Status:</strong> <span class="badge bg-${token.status === 'LIVE' ? 'success' : 'danger'}">${token.status}</span></p>
                    </div>
                    <div class="col-md-6">
                        <h6>📊 Statistics</h6>
                        <p><strong>Comments Sent:</strong> ${token.comments_sent || 0}</p>
                        <p><strong>Last Used:</strong> ${token.last_used || 'Never'}</p>
                        <p><strong>Created:</strong> ${token.created_at || 'Unknown'}</p>
                    </div>
                </div>
            `);
            
            $('#tokenDetailsModal').modal('show');
        }
        
        function uploadImages() {
            showAlert('Tính năng upload ảnh đang phát triển cho môi trường serverless...', 'info');
        }
        
        function previewSelectedFiles() {
            const files = $('#images-input')[0].files;
            if (files.length === 0) {
                $('#selected-files-preview').hide();
                return;
            }
            
            const preview = $('#selected-files-list');
            preview.empty();
            
            for (let i = 0; i < files.length; i++) {
                const file = files[i];
                const reader = new FileReader();
                
                reader.onload = function(e) {
                    preview.append(`
                        <div class="col-md-3 mb-2">
                            <div class="card">
                                <img src="${e.target.result}" class="card-img-top" style="height: 100px; object-fit: cover;">
                                <div class="card-body p-2">
                                    <small class="text-muted">${file.name}</small>
                                </div>
                            </div>
                        </div>
                    `);
                };
                
                reader.readAsDataURL(file);
            }
            
            $('#selected-files-preview').show();
        }
        
        function handleUIDChange() {
            // Placeholder for auto-fetching page names from UIDs
        }
        
        // Initialize everything when document is ready
        $(document).ready(function() {
            // Initialize Socket.IO (with graceful fallback)
            initializeSocketIO();
            
            // Initialize main app
            initializeApp();
            
            // Load initial data
            loadTokensData();
            loadImagesData();
            
            // Start auto refresh
            startAutoRefresh();
            
            // Initial log
            addLog('Tool khởi động thành công. Sẵn sàng sử dụng! (Phiên bản Vercel)', 'success');
        });
    </script>
</body>
</html>
    '''