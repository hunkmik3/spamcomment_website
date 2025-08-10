# -*- coding: utf-8 -*-
"""
Spam Manager for Web App - Quản lý spam comments
@origin 250724-01 (Plants1.3)
"""

import os
import time
import random
import threading
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
from typing import List, Dict, Optional, Any
import logging

from .facebook_api import WebFacebookAPI

logger = logging.getLogger(__name__)


class SpamManager:
    """Quản lý spam comments cho web environment"""
    
    def __init__(self, socketio, token_manager):
        self.socketio = socketio
        self.token_manager = token_manager
        
        # Session-based spam status
        self.spam_sessions = defaultdict(lambda: {
            'is_running': False,
            'stop_event': threading.Event(),
            'executor': None,
            'futures': [],
            'stats': {
                'comments_sent': 0,
                'total_comments': 0,
                'start_time': None,
                'errors': 0
            },
            'current_settings': {}
        })
        
        # Thread safety
        self.lock = threading.Lock()

    def _get_spam_session(self, session_id: str) -> Dict:
        """Lấy spam session data"""
        return self.spam_sessions[session_id]

    def start_spam(self, session_id: str, post_uids: List[str], comments: List[str], settings: Dict) -> bool:
        """Bắt đầu spam comments"""
        with self.lock:
            spam_session = self._get_spam_session(session_id)
            
            if spam_session['is_running']:
                logger.warning(f"Spam already running for session {session_id}")
                return False
            
            # Validate settings
            try:
                min_delay = settings['min_delay']
                max_delay = settings['max_delay'] 
                max_threads = settings['max_threads']
                num_comments = settings['num_comments']
                num_image_comments = settings['num_image_comments']
                auto_like = settings['auto_like']
                
                if min_delay >= max_delay:
                    raise ValueError("Min delay must be less than max delay")
                if num_comments <= 0:
                    raise ValueError("Number of comments must be > 0")
                if max_threads <= 0:
                    raise ValueError("Max threads must be > 0")
                    
            except (KeyError, ValueError) as e:
                logger.error(f"Invalid settings: {e}")
                return False
            
            # Check if we have available tokens
            if not self.token_manager.has_available_tokens(session_id):
                logger.error(f"No available tokens for session {session_id}")
                return False
            
            # Clean post UIDs
            clean_post_uids = []
            for uid in post_uids:
                clean_uid = uid.split(" (")[0] if " (" in uid else uid
                clean_post_uids.append(clean_uid)
            
            # Initialize spam session
            spam_session['is_running'] = True
            spam_session['stop_event'].clear()
            spam_session['stats'] = {
                'comments_sent': 0,
                'total_comments': len(clean_post_uids) * num_comments,
                'start_time': time.time(),
                'errors': 0
            }
            spam_session['current_settings'] = settings.copy()
            
            # Start spam in background thread
            threading.Thread(
                target=self._run_spam_background,
                args=(session_id, clean_post_uids, comments, settings),
                daemon=True
            ).start()
            
            logger.info(f"Started spam for session {session_id}")
            return True

    def _run_spam_background(self, session_id: str, post_uids: List[str], comments: List[str], settings: Dict):
        """Chạy spam trong background thread"""
        spam_session = self._get_spam_session(session_id)
        
        try:
            # Extract settings
            min_delay = settings['min_delay']
            max_delay = settings['max_delay']
            max_threads = settings['max_threads']
            num_comments = settings['num_comments']
            num_image_comments = settings['num_image_comments']
            auto_like = settings['auto_like']
            
            # Create thread pool
            spam_session['executor'] = ThreadPoolExecutor(max_workers=max_threads)
            spam_session['futures'] = []
            
            # Send start notification
            self.socketio.emit('spam_started', {
                'total_comments': spam_session['stats']['total_comments'],
                'posts': len(post_uids)
            }, room=session_id)
            
            # Process each post
            for post_index, post_uid in enumerate(post_uids):
                if spam_session['stop_event'].is_set():
                    break
                
                # Determine which comments should have images
                image_indices = set(random.sample(range(num_comments), 
                                                min(num_image_comments, num_comments)))
                
                # Submit comment tasks
                for comment_index in range(num_comments):
                    if spam_session['stop_event'].is_set():
                        break
                    
                    comment_text = comments[comment_index % len(comments)]
                    with_image = comment_index in image_indices
                    
                    future = spam_session['executor'].submit(
                        self._process_comment_task,
                        session_id, post_uid, comment_text, 
                        min_delay, max_delay, with_image, auto_like,
                        post_index + 1, len(post_uids)
                    )
                    spam_session['futures'].append(future)
            
            # Wait for all tasks to complete
            for future in spam_session['futures']:
                try:
                    future.result(timeout=30)  # 30 second timeout per task
                except Exception as e:
                    logger.error(f"Task failed: {e}")
                    spam_session['stats']['errors'] += 1
            
        except Exception as e:
            logger.error(f"Error in spam background: {e}")
            spam_session['stats']['errors'] += 1
        
        finally:
            # Cleanup
            if spam_session['executor']:
                spam_session['executor'].shutdown(wait=False)
            
            spam_session['is_running'] = False
            
            # Send completion notification
            self.socketio.emit('spam_completed', {
                'stats': spam_session['stats'],
                'duration': time.time() - spam_session['stats']['start_time']
            }, room=session_id)
            
            logger.info(f"Spam completed for session {session_id}")

    def _process_comment_task(self, session_id: str, post_uid: str, comment_text: str, 
                            min_delay: int, max_delay: int, with_image: bool, auto_like: bool,
                            post_number: int, total_posts: int):
        """Xử lý một comment task"""
        spam_session = self._get_spam_session(session_id)
        
        if spam_session['stop_event'].is_set():
            return
        
        try:
            # Random delay
            delay = random.uniform(min_delay / 1000, max_delay / 1000)
            time.sleep(delay)
            
            if spam_session['stop_event'].is_set():
                return
            
            # Get available token
            token_info = self.token_manager.get_available_token(session_id)
            if not token_info:
                logger.error(f"No available token for session {session_id}")
                spam_session['stats']['errors'] += 1
                return
            
            # Check rate limiting
            if not self.token_manager.can_use_token(session_id, token_info['id']):
                logger.warning(f"Token {token_info['id']} hit rate limit")
                spam_session['stats']['errors'] += 1
                return
            
            # Send comment
            success = False
            comment_id = None
            
            if with_image:
                # Try to send with image
                image_path = self._get_random_image(session_id)
                if image_path:
                    photo_id = WebFacebookAPI.upload_image_to_facebook(token_info['token'], image_path)
                    if photo_id:
                        success, comment_id = WebFacebookAPI.comment_with_image(
                            post_uid, token_info['token'], comment_text, photo_id
                        )
                
                # Fallback to text-only if image failed
                if not success:
                    success, comment_id = WebFacebookAPI.comment_text_only(
                        post_uid, token_info['token'], comment_text
                    )
            else:
                # Text-only comment
                success, comment_id = WebFacebookAPI.comment_text_only(
                    post_uid, token_info['token'], comment_text
                )
            
            if success and comment_id:
                # Update token usage
                self.token_manager.use_token(session_id, token_info['id'])
                
                # Update stats
                with self.lock:
                    spam_session['stats']['comments_sent'] += 1
                
                # Auto like if enabled
                if auto_like:
                    WebFacebookAPI.like_post(token_info['token'], post_uid)
                
                # Send progress update
                self.socketio.emit('spam_progress', {
                    'comments_sent': spam_session['stats']['comments_sent'],
                    'total_comments': spam_session['stats']['total_comments'],
                    'post_number': post_number,
                    'total_posts': total_posts,
                    'comment_id': comment_id,
                    'post_uid': post_uid,
                    'with_image': with_image
                }, room=session_id)
                
                logger.info(f"Comment sent successfully: {comment_id}")
                
            else:
                spam_session['stats']['errors'] += 1
                # Mark token as potentially dead if multiple failures
                self.token_manager.mark_token_dead(session_id, token_info['id'])
                
                self.socketio.emit('spam_error', {
                    'message': f'Comment failed for post {post_uid}',
                    'post_uid': post_uid
                }, room=session_id)
                
        except Exception as e:
            logger.error(f"Error in comment task: {e}")
            spam_session['stats']['errors'] += 1
            
            self.socketio.emit('spam_error', {
                'message': f'Error processing comment: {str(e)}',
                'post_uid': post_uid
            }, room=session_id)

    def _get_random_image(self, session_id: str) -> Optional[str]:
        """Lấy ảnh ngẫu nhiên từ session folder"""
        try:
            session_folder = os.path.join('uploads/images', session_id)
            if not os.path.exists(session_folder):
                return None
            
            images = []
            for filename in os.listdir(session_folder):
                if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    images.append(os.path.join(session_folder, filename))
            
            if images:
                return random.choice(images)
            return None
            
        except Exception as e:
            logger.error(f"Error getting random image: {e}")
            return None

    def stop_spam(self, session_id: str) -> bool:
        """Dừng spam comments"""
        with self.lock:
            spam_session = self._get_spam_session(session_id)
            
            if not spam_session['is_running']:
                logger.warning(f"Spam not running for session {session_id}")
                return False
            
            # Set stop event
            spam_session['stop_event'].set()
            
            # Cancel pending futures
            for future in spam_session['futures']:
                future.cancel()
            
            # Shutdown executor
            if spam_session['executor']:
                spam_session['executor'].shutdown(wait=False)
            
            spam_session['is_running'] = False
            
            # Send stop notification
            self.socketio.emit('spam_stopped', {
                'stats': spam_session['stats']
            }, room=session_id)
            
            logger.info(f"Stopped spam for session {session_id}")
            return True

    def get_status(self, session_id: str) -> Dict:
        """Lấy trạng thái spam"""
        spam_session = self._get_spam_session(session_id)
        
        status = {
            'is_running': spam_session['is_running'],
            'stats': spam_session['stats'].copy(),
            'settings': spam_session['current_settings'].copy()
        }
        
        if spam_session['stats']['start_time']:
            status['runtime'] = time.time() - spam_session['stats']['start_time']
        
        return status

    def cleanup_session(self, session_id: str):
        """Dọn dẹp session data"""
        with self.lock:
            if session_id in self.spam_sessions:
                spam_session = self.spam_sessions[session_id]
                
                # Stop if running
                if spam_session['is_running']:
                    self.stop_spam(session_id)
                
                # Delete session data
                del self.spam_sessions[session_id]
                
                logger.info(f"Cleaned up spam session: {session_id}")

    def get_all_sessions_status(self) -> Dict:
        """Lấy trạng thái tất cả sessions"""
        status = {}
        for session_id, spam_session in self.spam_sessions.items():
            status[session_id] = {
                'is_running': spam_session['is_running'],
                'comments_sent': spam_session['stats']['comments_sent'],
                'total_comments': spam_session['stats']['total_comments'],
                'errors': spam_session['stats']['errors']
            }
        return status
