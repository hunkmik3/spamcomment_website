/*
Main JavaScript for Facebook Spam Tool Web Edition
@origin 250724-01 (Plants1.3)
*/

// Global variables
let socket = null;
let tokensData = [];
let imagesData = [];
let spamStatus = { is_running: false };
let autoRefreshInterval = null;

// Initialize Socket.IO connection
function initializeSocketIO() {
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
        addLog(`Lỗi: ${data.message}`, 'error');
    });
    
    socket.on('spam_completed', function(data) {
        spamStatus.is_running = false;
        updateSpamUI();
        hideLoadingModal();
        addLog(`Hoàn thành spam! Đã gửi ${data.stats.comments_sent}/${data.stats.total_comments} comments trong ${formatDuration(data.duration)}`, 'success');
        showAlert('Spam comments hoàn tất!', 'success');
    });
    
    socket.on('spam_stopped', function(data) {
        spamStatus.is_running = false;
        updateSpamUI();
        hideLoadingModal();
        addLog('Đã dừng spam comments', 'warning');
    });
    

}

// Connection status management
function showConnectionStatus(status, text) {
    const statusIcon = $('#status-icon');
    const statusText = $('#status-text');
    const connectionStatus = $('#connection-status');
    
    connectionStatus.removeClass('status-connected status-disconnected status-connecting');
    connectionStatus.addClass(`status-${status}`);
    
    statusText.text(text);
    
    if (status === 'connected') {
        statusIcon.removeClass('fa-circle fa-exclamation-triangle').addClass('fa-circle');
    } else {
        statusIcon.removeClass('fa-circle').addClass('fa-exclamation-triangle');
    }
}

// Initialize main application
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
    $('#btn-upload-images').click(uploadImages);
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
        // If modal backdrop exists but modal is not visible, force cleanup
        if ($('.modal-backdrop').length > 0 && !$('#loadingModal').hasClass('show')) {
            console.log('Emergency cleanup triggered');
            forceCleanupModal();
        }
    });
    
    // Emergency cleanup with ESC key
    $(document).on('keydown', function(e) {
        if (e.key === 'Escape') {
            setTimeout(function() {
                if ($('body').hasClass('modal-open') && !$('.modal.show').length) {
                    console.log('ESC emergency cleanup triggered');
                    forceCleanupModal();
                }
            }, 100);
        }
        
        // Force cleanup with Ctrl+Shift+F (emergency hotkey)
        if (e.ctrlKey && e.shiftKey && e.key === 'F') {
            e.preventDefault();
            console.log('Manual emergency cleanup triggered (Ctrl+Shift+F)');
            forceCleanupModal();
        }
    });
    
    // Periodic check for stuck modals (every 5 seconds)
    setInterval(function() {
        if ($('body').hasClass('modal-open') && !$('.modal.show').length) {
            console.log('Periodic cleanup triggered');
            forceCleanupModal();
        }
    }, 5000);
}

// Token management functions
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
                loadTokensData();
                showAlert(response.message, 'success');
            } else {
                showAlert(response.message, 'danger');
            }
        },
        error: function(xhr, status, error) {
            console.error('Add tokens error:', status, error);
            if (status === 'timeout') {
                showAlert('Timeout khi thêm tokens! Vui lòng thử lại.', 'warning');
            } else {
                showAlert('Lỗi khi thêm tokens!', 'danger');
            }
        },
        complete: function() {
            // Always hide loading modal regardless of success or error
            hideLoadingModal();
        }
    });
}

function loadTokensData() {
    $.ajax({
        url: '/api/tokens',
        method: 'GET',
        success: function(response) {
            if (response.success) {
                tokensData = response.tokens;
                renderTokensTable();
                updateStatistics();
            }
        },
        error: function() {
            console.error('Error loading tokens data');
        }
    });
}

