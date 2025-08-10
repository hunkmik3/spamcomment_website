# -*- coding: utf-8 -*-
"""
Token Manager - Quản lý tokens và rate limiting
@origin 250724-01 (Plants1.3)
"""

import time
import threading
from collections import defaultdict
from typing import List, Tuple, Optional
from utils.facebook_api import FacebookAPI


class TokenManager:
    """Quản lý tokens và rate limiting"""
    
    def __init__(self):
        self.rate_limit = 100
        self.rate_limit_window = 3600  # 1 giờ
        self.token_usage = defaultdict(lambda: {"count": 0, "last_reset": time.time()})
        self.token_comment_count = defaultdict(int)
        self.available_tokens = []
        self.token_index = 0
        self.lock = threading.Lock()

    def can_use_token(self, token: str) -> bool:
        """Kiểm tra token có thể sử dụng không"""
        usage = self.token_usage[token]
        current_time = time.time()
        if current_time - usage["last_reset"] > self.rate_limit_window:
            usage["count"] = 0
            usage["last_reset"] = current_time
        return usage["count"] < self.rate_limit

    def use_token(self, token: str):
        """Sử dụng token (tăng counter)"""
        self.token_usage[token]["count"] += 1

    def get_token_from_queue(self) -> Tuple[Optional[str], Optional[int]]:
        """Lấy token từ queue"""
        with self.lock:
            if not self.available_tokens:
                return None, None
            if self.token_index >= len(self.available_tokens):
                self.token_index = 0
            token, row = self.available_tokens[self.token_index]
            self.token_index = (self.token_index + 1) % len(self.available_tokens)
            return token, row

    def update_available_tokens(self, tokens_with_rows: List[Tuple[str, int]]):
        """Cập nhật danh sách token khả dụng"""
        with self.lock:
            self.available_tokens = tokens_with_rows

    def remove_token(self, token: str):
        """Xóa token khỏi danh sách khả dụng"""
        with self.lock:
            self.available_tokens = [(t, r) for (t, r) in self.available_tokens if t != token]

    def increment_comment_count(self, token: str):
        """Tăng số comment đã gửi cho token"""
        self.token_comment_count[token] += 1

    def get_comment_count(self, token: str) -> int:
        """Lấy số comment đã gửi của token"""
        return self.token_comment_count.get(token, 0)

    def check_tokens_status(self, tokens: List[str]) -> List[Tuple[str, str]]:
        """Kiểm tra trạng thái nhiều token"""
        results = []
        for token in tokens:
            status, account_name = FacebookAPI.check_token_status(token)
            results.append((status, account_name))
        return results 