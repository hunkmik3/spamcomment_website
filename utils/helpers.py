# -*- coding: utf-8 -*-
"""
Helper utilities for Facebook Spam Tool
@origin 250724-01 (Plants1.3)
"""

import uuid
import time
from typing import Optional


def allowed_file(filename: str) -> bool:
    """Kiểm tra file có được phép upload không"""
    if not filename:
        return False
    
    allowed_extensions = {'jpg', 'jpeg', 'png', 'gif', 'webp'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


def generate_session_id() -> str:
    """Tạo session ID unique"""
    return str(uuid.uuid4())


def format_time_duration(seconds: float) -> str:
    """Format thời gian thành chuỗi dễ đọc"""
    if seconds < 60:
        return f"{seconds:.1f} giây"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f} phút"
    else:
        hours = seconds / 3600
        return f"{hours:.1f} giờ"


def extract_clean_uid(uid_string: str) -> str:
    """Trích xuất UID sạch từ chuỗi có thể chứa tên page"""
    return uid_string.split(" (")[0] if " (" in uid_string else uid_string


def validate_facebook_token(token: str) -> bool:
    """Kiểm tra format cơ bản của Facebook token"""
    if not token or len(token) < 50:
        return False
    
    # Facebook tokens usually start with specific prefixes
    valid_prefixes = ['EAAG', 'EAAg', 'EAAB', 'EAAb']
    return any(token.startswith(prefix) for prefix in valid_prefixes)


def sanitize_filename(filename: str) -> str:
    """Làm sạch tên file để tránh lỗi security"""
    import re
    # Remove any path separators and special chars
    filename = re.sub(r'[/\\:*?"<>|]', '', filename)
    # Limit length
    if len(filename) > 100:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        filename = name[:95] + ('.' + ext if ext else '')
    return filename


def get_file_size_mb(filepath: str) -> float:
    """Lấy kích thước file theo MB"""
    try:
        import os
        size_bytes = os.path.getsize(filepath)
        return size_bytes / (1024 * 1024)
    except:
        return 0.0


def is_valid_post_uid(uid: str) -> bool:
    """Kiểm tra UID post có hợp lệ không"""
    clean_uid = extract_clean_uid(uid)
    if not clean_uid:
        return False
    
    # Basic validation - Facebook post UIDs are typically numeric or contain underscores
    import re
    pattern = r'^[0-9_]+$'
    return bool(re.match(pattern, clean_uid))


def truncate_text(text: str, max_length: int = 100) -> str:
    """Cắt ngắn text với dấu ..."""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."


def format_token_display(token: str) -> str:
    """Format token để hiển thị an toàn"""
    if len(token) <= 30:
        return token[:10] + "..." + token[-5:]
    return token[:15] + "..." + token[-10:]


class RateLimiter:
    """Simple rate limiter class"""
    
    def __init__(self, max_calls: int, window_seconds: int):
        self.max_calls = max_calls
        self.window_seconds = window_seconds
        self.calls = []
    
    def can_proceed(self) -> bool:
        """Kiểm tra có thể thực hiện call không"""
        now = time.time()
        
        # Remove old calls outside window
        self.calls = [call_time for call_time in self.calls 
                     if now - call_time < self.window_seconds]
        
        return len(self.calls) < self.max_calls
    
    def record_call(self):
        """Ghi lại một call"""
        self.calls.append(time.time())


def parse_delay_input(delay_str: str) -> Optional[int]:
    """Parse input delay string thành milliseconds"""
    try:
        delay = int(delay_str.strip())
        if delay < 0:
            return None
        return delay
    except (ValueError, AttributeError):
        return None


def validate_comment_text(text: str) -> tuple[bool, str]:
    """Validate comment text"""
    if not text or not text.strip():
        return False, "Comment không được để trống"
    
    text = text.strip()
    
    if len(text) > 8000:  # Facebook comment limit
        return False, "Comment quá dài (tối đa 8000 ký tự)"
    
    # Check for potentially harmful content
    suspicious_patterns = ['<script', 'javascript:', 'data:']
    text_lower = text.lower()
    for pattern in suspicious_patterns:
        if pattern in text_lower:
            return False, "Comment chứa nội dung không được phép"
    
    return True, "OK"


def get_image_path(session_id: str, filename: str, upload_folder: str) -> str:
    """Get full path to uploaded image"""
    import os
    return os.path.join(upload_folder, session_id, filename)


def delete_image_file(filepath: str) -> bool:
    """Delete image file safely"""
    try:
        import os
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False
    except Exception:
        return False
