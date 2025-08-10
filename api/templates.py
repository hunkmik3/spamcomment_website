#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Template content for Vercel deployment
@origin 250724-01 (Plants1.3)
"""

def get_index_template():
    """Return full HTML content for index page"""
    return '''
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FB Spam Tool - Web Version</title>
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    
    <!-- Font Awesome -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    
    <!-- Socket.IO (for future use) -->
    <script src="https://cdn.socket.io/4.7.0/socket.io.min.js"></script>
    
    <!-- Custom CSS -->
    <style>
        body {
            background-color: #f8f9fa;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .navbar-brand {
            font-weight: bold;
        }
        .card {
            transition: transform 0.2s ease-in-out;
        }
        .card:hover {
            transform: translateY(-2px);
        }
        .bg-gradient-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .token-row.live {
            background-color: #d1edff;
        }
        .token-row.die {
            background-color: #ffebee;
        }
        .status-badge.live {
            background-color: #28a745;
        }
        .status-badge.die {
            background-color: #dc3545;
        }
        .log-entry {
            padding: 8px 12px;
            margin: 2px 0;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }
        .log-info {
            background-color: #e3f2fd;
            border-left: 4px solid #2196f3;
        }
        .log-success {
            background-color: #e8f5e8;
            border-left: 4px solid #4caf50;
        }
        .log-warning {
            background-color: #fff3e0;
            border-left: 4px solid #ff9800;
        }
        .log-error {
            background-color: #ffebee;
            border-left: 4px solid #f44336;
        }
        #connection-status.connected {
            color: #28a745;
        }
        #connection-status.disconnected {
            color: #dc3545;
        }
        #loadingModal .modal-content {
            border: none;
            border-radius: 15px;
        }
        .spinner-border-lg {
            width: 3rem;
            height: 3rem;
        }
    </style>
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary shadow-sm">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">
                <i class="fab fa-facebook me-2"></i>
                FB Spam Tool
            </a>
            
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="#token-section">
                            <i class="fas fa-key me-1"></i>Tokens
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#spam-section">
                            <i class="fas fa-comments me-1"></i>Auto Spam
                        </a>
                    </li>
                </ul>
                
                <ul class="navbar-nav">
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

    <div class="container-fluid mt-4">
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
                            Quản lý tokens, spam comments tự động - Phiên bản web chuyên nghiệp
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
                        <i class="fas fa-clock fa-2x text-warning mb-2"></i>
                        <h4 class="fw-bold mb-1" id="uptime">0:00:00</h4>
                        <small class="text-muted">Thời Gian Hoạt Động</small>
                    </div>
                </div>
            </div>
        </div>

        <!-- Token Management Section -->
        <div class="row mb-4" id="token-section">
            <div class="col-12">
                <div class="card shadow-sm">
                    <div class="card-header bg-primary text-white">
                        <h5 class="mb-0">
                            <i class="fas fa-key me-2"></i>
                            Quản lý Tokens
                        </h5>
                    </div>
                    <div class="card-body">
                        <div class="row mb-3">
                            <div class="col-md-6">
                                <button type="button" class="btn btn-success me-2" data-bs-toggle="modal" data-bs-target="#addTokenModal">
                                    <i class="fas fa-plus me-1"></i>Thêm Tokens
                                </button>
                                <button type="button" class="btn btn-warning me-2" onclick="checkAllTokens()">
                                    <i class="fas fa-sync me-1"></i>Kiểm tra tất cả
                                </button>
                                <button type="button" class="btn btn-danger me-2" onclick="deleteAllTokens()">
                                    <i class="fas fa-trash me-1"></i>Xóa tất cả
                                </button>
                            </div>
                            <div class="col-md-6 text-end">
                                <div class="input-group">
                                    <input type="text" class="form-control" id="tokenSearch" placeholder="Tìm kiếm token...">
                                    <button class="btn btn-outline-secondary" type="button">
                                        <i class="fas fa-search"></i>
                                    </button>
                                </div>
                            </div>
                        </div>
                        
                        <div class="table-responsive">
                            <table class="table table-hover">
                                <thead class="table-dark">
                                    <tr>
                                        <th width="5%">
                                            <input type="checkbox" id="selectAllTokens" onchange="toggleSelectAll()">
                                        </th>
                                        <th width="10%">STT</th>
                                        <th width="25%">Page Name</th>
                                        <th width="35%">Token</th>
                                        <th width="10%">Trạng thái</th>
                                        <th width="15%">Thao tác</th>
                                    </tr>
                                </thead>
                                <tbody id="tokenTableBody">
                                    <!-- Tokens will be loaded here -->
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Auto Spam Section -->
        <div class="row mb-4" id="spam-section">
            <div class="col-12">
                <div class="card shadow-sm">
                    <div class="card-header bg-success text-white">
                        <h5 class="mb-0">
                            <i class="fas fa-comments me-2"></i>
                            Auto Spam Comments
                        </h5>
                    </div>
                    <div class="card-body">
                        <form id="spamForm">
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label for="targetUrl" class="form-label">URL Bài Viết/Post ID</label>
                                        <input type="text" class="form-control" id="targetUrl" required
                                               placeholder="https://facebook.com/post/123... hoặc post_id">
                                    </div>
                                    
                                    <div class="mb-3">
                                        <label for="commentText" class="form-label">Nội dung Comment</label>
                                        <textarea class="form-control" id="commentText" rows="4" required
                                                  placeholder="Nhập nội dung comment..."></textarea>
                                    </div>
                                </div>
                                
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label class="form-label">Thời gian chờ (giây)</label>
                                        <div class="row">
                                            <div class="col-6">
                                                <input type="number" class="form-control" id="delayMin" value="5" min="1" max="300">
                                                <small class="text-muted">Tối thiểu</small>
                                            </div>
                                            <div class="col-6">
                                                <input type="number" class="form-control" id="delayMax" value="15" min="1" max="300">
                                                <small class="text-muted">Tối đa</small>
                                            </div>
                                        </div>
                                    </div>
                                    
                                    <div class="mb-3">
                                        <label class="form-label">Tùy chọn</label>
                                        <div class="form-check">
                                            <input class="form-check-input" type="checkbox" id="autoLike" checked>
                                            <label class="form-check-label" for="autoLike">
                                                Tự động like bài viết
                                            </label>
                                        </div>
                                        <div class="form-check">
                                            <input class="form-check-input" type="checkbox" id="randomComment">
                                            <label class="form-check-label" for="randomComment">
                                                Random thứ tự comment
                                            </label>
                                        </div>
                                    </div>
                                    
                                    <div class="mb-3">
                                        <label for="imageUpload" class="form-label">Upload Ảnh (tùy chọn)</label>
                                        <input type="file" class="form-control" id="imageUpload" accept="image/*">
                                        <div id="imagePreview" class="mt-2"></div>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="text-center">
                                <button type="submit" class="btn btn-success btn-lg me-2" id="startSpamBtn">
                                    <i class="fas fa-play me-1"></i>Bắt đầu Spam
                                </button>
                                <button type="button" class="btn btn-danger btn-lg" id="stopSpamBtn" style="display: none;">
                                    <i class="fas fa-stop me-1"></i>Dừng Spam
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>

        <!-- Logs Section -->
        <div class="row">
            <div class="col-12">
                <div class="card shadow-sm">
                    <div class="card-header bg-info text-white d-flex justify-content-between align-items-center">
                        <h5 class="mb-0">
                            <i class="fas fa-list me-2"></i>
                            Logs Hoạt Động
                        </h5>
                        <button type="button" class="btn btn-sm btn-outline-light" onclick="clearLogs()">
                            <i class="fas fa-trash me-1"></i>Xóa Logs
                        </button>
                    </div>
                    <div class="card-body p-0">
                        <div id="logsContainer" style="height: 400px; overflow-y: auto; padding: 15px;">
                            <!-- Logs will appear here -->
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Add Token Modal -->
    <div class="modal fade" id="addTokenModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Thêm Tokens</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <form id="addTokenForm">
                        <div class="mb-3">
                            <label for="tokensInput" class="form-label">Tokens (mỗi token một dòng)</label>
                            <textarea class="form-control" id="tokensInput" rows="10" required
                                      placeholder="Nhập tokens, mỗi token một dòng..."></textarea>
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Hủy</button>
                    <button type="button" class="btn btn-primary" onclick="addTokens()">Thêm Tokens</button>
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
                    <h5 id="loadingText">Đang xử lý...</h5>
                    <p class="text-muted mb-0" id="loadingSubtext">Vui lòng đợi</p>
                </div>
            </div>
        </div>
    </div>

    <!-- Scripts -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    
    <script>
        // Basic JavaScript functionality
        let isSpamming = false;
        let spamInterval = null;
        let socket = null;
        
        // Initialize app
        $(document).ready(function() {
            loadTokens();
            setupFormHandlers();
            setupEmergencyCleanup();
            updateUptime();
            
            // Try to connect Socket.IO (will fail gracefully on Vercel)
            try {
                socket = io();
                socket.on('connect', function() {
                    updateConnectionStatus(true);
                    addLog('Đã kết nối WebSocket', 'success');
                });
                socket.on('disconnect', function() {
                    updateConnectionStatus(false);
                    addLog('Mất kết nối WebSocket', 'warning');
                });
            } catch (e) {
                console.log('Socket.IO not available:', e);
                addLog('Chạy ở chế độ HTTP (không có WebSocket)', 'info');
            }
        });
        
        function setupFormHandlers() {
            $('#spamForm').on('submit', function(e) {
                e.preventDefault();
                startSpam();
            });
            
            $('#imageUpload').on('change', function() {
                handleImageUpload(this);
            });
        }
        
        function loadTokens() {
            showLoadingModal('Đang tải tokens...');
            
            $.ajax({
                url: '/api/tokens',
                method: 'GET',
                timeout: 10000,
                success: function(response) {
                    if (response.success) {
                        displayTokens(response.tokens);
                        updateStatistics();
                    } else {
                        showAlert('Lỗi: ' + response.message, 'danger');
                    }
                },
                error: function(xhr, status, error) {
                    console.error('Load tokens error:', error);
                    showAlert('Không thể tải tokens: ' + error, 'danger');
                },
                complete: function() {
                    hideLoadingModal();
                }
            });
        }
        
        function addTokens() {
            const tokens = $('#tokensInput').val().trim();
            if (!tokens) {
                showAlert('Vui lòng nhập tokens', 'warning');
                return;
            }
            
            showLoadingModal('Đang thêm tokens...');
            
            $.ajax({
                url: '/api/tokens',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ tokens: tokens }),
                timeout: 30000,
                success: function(response) {
                    if (response.success) {
                        showAlert('Đã thêm tokens thành công!', 'success');
                        $('#addTokenModal').modal('hide');
                        $('#tokensInput').val('');
                        loadTokens();
                    } else {
                        showAlert('Lỗi: ' + response.message, 'danger');
                    }
                },
                error: function(xhr, status, error) {
                    console.error('Add tokens error:', error);
                    showAlert('Không thể thêm tokens: ' + error, 'danger');
                },
                complete: function() {
                    hideLoadingModal();
                }
            });
        }
        
        function startSpam() {
            const formData = {
                target_url: $('#targetUrl').val(),
                comment_text: $('#commentText').val(),
                delay_min: parseInt($('#delayMin').val()),
                delay_max: parseInt($('#delayMax').val()),
                auto_like: $('#autoLike').is(':checked'),
                random_comment: $('#randomComment').is(':checked')
            };
            
            showLoadingModal('Đang khởi chạy spam...');
            
            $.ajax({
                url: '/api/spam/start',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(formData),
                timeout: 10000,
                success: function(response) {
                    if (response.success) {
                        showAlert(response.message, 'success');
                        isSpamming = true;
                        $('#startSpamBtn').hide();
                        $('#stopSpamBtn').show();
                    } else {
                        showAlert('Lỗi: ' + response.message, 'danger');
                    }
                },
                error: function(xhr, status, error) {
                    console.error('Start spam error:', error);
                    showAlert('Không thể khởi chạy spam: ' + error, 'danger');
                },
                complete: function() {
                    hideLoadingModal();
                }
            });
        }
        
        function displayTokens(tokens) {
            const tbody = $('#tokenTableBody');
            tbody.empty();
            
            if (!tokens || tokens.length === 0) {
                tbody.append(`
                    <tr>
                        <td colspan="6" class="text-center text-muted">
                            <i class="fas fa-info-circle me-2"></i>
                            Chưa có tokens nào. Hãy thêm tokens để bắt đầu.
                        </td>
                    </tr>
                `);
                return;
            }
            
            tokens.forEach((token, index) => {
                const statusClass = token.status === 'LIVE' ? 'live' : 'die';
                const statusBadge = token.status === 'LIVE' ? 
                    '<span class="badge bg-success">LIVE</span>' : 
                    '<span class="badge bg-danger">DIE</span>';
                
                tbody.append(`
                    <tr class="token-row ${statusClass}" data-token-id="${token.id}">
                        <td><input type="checkbox" class="token-checkbox" value="${token.id}"></td>
                        <td>${index + 1}</td>
                        <td>${token.page_name}</td>
                        <td><code>${token.token.substring(0, 20)}...</code></td>
                        <td>${statusBadge}</td>
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
                        loadTokens();
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
            const tokens = $('#tokenTableBody tr').not(':contains("Chưa có tokens")').length;
            const liveTokens = $('#tokenTableBody .badge.bg-success').length;
            
            $('#total-tokens').text(tokens);
            $('#live-tokens').text(liveTokens);
        }
        
        function updateConnectionStatus(connected) {
            const statusIcon = $('#status-icon');
            const statusText = $('#status-text');
            
            if (connected) {
                statusIcon.removeClass('text-danger').addClass('text-success');
                statusText.text('Đã kết nối');
            } else {
                statusIcon.removeClass('text-success').addClass('text-danger');
                statusText.text('Mất kết nối');
            }
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
            
            $('#logsContainer').append(logEntry);
            $('#logsContainer').scrollTop($('#logsContainer')[0].scrollHeight);
        }
        
        function clearLogs() {
            $('#logsContainer').empty();
            addLog('Logs đã được xóa', 'info');
        }
        
        function showLoadingModal(text = 'Đang xử lý...', subtext = 'Vui lòng đợi') {
            $('#loadingText').text(text);
            $('#loadingSubtext').text(subtext);
            $('#loadingModal').modal('show');
        }
        
        function hideLoadingModal() {
            $('#loadingModal').modal('hide');
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
            
            // Add to top of container
            $('.container-fluid').prepend(alertHtml);
            
            // Auto remove after 5 seconds
            setTimeout(() => {
                $('.alert').first().alert('close');
            }, 5000);
        }
        
        function forceCleanupModal() {
            try {
                // Hide all modals
                $('.modal').modal('hide');
                $('.modal-backdrop').remove();
                $('body').removeClass('modal-open').css('overflow', '');
                
                showAlert('Đã khắc phục lỗi giao diện thành công!', 'success');
            } catch (error) {
                console.error('Force cleanup failed:', error);
            }
        }
        
        function setupEmergencyCleanup() {
            // Add keyboard shortcut
            $(document).keydown(function(e) {
                if (e.ctrlKey && e.shiftKey && e.keyCode === 70) { // Ctrl+Shift+F
                    forceCleanupModal();
                }
            });
        }
        
        function updateUptime() {
            let startTime = Date.now();
            setInterval(() => {
                const uptime = Date.now() - startTime;
                const hours = Math.floor(uptime / 3600000);
                const minutes = Math.floor((uptime % 3600000) / 60000);
                const seconds = Math.floor((uptime % 60000) / 1000);
                $('#uptime').text(`${hours}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`);
            }, 1000);
        }
        
        // Placeholder functions
        function checkAllTokens() {
            showAlert('Tính năng đang phát triển...', 'info');
        }
        
        function deleteAllTokens() {
            showAlert('Tính năng đang phát triển...', 'info');
        }
        
        function toggleSelectAll() {
            const isChecked = $('#selectAllTokens').is(':checked');
            $('.token-checkbox').prop('checked', isChecked);
        }
        
        function viewTokenDetails(tokenId) {
            showAlert('Tính năng đang phát triển...', 'info');
        }
        
        function handleImageUpload(input) {
            if (input.files && input.files[0]) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    $('#imagePreview').html(`
                        <img src="${e.target.result}" class="img-thumbnail" style="max-width: 200px;">
                        <button type="button" class="btn btn-sm btn-outline-danger ms-2" onclick="$('#imagePreview').empty(); $('#imageUpload').val('');">
                            <i class="fas fa-times"></i>
                        </button>
                    `);
                };
                reader.readAsDataURL(input.files[0]);
            }
        }
        
        // Initial log
        addLog('Ứng dụng đã khởi chạy thành công!', 'success');
    </script>
</body>
</html>
    '''