function renderTokensTable() {
    const tbody = $('#tokens-table-body');
    tbody.empty();
    
    if (tokensData.length === 0) {
        tbody.html(`
            <tr>
                <td colspan="6" class="text-center text-muted py-4">
                    <i class="fas fa-info-circle me-2"></i>
                    Chưa có token nào. Nhấn "➕ Nhập Token" để thêm token.
                </td>
            </tr>
        `);
        return;
    }
    
    tokensData.forEach(token => {
        const statusClass = getStatusClass(token.status);
        const statusBadge = getStatusBadge(token.status);
        const tokenDisplay = formatTokenDisplay(token.token);
        
        const row = $(`
            <tr class="${statusClass}" data-token-id="${token.id}">
                <td>
                    <input type="checkbox" class="form-check-input token-checkbox" value="${token.id}">
                </td>
                <td>${escapeHtml(token.account_name)}</td>
                <td>
                    <code class="font-monospace small">${tokenDisplay}</code>
                </td>
                <td>${statusBadge}</td>
                <td class="token-process">-</td>
                <td>
                    <button class="btn btn-sm btn-outline-info" onclick="showTokenDetails('${token.id}')">
                        <i class="fas fa-info-circle"></i>
                    </button>
                </td>
            </tr>
        `);
        
        tbody.append(row);
    });
}

function getStatusClass(status) {
    switch (status) {
        case 'LIVE': return 'token-status-live';
        case 'DIE': return 'token-status-die';
        default: return 'token-status-unchecked';
    }
}

function getStatusBadge(status) {
    switch (status) {
        case 'LIVE':
            return '<span class="badge status-live">LIVE</span>';
        case 'DIE':
            return '<span class="badge status-die">DIE</span>';
        default:
            return '<span class="badge status-unchecked">Chưa Check</span>';
    }
}

function formatTokenDisplay(token) {
    if (token.length <= 30) {
        return token.substring(0, 10) + '...' + token.substring(token.length - 5);
    }
    return token.substring(0, 15) + '...' + token.substring(token.length - 10);
}

function toggleAllTokens() {
    const checked = $('#select-all-tokens').is(':checked');
    $('.token-checkbox').prop('checked', checked);
}

function getSelectedTokenIds() {
    return $('.token-checkbox:checked').map(function() {
        return $(this).val();
    }).get();
}

function checkSelectedTokens() {
    const tokenIds = getSelectedTokenIds();
    if (tokenIds.length === 0) {
        showAlert('Vui lòng chọn ít nhất một token!', 'warning');
        return;
    }
    
    showLoadingModal('Đang kiểm tra tokens...', `Sẽ kiểm tra ${tokenIds.length} token`);
    
    $.ajax({
        url: '/api/tokens/check',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ token_ids: tokenIds }),
        timeout: 60000, // 60 second timeout for checking tokens
        success: function(response) {
            if (response.success) {
                addLog(response.message, 'info');
                // Note: hideLoadingModal will be called by WebSocket event
            } else {
                showAlert(response.message, 'danger');
            }
        },
        error: function(xhr, status, error) {
            console.error('Check tokens error:', status, error);
            if (status === 'timeout') {
                showAlert('Timeout khi kiểm tra tokens! Vui lòng thử lại.', 'warning');
            } else {
                showAlert('Lỗi khi kiểm tra tokens!', 'danger');
            }
        },
        complete: function() {
            // Fallback to hide modal after 5 seconds if WebSocket doesn't respond
            setTimeout(function() {
                hideLoadingModal();
            }, 5000);
        }
    });
}

function deleteTokens(action) {
    let tokenIds = [];
    let confirmMessage = '';
    
    switch (action) {
        case 'selected':
            tokenIds = getSelectedTokenIds();
            if (tokenIds.length === 0) {
                showAlert('Vui lòng chọn ít nhất một token!', 'warning');
                return;
            }
            confirmMessage = `Bạn có chắc muốn xóa ${tokenIds.length} token đã chọn?`;
            break;
        case 'all':
            confirmMessage = 'Bạn có chắc muốn xóa TẤT CẢ tokens?';
            break;
        case 'die':
            confirmMessage = 'Bạn có chắc muốn xóa tất cả tokens DIE?';
            break;
        case 'duplicates':
            confirmMessage = 'Bạn có chắc muốn xóa tokens trùng lặp?';
            break;
    }
    
    if (!confirm(confirmMessage)) return;
    
    showLoadingModal('Đang xóa tokens...', 'Vui lòng đợi');
    
    $.ajax({
        url: '/api/tokens/delete',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ action, token_ids: tokenIds }),
        timeout: 30000, // 30 second timeout
        success: function(response) {
            if (response.success) {
                loadTokensData();
                showAlert(response.message, 'success');
            } else {
                showAlert(response.message, 'danger');
            }
        },
        error: function(xhr, status, error) {
            console.error('Delete tokens error:', status, error);
            if (status === 'timeout') {
                showAlert('Timeout khi xóa tokens! Vui lòng thử lại.', 'warning');
            } else {
                showAlert('Lỗi khi xóa tokens!', 'danger');
            }
        },
        complete: function() {
            // Always hide loading modal
            hideLoadingModal();
        }
    });
}

