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
                                <button type="button" class="btn btn-success me-2" id="btn-add-tokens">
                                    <i class="fas fa-plus me-1"></i>Thêm Tokens
                                </button>
                                <button type="button" class="btn btn-warning me-2" id="btn-check-selected">
                                    <i class="fas fa-sync me-1"></i>Kiểm tra đã chọn
                                </button>
                                <button type="button" class="btn btn-danger me-2" id="btn-delete-selected">
                                    <i class="fas fa-trash me-1"></i>Xóa đã chọn
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
                                            <input type="checkbox" id="select-all-tokens">
                                        </th>
                                        <th width="10%">STT</th>
                                        <th width="25%">Page Name</th>
                                        <th width="35%">Token</th>
                                        <th width="10%">Trạng thái</th>
                                        <th width="15%">Thao tác</th>
                                    </tr>
                                </thead>
                                <tbody id="tokens-table-body">
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
                                        <label for="post-uids" class="form-label">Post UIDs (mỗi UID một dòng)</label>
                                        <textarea class="form-control" id="post-uids" rows="4" required
                                                  placeholder="Nhập post UIDs..."></textarea>
                                    </div>
                                    
                                    <div class="mb-3">
                                        <label for="comment-text" class="form-label">Nội dung Comment</label>
                                        <textarea class="form-control" id="comment-text" rows="4" required
                                                  placeholder="Nhập nội dung comment..."></textarea>
                                    </div>
                                </div>
                                
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label class="form-label">Thời gian chờ (giây)</label>
                                        <div class="row">
                                            <div class="col-6">
                                                <input type="number" class="form-control" id="delay-min" value="5" min="1" max="300">
                                                <small class="text-muted">Tối thiểu</small>
                                            </div>
                                            <div class="col-6">
                                                <input type="number" class="form-control" id="delay-max" value="15" min="1" max="300">
                                                <small class="text-muted">Tối đa</small>
                                            </div>
                                        </div>
                                    </div>
                                    
                                    <div class="mb-3">
                                        <label class="form-label">Tùy chọn</label>
                                        <div class="form-check">
                                            <input class="form-check-input" type="checkbox" id="auto-like" checked>
                                            <label class="form-check-label" for="auto-like">
                                                Tự động like bài viết
                                            </label>
                                        </div>
                                        <div class="form-check">
                                            <input class="form-check-input" type="checkbox" id="random-comments">
                                            <label class="form-check-label" for="random-comments">
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
                                <button type="button" class="btn btn-success btn-lg me-2" id="btn-start-spam">
                                    <i class="fas fa-play me-1"></i>Bắt đầu Spam
                                </button>
                                <button type="button" class="btn btn-danger btn-lg" id="btn-stop-spam" style="display: none;">
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
                        <button type="button" class="btn btn-sm btn-outline-light" id="btn-clear-logs">
                            <i class="fas fa-trash me-1"></i>Xóa Logs
                        </button>
                    </div>
                    <div class="card-body p-0">
                        <div id="logs-container" style="height: 400px; overflow-y: auto; padding: 15px;">
                            <!-- Logs will appear here -->
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Add Token Modal -->
    <div class="modal fade" id="addTokensModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Thêm Tokens</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <form id="addTokenForm">
                        <div class="mb-3">
                            <label for="tokens-input" class="form-label">Tokens (mỗi token một dòng)</label>
                            <textarea class="form-control" id="tokens-input" rows="10" required
                                      placeholder="Nhập tokens, mỗi token một dòng..."></textarea>
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Hủy</button>
                    <button type="button" class="btn btn-primary" id="btn-save-tokens">Thêm Tokens</button>
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
        let spamStatus = { is_running: false };
        let autoRefreshInterval = null;
        
        // Initialize Socket.IO connection (graceful fallback for Vercel)
        function initializeSocketIO() {
            try {
                socket = io();
                
                socket.on('connect', function() {
                    showConnectionStatus('connected', 'Đã kết nối');
                    addLog('Kết nối WebSocket thành công!', 'success');
                });
                
                socket.on('disconnect', function() {
                    showConnectionStatus('disconnected', 'Mất kết nối');
                    addLog('Mất kết nối WebSocket. Đang thử kết nối lại...', 'warning');
                });
                
                socket.on('reconnect', function() {
                    showConnectionStatus('connected', 'Đã kết nối');
                    addLog('Đã kết nối lại WebSocket!', 'success');
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
            
            // Add tokens
            $('#btn-save-tokens').click(addTokens);
            
            // Token table events
            $('#select-all-tokens').change(toggleAllTokens);
            $('#btn-check-selected').click(checkSelectedTokens);
            $('#btn-delete-selected').click(deleteSelectedTokens);
            
            // Spam management
            $('#btn-start-spam').click(startSpam);
            $('#btn-stop-spam').click(stopSpam);
            
            // Logs
            $('#btn-clear-logs').click(clearLogs);
            
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
        
        function renderTokensTable() {
            const tbody = $('#tokens-table-body');
            tbody.empty();
            
            if (!tokensData || tokensData.length === 0) {
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
            
            tokensData.forEach((token, index) => {
                const statusClass = token.status === 'LIVE' ? 'live' : 'die';
                const statusBadge = token.status === 'LIVE' ? 
                    '<span class="badge bg-success">LIVE</span>' : 
                    '<span class="badge bg-danger">DIE</span>';
                
                const tokenDisplay = token.token ? token.token.substring(0, 20) + '...' : 'N/A';
                
                tbody.append(`
                    <tr class="token-row ${statusClass}" data-token-id="${token.id}">
                        <td><input type="checkbox" class="token-checkbox" value="${token.id}"></td>
                        <td>${index + 1}</td>
                        <td>${token.page_name || 'Unknown'}</td>
                        <td><code>${tokenDisplay}</code></td>
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
            
            $('#total-tokens').text(totalTokens);
            $('#live-tokens').text(liveTokens);
        }
        
        function startSpam() {
            const postUIDs = $('#post-uids').val().trim();
            const commentText = $('#comment-text').val().trim();
            
            if (!postUIDs) {
                showAlert('Vui lòng nhập Post UIDs!', 'warning');
                return;
            }
            
            if (!commentText) {
                showAlert('Vui lòng nhập nội dung comment!', 'warning');
                return;
            }
            
            const data = {
                post_uids: postUIDs,
                comment_text: commentText,
                delay_min: parseInt($('#delay-min').val()),
                delay_max: parseInt($('#delay-max').val()),
                auto_like: $('#auto-like').is(':checked'),
                random_comments: $('#random-comments').is(':checked')
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
                $('#btn-stop-spam').show();
            } else {
                $('#btn-start-spam').show();
                $('#btn-stop-spam').hide();
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
            
            // Add to top of container
            $('.container-fluid').prepend(alertHtml);
            
            // Auto remove after 5 seconds
            setTimeout(() => {
                $('.alert').first().alert('close');
            }, 5000);
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
        function checkSelectedTokens() {
            showAlert('Tính năng kiểm tra tokens đang phát triển cho môi trường serverless...', 'info');
        }
        
        function deleteSelectedTokens() {
            showAlert('Tính năng xóa nhiều tokens đang phát triển...', 'info');
        }
        
        function toggleAllTokens() {
            const isChecked = $('#select-all-tokens').is(':checked');
            $('.token-checkbox').prop('checked', isChecked);
        }
        
        function viewTokenDetails(tokenId) {
            showAlert('Tính năng xem chi tiết token đang phát triển...', 'info');
        }
        
        // Initialize everything when document is ready
        $(document).ready(function() {
            // Initialize Socket.IO (with graceful fallback)
            initializeSocketIO();
            
            // Initialize main app
            initializeApp();
            
            // Load initial data
            loadTokensData();
            
            // Start uptime counter
            updateUptime();
            
            // Initial log
            addLog('Ứng dụng đã khởi chạy thành công! (Phiên bản Vercel)', 'success');
        });
    </script>
</body>
</html>
    '''