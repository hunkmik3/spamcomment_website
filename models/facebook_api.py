# -*- coding: utf-8 -*-
"""
Facebook API utilities for Web App
@origin 250724-01 (Plants1.3)
"""

import os
import requests
import tempfile
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class WebFacebookAPI:
    """Class xử lý các API call đến Facebook cho web environment"""
    
    @staticmethod
    def fetch_page_name(token: str, uid: str) -> Optional[str]:
        """Lấy tên page từ UID"""
        # Extract clean UID if it contains page name already
        clean_uid = uid.split(" (")[0] if " (" in uid else uid
        
        url = f"https://graph.facebook.com/{clean_uid}?fields=from&access_token={token}"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if "from" in data and "name" in data["from"]:
                    return data["from"]["name"]
            logger.warning(f"Could not fetch page name for UID: {clean_uid}")
            return None
        except Exception as e:
            logger.error(f"Error fetching page name: {e}")
            return None

    @staticmethod
    def comment_text_only(post_id: str, token: str, message: str) -> Tuple[bool, Optional[str]]:
        """Comment chỉ text"""
        # Extract clean post ID
        clean_post_id = post_id.split(" (")[0] if " (" in post_id else post_id
        
        url = f"https://graph.facebook.com/{clean_post_id}/comments"
        data = {"access_token": token, "message": message}
        
        try:
            response = requests.post(url, data=data, timeout=30)
            if response.status_code == 200:
                json_data = response.json()
                comment_id = json_data.get("id")
                if comment_id:
                    logger.info(f"Comment sent successfully: {comment_id}")
                    return True, comment_id
            
            logger.warning(f"Comment failed with status: {response.status_code}")
            return False, None
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request exception in comment_text_only: {e}")
            return False, None

    @staticmethod
    def upload_image_to_facebook(token: str, image_path: str) -> Optional[str]:
        """Upload ảnh lên Facebook"""
        url = "https://graph.facebook.com/me/photos"
        
        try:
            if not os.path.exists(image_path):
                logger.error(f"Image file not found: {image_path}")
                return None
                
            with open(image_path, 'rb') as f:
                files = {'source': f}
                data = {'access_token': token, 'published': 'false'}
                response = requests.post(url, files=files, data=data, timeout=60)
                
            if response.status_code == 200:
                json_data = response.json()
                photo_id = json_data.get("id")
                if photo_id:
                    logger.info(f"Image uploaded successfully: {photo_id}")
                    return photo_id
                    
            logger.warning(f"Image upload failed with status: {response.status_code}")
            return None
            
        except Exception as e:
            logger.error(f"Error uploading image: {e}")
            return None

    @staticmethod
    def comment_with_image(post_id: str, token: str, message: str, photo_id: str) -> Tuple[bool, Optional[str]]:
        """Comment với ảnh"""
        # Extract clean post ID
        clean_post_id = post_id.split(" (")[0] if " (" in post_id else post_id
        
        url = f"https://graph.facebook.com/{clean_post_id}/comments"
        data = {
            "access_token": token, 
            "message": message, 
            "attachment_id": photo_id
        }
        
        try:
            response = requests.post(url, data=data, timeout=30)
            if response.status_code == 200:
                json_data = response.json()
                comment_id = json_data.get("id")
                if comment_id:
                    logger.info(f"Comment with image sent successfully: {comment_id}")
                    return True, comment_id
                    
            logger.warning(f"Comment with image failed with status: {response.status_code}")
            return False, None
            
        except Exception as e:
            logger.error(f"Error in comment_with_image: {e}")
            return False, None

    @staticmethod
    def like_post(token: str, post_id: str) -> bool:
        """Like bài viết"""
        # Extract clean post ID
        clean_post_id = post_id.split(" (")[0] if " (" in post_id else post_id
        
        url = f"https://graph.facebook.com/{clean_post_id}/likes"
        data = {"access_token": token}
        
        try:
            response = requests.post(url, data=data, timeout=30)
            success = response.status_code == 200
            if success:
                logger.info(f"Post liked successfully: {clean_post_id}")
            else:
                logger.warning(f"Like failed with status: {response.status_code}")
            return success
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error liking post: {e}")
            return False

    @staticmethod
    def uncomment_comment(token: str, comment_id: str) -> bool:
        """Gỡ comment"""
        url = f"https://graph.facebook.com/{comment_id}"
        params = {"access_token": token}
        
        try:
            response = requests.delete(url, params=params, timeout=30)
            if response.status_code == 200:
                resp_data = response.json()
                success = resp_data is True
                if success:
                    logger.info(f"Comment deleted successfully: {comment_id}")
                return success
                
            logger.warning(f"Delete comment failed with status: {response.status_code}")
            return False
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error deleting comment: {e}")
            return False

    @staticmethod
    def check_token_status(token: str) -> Tuple[str, str]:
        """Kiểm tra trạng thái token"""
        url = f"https://graph.facebook.com/me?access_token={token}"
        
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                account_name = data.get("name", "Unknown")
                logger.info(f"Token is LIVE for account: {account_name}")
                return "LIVE", account_name
            else:
                logger.warning(f"Token check failed with status: {response.status_code}")
                return "DIE", "Unknown"
                
        except Exception as e:
            logger.error(f"Error checking token: {e}")
            return "DIE", "Unknown"

    @staticmethod
    def upload_image_from_bytes(token: str, image_bytes: bytes, filename: str) -> Optional[str]:
        """Upload ảnh từ bytes data (cho web upload)"""
        url = "https://graph.facebook.com/me/photos"
        
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as temp_file:
                temp_file.write(image_bytes)
                temp_path = temp_file.name
            
            # Upload using temporary file
            photo_id = WebFacebookAPI.upload_image_to_facebook(token, temp_path)
            
            # Clean up temporary file
            try:
                os.unlink(temp_path)
            except:
                pass
                
            return photo_id
            
        except Exception as e:
            logger.error(f"Error uploading image from bytes: {e}")
            return None