// Image management functions
function setupFileDragDrop() {
    const dropzone = $('#upload-dropzone');
    
    dropzone.on('click', () => $('#images-input').click());
    
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

function previewSelectedFiles() {
    const files = $('#images-input')[0].files;
    const preview = $('#selected-files-preview');
    const list = $('#selected-files-list');
    
    if (files.length === 0) {
        preview.hide();
        return;
    }
    
    list.empty();
    preview.show();
    
    Array.from(files).forEach((file, index) => {
        if (file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const item = $(`
                    <div class="col-md-3 mb-2">
                        <div class="image-gallery-item">
                            <img src="${e.target.result}" alt="${file.name}">
                            <div class="image-overlay">
                                <small class="text-center">${file.name}</small>
                            </div>
                        </div>
                    </div>
                `);
                list.append(item);
            };
            reader.readAsDataURL(file);
        }
    });
}

function uploadImages() {
    const files = $('#images-input')[0].files;
    if (files.length === 0) {
        showAlert('Vui lòng chọn ít nhất một ảnh!', 'warning');
        return;
    }
    
    const formData = new FormData();
    Array.from(files).forEach(file => {
        formData.append('images', file);
    });
    
    showUploadProgress();
    
    $.ajax({
        url: '/api/upload',
        method: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        xhr: function() {
            const xhr = new window.XMLHttpRequest();
            xhr.upload.addEventListener('progress', function(evt) {
                if (evt.lengthComputable) {
                    const percentComplete = Math.round((evt.loaded / evt.total) * 100);
                    updateUploadProgress(percentComplete);
                }
            });
            return xhr;
        },
        timeout: 120000, // 2 minute timeout for large files
        success: function(response) {
            if (response.success) {
                $('#uploadImagesModal').modal('hide');
                $('#images-input').val('');
                $('#selected-files-preview').hide();
                loadImagesData();
                showAlert(response.message, 'success');
            } else {
                showAlert(response.message, 'danger');
            }
        },
        error: function(xhr, status, error) {
            console.error('Upload images error:', status, error);
            if (status === 'timeout') {
                showAlert('Timeout khi upload ảnh! File có thể quá lớn.', 'warning');
            } else {
                showAlert('Lỗi khi upload ảnh!', 'danger');
            }
        },
        complete: function() {
            // Always hide upload progress
            hideUploadProgress();
        }
    });
}

function showUploadProgress() {
    $('#upload-progress-container').show();
    $('#btn-upload-images').prop('disabled', true);
}

function hideUploadProgress() {
    $('#upload-progress-container').hide();
    $('#btn-upload-images').prop('disabled', false);
}

function updateUploadProgress(percent) {
    const progressBar = $('#upload-progress');
    progressBar.css('width', percent + '%');
    progressBar.text(percent + '%');
}

function loadImagesData() {
    $.ajax({
        url: '/api/images',
        method: 'GET',
        success: function(response) {
            if (response.success) {
                imagesData = response.images;
                renderImageGallery();
            }
        },
        error: function() {
            console.error('Error loading images data');
        }
    });
}

function renderImageGallery() {
    const gallery = $('#image-gallery');
    const content = $('#image-gallery-content');
    
    if (imagesData.length === 0) {
        gallery.hide();
        return;
    }
    
    content.empty();
    gallery.show();
    
    imagesData.forEach(image => {
        const item = $(`
            <div class="col-md-2 col-sm-3 col-4 mb-3">
                <div class="image-gallery-item">
                    <img src="${image.url}" alt="${image.filename}">
                    <div class="image-overlay">
                        <small class="text-center">${image.filename}</small>
                    </div>
                </div>
            </div>
        `);
        content.append(item);
    });
}

