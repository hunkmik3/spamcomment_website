# -*- coding: utf-8 -*-
"""
Token Manager for Web App - Quản lý tokens và rate limiting
@origin 250724-01 (Plants1.3)
"""

import time
import uuid
import threading
from collections import defaultdict
from typing import List, Dict, Tuple, Optional, Any
import logging

from .facebook_api import WebFacebookAPI

logger = logging.getLogger(__name__)


class WebTokenManager:
    """Quản lý tokens và rate limiting cho web environment"""
    
    def __init__(self, session_id=None):
        # Rate limiting configuration
        self.rate_limit = 100  # comments per hour
        self.rate_limit_window = 3600  # 1 hour in seconds
        
        # Data storage - organized by session
        self.sessions = defaultdict(lambda: {
            'tokens': {},  # token_id: token_data
            'token_usage': defaultdict(lambda: {"count": 0, "last_reset": time.time()}),
            'token_comment_count': defaultdict(int),
            'available_tokens': [],  # List of available token IDs
            'token_index': 0
        })
        
        # Thread safety
        self.lock = threading.Lock()
        
        # Legacy compatibility
        self.session_id = session_id

    def _get_session_data(self, session_id: str) -> Dict:
        """Lấy data của session"""
        return self.sessions[session_id]

    def add_tokens(self, session_id: str, tokens: List[str]) -> int:
        """Thêm tokens mới vào session"""
        with self.lock:
            session_data = self._get_session_data(session_id)
            added_count = 0
            
            for token in tokens:
                token = token.strip()
                if not token:
                    continue
                    
                # Check if token already exists
                existing = False
                for existing_token_data in session_data['tokens'].values():
                    if existing_token_data['token'] == token:
                        existing = True
                        break
                
                if not existing:
                    token_id = str(uuid.uuid4())
                    session_data['tokens'][token_id] = {
                        'id': token_id,
                        'token': token,
                        'account_name': 'Unknown',
                        'status': 'Chưa Check',
                        'added_at': time.time()
                    }
                    added_count += 1
            
            logger.info(f"Added {added_count} tokens to session {session_id}")
            return added_count

    def get_tokens(self, session_id: str) -> List[Dict]:
        """Lấy danh sách tokens của session"""
        session_data = self._get_session_data(session_id)
        return list(session_data['tokens'].values())

    def delete_tokens(self, session_id: str, token_ids: List[str]) -> int:
        """Xóa tokens được chỉ định"""
        with self.lock:
            session_data = self._get_session_data(session_id)
            deleted_count = 0
            
            for token_id in token_ids:
                if token_id in session_data['tokens']:
                    del session_data['tokens'][token_id]
                    deleted_count += 1
            
            # Update available tokens list
            session_data['available_tokens'] = [
                tid for tid in session_data['available_tokens'] 
                if tid not in token_ids
            ]
            
            logger.info(f"Deleted {deleted_count} tokens from session {session_id}")
            return deleted_count

    def delete_all_tokens(self, session_id: str) -> int:
        """Xóa tất cả tokens"""
        with self.lock:
            session_data = self._get_session_data(session_id)
            count = len(session_data['tokens'])
            
            session_data['tokens'].clear()
            session_data['available_tokens'].clear()
            session_data['token_usage'].clear()
            session_data['token_comment_count'].clear()
            
            logger.info(f"Deleted all {count} tokens from session {session_id}")
            return count

    def delete_die_tokens(self, session_id: str) -> int:
        """Xóa tokens có status DIE"""
        with self.lock:
            session_data = self._get_session_data(session_id)
            die_token_ids = []
            
            for token_id, token_data in session_data['tokens'].items():
                if token_data['status'] == 'DIE':
                    die_token_ids.append(token_id)
            
            return self.delete_tokens(session_id, die_token_ids)

    def delete_duplicate_tokens(self, session_id: str) -> int:
        """Xóa tokens trùng lặp"""
        with self.lock:
            session_data = self._get_session_data(session_id)
            seen_tokens = {}
            duplicate_ids = []
            
            for token_id, token_data in session_data['tokens'].items():
                token = token_data['token']
                if token in seen_tokens:
                    duplicate_ids.append(token_id)
                else:
                    seen_tokens[token] = token_id
            
            return self.delete_tokens(session_id, duplicate_ids)

    def check_tokens_status(self, session_id: str, token_ids: List[str], socketio=None) -> List[Dict]:
        """Kiểm tra trạng thái tokens"""
        session_data = self._get_session_data(session_id)
        results = []
        
        for i, token_id in enumerate(token_ids):
            if token_id not in session_data['tokens']:
                continue
                
            token_data = session_data['tokens'][token_id]
            token = token_data['token']
            
            # Send progress update via websocket
            if socketio:
                socketio.emit('token_check_progress', {
                    'current': i + 1,
                    'total': len(token_ids),
                    'token_id': token_id
                }, room=session_id)
            
            status, account_name = WebFacebookAPI.check_token_status(token)
            
            # Update token data
            with self.lock:
                session_data['tokens'][token_id]['status'] = status
                session_data['tokens'][token_id]['account_name'] = account_name
                session_data['tokens'][token_id]['last_checked'] = time.time()
            
            results.append({
                'token_id': token_id,
                'status': status,
                'account_name': account_name
            })
            
        # Update available tokens list after checking
        self._update_available_tokens(session_id)
        
        logger.info(f"Checked {len(results)} tokens for session {session_id}")
        return results

    def _update_available_tokens(self, session_id: str):
        """Cập nhật danh sách tokens khả dụng"""
        session_data = self._get_session_data(session_id)
        available = []
        
        for token_id, token_data in session_data['tokens'].items():
            if token_data['status'] == 'LIVE':
                available.append(token_id)
        
        session_data['available_tokens'] = available
        session_data['token_index'] = 0

    def has_available_tokens(self, session_id: str) -> bool:
        """Kiểm tra có tokens khả dụng không"""
        self._update_available_tokens(session_id)
        session_data = self._get_session_data(session_id)
        return len(session_data['available_tokens']) > 0

    def get_available_token(self, session_id: str) -> Optional[Dict]:
        """Lấy token khả dụng từ queue"""
        with self.lock:
            session_data = self._get_session_data(session_id)
            
            if not session_data['available_tokens']:
                self._update_available_tokens(session_id)
                
            if not session_data['available_tokens']:
                return None
            
            # Round-robin selection
            if session_data['token_index'] >= len(session_data['available_tokens']):
                session_data['token_index'] = 0
                
            token_id = session_data['available_tokens'][session_data['token_index']]
            session_data['token_index'] = (session_data['token_index'] + 1) % len(session_data['available_tokens'])
            
            return session_data['tokens'][token_id]

    def can_use_token(self, session_id: str, token_id: str) -> bool:
        """Kiểm tra token có thể sử dụng không (rate limiting)"""
        session_data = self._get_session_data(session_id)
        
        if token_id not in session_data['tokens']:
            return False
            
        token = session_data['tokens'][token_id]['token']
        usage = session_data['token_usage'][token]
        current_time = time.time()
        
        # Reset counter if window expired
        if current_time - usage["last_reset"] > self.rate_limit_window:
            usage["count"] = 0
            usage["last_reset"] = current_time
            
        return usage["count"] < self.rate_limit

    def use_token(self, session_id: str, token_id: str):
        """Sử dụng token (tăng counter)"""
        session_data = self._get_session_data(session_id)
        
        if token_id not in session_data['tokens']:
            return
            
        token = session_data['tokens'][token_id]['token']
        
        with self.lock:
            session_data['token_usage'][token]["count"] += 1
            session_data['token_comment_count'][token] += 1

    def get_comment_count(self, session_id: str, token_id: str) -> int:
        """Lấy số comment đã gửi của token"""
        session_data = self._get_session_data(session_id)
        
        if token_id not in session_data['tokens']:
            return 0
            
        token = session_data['tokens'][token_id]['token']
        return session_data['token_comment_count'].get(token, 0)

    def mark_token_dead(self, session_id: str, token_id: str):
        """Đánh dấu token chết"""
        with self.lock:
            session_data = self._get_session_data(session_id)
            
            if token_id in session_data['tokens']:
                session_data['tokens'][token_id]['status'] = 'DIE'
                
                # Remove from available tokens
                if token_id in session_data['available_tokens']:
                    session_data['available_tokens'].remove(token_id)
                    
                logger.warning(f"Marked token {token_id} as DIE in session {session_id}")

    def get_session_stats(self, session_id: str) -> Dict:
        """Lấy thống kê của session"""
        session_data = self._get_session_data(session_id)
        
        total_tokens = len(session_data['tokens'])
        live_tokens = sum(1 for t in session_data['tokens'].values() if t['status'] == 'LIVE')
        die_tokens = sum(1 for t in session_data['tokens'].values() if t['status'] == 'DIE')
        unchecked_tokens = sum(1 for t in session_data['tokens'].values() if t['status'] == 'Chưa Check')
        
        total_comments = sum(session_data['token_comment_count'].values())
        
        return {
            'total_tokens': total_tokens,
            'live_tokens': live_tokens,
            'die_tokens': die_tokens,
            'unchecked_tokens': unchecked_tokens,
            'available_tokens': len(session_data['available_tokens']),
            'total_comments': total_comments
        }

    def cleanup_old_sessions(self, max_age_hours: int = 24):
        """Dọn dẹp sessions cũ"""
        with self.lock:
            current_time = time.time()
            old_sessions = []
            
            for session_id, session_data in self.sessions.items():
                # Check if session has any recent activity
                has_recent_activity = False
                for token_data in session_data['tokens'].values():
                    if current_time - token_data.get('added_at', 0) < max_age_hours * 3600:
                        has_recent_activity = True
                        break
                
                if not has_recent_activity and session_data['tokens']:
                    old_sessions.append(session_id)
            
            for session_id in old_sessions:
                del self.sessions[session_id]
                logger.info(f"Cleaned up old session: {session_id}")
                
            return len(old_sessions)
