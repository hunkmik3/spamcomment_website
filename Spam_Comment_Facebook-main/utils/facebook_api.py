# -*- coding: utf-8 -*-
"""
Facebook API utilities
@origin 250724-01 (Plants1.3)
"""

import os
import requests
from typing import Tuple, Optional


class FacebookAPI:
    """Class xử lý các API call đến Facebook"""
    
    @staticmethod
    def fetch_page_name(token: str, uid: str) -> Optional[str]:
        """Lấy tên page từ UID"""
        url = f"https://graph.facebook.com/{uid}?fields=from&access_token={token}"
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                data = r.json()
                if "from" in data and "name" in data["from"]:
                    return data["from"]["name"]
            return None
        except Exception:
            return None

    @staticmethod
    def comment_text_only(post_id: str, token: str, message: str) -> Tuple[bool, Optional[str]]:
        """Comment chỉ text"""
        url = f"https://graph.facebook.com/{post_id}/comments"
        data = {"access_token": token, "message": message}
        try:
            r = requests.post(url, data=data, timeout=30)
            if r.status_code == 200:
                j = r.json()
                c_id = j.get("id")
                if c_id:
                    return True, c_id
            return False, None
        except requests.exceptions.RequestException:
            return False, None

    @staticmethod
    def upload_image_to_facebook(token: str, image_path: str) -> Optional[str]:
        """Upload ảnh lên Facebook"""
        url = "https://graph.facebook.com/me/photos"
        try:
            with open(image_path, 'rb') as f:
                files = {'source': f}
                data = {'access_token': token, 'published': 'false'}
                resp = requests.post(url, files=files, data=data, timeout=60)
            if resp.status_code == 200:
                j = resp.json()
                photo_id = j.get("id")
                if photo_id:
                    return photo_id
            return None
        except Exception:
            return None

    @staticmethod
    def comment_with_image(post_id: str, token: str, message: str, photo_id: str) -> Tuple[bool, Optional[str]]:
        """Comment với ảnh"""
        url = f"https://graph.facebook.com/{post_id}/comments"
        data = {"access_token": token, "message": message, "attachment_id": photo_id}
        try:
            r = requests.post(url, data=data, timeout=30)
            if r.status_code == 200:
                j = r.json()
                c_id = j.get("id")
                if c_id:
                    return True, c_id
            return False, None
        except Exception:
            return False, None

    @staticmethod
    def like_post(token: str, post_id: str) -> bool:
        """Like bài viết"""
        url = f"https://graph.facebook.com/{post_id}/likes"
        data = {"access_token": token}
        try:
            r = requests.post(url, data=data, timeout=30)
            return r.status_code == 200
        except requests.exceptions.RequestException:
            return False

    @staticmethod
    def uncomment_comment(token: str, comment_id: str) -> bool:
        """Gỡ comment"""
        url = f"https://graph.facebook.com/{comment_id}"
        params = {"access_token": token}
        try:
            r = requests.delete(url, params=params, timeout=30)
            if r.status_code == 200:
                resp_data = r.json()
                return resp_data is True
            return False
        except requests.exceptions.RequestException:
            return False

    @staticmethod
    def check_token_status(token: str) -> Tuple[str, str]:
        """Kiểm tra trạng thái token"""
        url = f"https://graph.facebook.com/me?access_token={token}"
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                data = r.json()
                account_name = data.get("name", "Unknown")
                return "LIVE", account_name
            else:
                return "DIE", "Unknown"
        except:
            return "DIE", "Unknown" 