// Spam management functions
function startSpam() {
    // Validate inputs
    const postUIDs = $('#post-uids').val().trim();
    const comments = $('#comment-texts').val().trim();
    const minDelay = parseInt($('#min-delay').val());
    const maxDelay = parseInt($('#max-delay').val());
    const maxThreads = parseInt($('#max-threads').val());
    const numComments = parseInt($('#num-comments').val());
    const numImageComments = parseInt($('#num-image-comments').val());
    const autoLike = $('#auto-like').is(':checked');
    
    if (!postUIDs) {
        showAlert('Vui lòng nhập Post UID!', 'warning');
        return;
    }
    if (!comments) {
        showAlert('Vui lòng nhập nội dung comment!', 'warning');
        return;
    }
    if (minDelay >= maxDelay) {
        showAlert('Min Delay phải nhỏ hơn Max Delay!', 'warning');
        return;
    }
    if (numComments <= 0) {
        showAlert('Số comment phải lớn hơn 0!', 'warning');
        return;
    }
    
    const data = {
        post_uids: postUIDs,
        comments: comments,
        min_delay: minDelay,
        max_delay: maxDelay,
        max_threads: maxThreads,
        num_comments: numComments,
        num_image_comments: numImageComments,
        auto_like: autoLike
    };
    
    showLoadingModal('Đang bắt đầu spam...', 'Chuẩn bị các comment tasks');
    
    $.ajax({
        url: '/api/spam/start',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(data),
        timeout: 30000, // 30 second timeout
        success: function(response) {
            if (response.success) {
                showAlert(response.message, 'success');
                // Note: hideLoadingModal will be called by WebSocket 'spam_started' event
            } else {
                showAlert(response.message, 'danger');
            }
        },
        error: function(xhr, status, error) {
            console.error('Start spam error:', status, error);
            if (status === 'timeout') {
                showAlert('Timeout khi bắt đầu spam! Vui lòng thử lại.', 'warning');
            } else {
                showAlert('Lỗi khi bắt đầu spam!', 'danger');
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
    
    showLoadingModal('Đang dừng spam...', 'Hủy các task đang chạy');
    
    $.ajax({
        url: '/api/spam/stop',
        method: 'POST',
        timeout: 30000, // 30 second timeout
        success: function(response) {
            if (response.success) {
                showAlert(response.message, 'success');
                // Note: hideLoadingModal will be called by WebSocket 'spam_stopped' event
            } else {
                showAlert(response.message, 'warning');
            }
        },
        error: function(xhr, status, error) {
            console.error('Stop spam error:', status, error);
            if (status === 'timeout') {
                showAlert('Timeout khi dừng spam! Vui lòng thử lại.', 'warning');
            } else {
                showAlert('Lỗi khi dừng spam!', 'danger');
            }
        },
        complete: function() {
            // Fallback to hide modal after 5 seconds
            setTimeout(function() {
                hideLoadingModal();
            }, 5000);
        }
    });
}

function updateSpamUI() {
    if (spamStatus.is_running) {
        $('#btn-start-spam').prop('disabled', true);
        $('#btn-stop-spam').prop('disabled', false);
        $('#tool-status').text('Đang Chạy');
        updateStatusAlert('Tool đang chạy...', 'warning');
    } else {
        $('#btn-start-spam').prop('disabled', false);
        $('#btn-stop-spam').prop('disabled', true);
        $('#tool-status').text('Sẵn Sàng');
        updateStatusAlert('Tool đã sẵn sàng chạy', 'success');
    }
}

function updateSpamProgress(current, total) {
    const percent = total > 0 ? Math.round((current / total) * 100) : 0;
    const progressBar = $('#spam-progress');
    
    progressBar.css('width', percent + '%');
    progressBar.text(`${current}/${total}`);
    
    $('#progress-text').text(`📊 Comment ${current}/${total}`);
}



// Auto fetch page names
function handleUIDChange() {
    const element = $(this);
    const value = element.val().trim();
    
    if (!value) return;
    
    // Simple debounce
    clearTimeout(element.data('timeout'));
    element.data('timeout', setTimeout(() => {
        fetchPageNames(element);
    }, 1000));
}

function fetchPageNames(element) {
    const lines = element.val().split('\n');
    const updatedLines = [];
    let hasChanges = false;
    
    lines.forEach(line => {
        const trimmedLine = line.trim();
        if (trimmedLine && !trimmedLine.includes(' (')) {
            // Fetch page name for this UID
            $.ajax({
                url: '/api/page-info',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ post_uid: trimmedLine }),
                success: function(response) {
                    if (response.success && response.page_name) {
                        const currentValue = element.val();
                        const newValue = currentValue.replace(trimmedLine, response.formatted_uid);
                        element.val(newValue);
                    }
                }
            });
        }
    });
}

// Utility functions
function showAlert(message, type = 'info') {
    const alertClass = `alert-${type}`;
    const iconClass = {
        'success': 'fas fa-check-circle',
        'danger': 'fas fa-exclamation-triangle',
        'warning': 'fas fa-exclamation-triangle',
        'info': 'fas fa-info-circle'
    }[type] || 'fas fa-info-circle';
    
    const alert = $(`
        <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
            <i class="${iconClass} me-2"></i>
            ${escapeHtml(message)}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `);
    
    $('#alert-container').append(alert);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        alert.alert('close');
    }, 5000);
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
        }, 100); // Reduce timeout to 100ms for faster cleanup
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
        
        // Force show emergency cleanup button
        $('#emergency-cleanup').show();
        
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

function updateLoadingModal(title, detail = '') {
    $('#loading-text').text(title);
    $('#loading-detail').text(detail);
}

function addLog(message, type = 'info') {
    const timestamp = new Date().toLocaleTimeString();
    const logClass = `log-${type}`;
    const iconClass = {
        'success': 'fas fa-check',
        'error': 'fas fa-times',
        'warning': 'fas fa-exclamation-triangle',
        'info': 'fas fa-info-circle'
    }[type] || 'fas fa-info-circle';
    
    const logEntry = $(`
        <div class="log-entry ${logClass}">
            <span class="log-timestamp">[${timestamp}]</span>
            <i class="${iconClass} ms-2 me-1"></i>
            ${escapeHtml(message)}
        </div>
    `);
    
    const container = $('#logs-container');
    container.append(logEntry);
    container.scrollTop(container[0].scrollHeight);
}

function clearLogs() {
    if (confirm('Bạn có chắc muốn xóa tất cả logs?')) {
        $('#logs-container').empty();
        addLog('Logs đã được xóa', 'info');
    }
}

function updateStatistics() {
    const stats = {
        total: tokensData.length,
        live: tokensData.filter(t => t.status === 'LIVE').length,
        die: tokensData.filter(t => t.status === 'DIE').length,
        unchecked: tokensData.filter(t => t.status === 'Chưa Check').length
    };
    
    $('#total-tokens').text(stats.total);
    $('#live-tokens').text(stats.live);
}

function updateStatusAlert(message, type) {
    const alertClass = `alert-${type}`;
    const iconClass = {
        'success': 'fas fa-check-circle',
        'warning': 'fas fa-exclamation-triangle',
        'danger': 'fas fa-times-circle'
    }[type] || 'fas fa-info-circle';
    
    const alert = $('#status-alert');
    alert.removeClass('alert-success alert-warning alert-danger alert-info')
         .addClass(alertClass);
    alert.html(`<i class="${iconClass} me-2"></i><strong>${message}</strong>`);
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatDuration(seconds) {
    if (seconds < 60) {
        return `${seconds.toFixed(1)} giây`;
    } else if (seconds < 3600) {
        return `${(seconds / 60).toFixed(1)} phút`;
    } else {
        return `${(seconds / 3600).toFixed(1)} giờ`;
    }
}

function startAutoRefresh() {
    // Refresh data every 30 seconds
    autoRefreshInterval = setInterval(() => {
        if (!spamStatus.is_running) {
            loadTokensData();
        }
    }, 30000);
}

function stopAutoRefresh() {
    if (autoRefreshInterval) {
        clearInterval(autoRefreshInterval);
        autoRefreshInterval = null;
    }
}

// Show token details modal
function showTokenDetails(tokenId) {
    const token = tokensData.find(t => t.id === tokenId);
    if (!token) return;
    
    $('#token-account-name').text(token.account_name);
    $('#token-status').html(getStatusBadge(token.status));
    $('#token-display').val(formatTokenDisplay(token.token));
    $('#token-added-time').text(new Date(token.added_at * 1000).toLocaleString());
    
    $('#tokenDetailsModal').modal('show');
}

// Copy token function
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showAlert('Đã copy vào clipboard!', 'success');
    }).catch(() => {
        showAlert('Lỗi khi copy!', 'danger');
    });
}

// Page visibility change handler
document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
        // Page is hidden, reduce activity
        stopAutoRefresh();
    } else {
        // Page is visible, resume activity
        if (!autoRefreshInterval) {
            startAutoRefresh();
        }
    }
});

// Cleanup on page unload
window.addEventListener('beforeunload', function() {
    stopAutoRefresh();
    if (socket) {
        socket.disconnect();
    }
});
