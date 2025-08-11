#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Spam Manager for Web App - Quản lý spam process với threading
@origin 250724-01 (Plants1.3)
"""

import time
import threading
import random
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Optional, Any
from queue import Queue

from .facebook_api import WebFacebookAPI

logger = logging.getLogger(__name__)


class SpamManager:
    """Quản lý spam process với multi-threading"""
    
    def __init__(self, session_id: str, token_manager, socketio=None):
        self.session_id = session_id
        self.token_manager = token_manager
        self.socketio = socketio
        
        # Spam state
        self.is_running_flag = False
        self.should_stop = False
        self.executor = None
        
        # Statistics
        self.stats = {
            'comments_sent': 0,
            'total_comments': 0,
            'successful_comments': 0,
            'failed_comments': 0,
            'posts_processed': 0,
            'total_posts': 0,
            'start_time': 0,
            'end_time': 0
        }
        
        # Thread safety
        self.lock = threading.Lock()
    
    def is_running(self) -> bool:
        """Kiểm tra spam có đang chạy không"""
        return self.is_running_flag
    
    def start_spam(self, post_uids: List[str], comment_texts: List[str], settings: Dict):
        """Bắt đầu spam process"""
        if self.is_running_flag:
            raise Exception("Spam đang chạy")
        
        with self.lock:
            self.is_running_flag = True
            self.should_stop = False
            
            # Reset statistics
            self.stats = {
                'comments_sent': 0,
                'total_comments': len(post_uids) * len(comment_texts),
                'successful_comments': 0,
                'failed_comments': 0,
                'posts_processed': 0,
                'total_posts': len(post_uids),
                'start_time': time.time(),
                'end_time': 0
            }
        
        # Emit spam started event
        if self.socketio:
            self.socketio.emit('spam_started', {
                'total_comments': self.stats['total_comments'],
                'posts': self.stats['total_posts']
            }, room=self.session_id)
        
        logger.info(f"Starting spam for session {self.session_id}: {len(post_uids)} posts, {len(comment_texts)} comments")
        
        try:
            self._run_spam(post_uids, comment_texts, settings)
        except Exception as e:
            logger.error(f"Error in spam process: {e}")
            if self.socketio:
                self.socketio.emit('spam_error', {
                    'message': str(e)
                }, room=self.session_id)
        finally:
            self._finish_spam()
    
    def stop_spam(self):
        """Dừng spam process"""
        with self.lock:
            self.should_stop = True
            
        if self.executor:
            # Cancel pending futures
            self.executor.shutdown(wait=False)
        
        # Emit stopped event
        if self.socketio:
            self.socketio.emit('spam_stopped', {
                'stats': self.stats
            }, room=self.session_id)
        
        logger.info(f"Spam stopped for session {self.session_id}")
    
    def _run_spam(self, post_uids: List[str], comment_texts: List[str], settings: Dict):
        """Chạy spam process chính"""
        max_threads = min(settings.get('max_threads', 10), 20)  # Limit max threads
        min_delay = settings.get('min_delay', 5000) / 1000.0  # Convert to seconds
        max_delay = settings.get('max_delay', 15000) / 1000.0
        auto_like = settings.get('auto_like', True)
        
        # Create thread pool
        self.executor = ThreadPoolExecutor(max_workers=max_threads)
        
        # Create comment tasks
        tasks = []
        for post_uid in post_uids:
            for comment_text in comment_texts:
                if self.should_stop:
                    break
                    
                task_data = {
                    'post_uid': post_uid,
                    'comment_text': comment_text,
                    'auto_like': auto_like,
                    'delay': random.uniform(min_delay, max_delay)
                }
                
                future = self.executor.submit(self._spam_single_comment, task_data)
                tasks.append(future)
            
            if self.should_stop:
                break
        
        # Wait for all tasks to complete
        for future in as_completed(tasks):
            if self.should_stop:
                break
                
            try:
                result = future.result(timeout=60)  # 60 second timeout per task
                self._update_progress(result)
            except Exception as e:
                logger.error(f"Task failed: {e}")
                self._update_progress({'success': False, 'error': str(e)})
    
    def _spam_single_comment(self, task_data: Dict) -> Dict:
        """Xử lý một comment task"""
        try:
            # Apply delay before processing
            time.sleep(task_data['delay'])
            
            if self.should_stop:
                return {'success': False, 'cancelled': True}
            
            # Get available token
            token_data = self.token_manager.get_available_token(self.session_id)
            if not token_data:
                return {'success': False, 'error': 'Không có token khả dụng'}
            
            token = token_data['token']
            token_id = token_data['id']
            
            # Check rate limiting
            if not self.token_manager.can_use_token(self.session_id, token_id):
                return {'success': False, 'error': f'Token {token_id} đã đạt rate limit'}
            
            post_uid = task_data['post_uid']
            comment_text = task_data['comment_text']
            
            # Send comment
            success, comment_id = WebFacebookAPI.comment_text_only(post_uid, token, comment_text)
            
            if success:
                # Mark token as used
                self.token_manager.use_token(self.session_id, token_id)
                
                # Auto like if enabled
                if task_data['auto_like']:
                    like_success = WebFacebookAPI.like_post(token, post_uid)
                    logger.info(f"Auto like {'successful' if like_success else 'failed'} for post {post_uid}")
                
                return {
                    'success': True,
                    'comment_id': comment_id,
                    'post_uid': post_uid,
                    'token_id': token_id,
                    'with_image': False
                }
            else:
                # Comment failed - might be token issue
                if comment_id is None:  # Likely token problem
                    self.token_manager.mark_token_dead(self.session_id, token_id)
                    logger.warning(f"Marked token {token_id} as dead due to comment failure")
                
                return {
                    'success': False,
                    'error': 'Comment failed',
                    'post_uid': post_uid,
                    'token_id': token_id
                }
                
        except Exception as e:
            logger.error(f"Error in spam task: {e}")
            return {'success': False, 'error': str(e)}
    
    def _update_progress(self, result: Dict):
        """Cập nhật progress và emit events"""
        with self.lock:
            self.stats['comments_sent'] += 1
            
            if result.get('success'):
                self.stats['successful_comments'] += 1
            else:
                self.stats['failed_comments'] += 1
        
        # Emit progress event
        if self.socketio and result.get('success'):
            self.socketio.emit('spam_progress', {
                'comments_sent': self.stats['comments_sent'],
                'total_comments': self.stats['total_comments'],
                'comment_id': result.get('comment_id'),
                'post_uid': result.get('post_uid'),
                'with_image': result.get('with_image', False)
            }, room=self.session_id)
        
        # Emit error if needed
        if self.socketio and not result.get('success') and not result.get('cancelled'):
            self.socketio.emit('spam_error', {
                'message': result.get('error', 'Unknown error'),
                'post_uid': result.get('post_uid'),
                'token_id': result.get('token_id')
            }, room=self.session_id)
    
    def _finish_spam(self):
        """Kết thúc spam process"""
        with self.lock:
            self.is_running_flag = False
            self.stats['end_time'] = time.time()
            duration = self.stats['end_time'] - self.stats['start_time']
        
        # Shutdown executor
        if self.executor:
            self.executor.shutdown(wait=True)
            self.executor = None
        
        # Emit completion event
        if self.socketio:
            self.socketio.emit('spam_completed', {
                'stats': self.stats,
                'duration': duration
            }, room=self.session_id)
        
        logger.info(f"Spam completed for session {self.session_id}. "
                   f"Success: {self.stats['successful_comments']}, "
                   f"Failed: {self.stats['failed_comments']}, "
                   f"Duration: {duration:.1f}s")
    
    def get_stats(self) -> Dict:
        """Lấy thống kê hiện tại"""
        with self.lock:
            stats = self.stats.copy()
            if self.is_running_flag and stats['start_time'] > 0:
                stats['duration'] = time.time() - stats['start_time']
            else:
                stats['duration'] = stats['end_time'] - stats['start_time'] if stats['end_time'] > 0 else 0
            
            return stats


class ImageSpamManager(SpamManager):
    """Spam Manager with image support"""
    
    def _spam_single_comment_with_image(self, task_data: Dict) -> Dict:
        """Xử lý comment với ảnh"""
        try:
            # Apply delay
            time.sleep(task_data['delay'])
            
            if self.should_stop:
                return {'success': False, 'cancelled': True}
            
            # Get available token
            token_data = self.token_manager.get_available_token(self.session_id)
            if not token_data:
                return {'success': False, 'error': 'Không có token khả dụng'}
            
            token = token_data['token']
            token_id = token_data['id']
            
            # Check rate limiting
            if not self.token_manager.can_use_token(self.session_id, token_id):
                return {'success': False, 'error': f'Token {token_id} đã đạt rate limit'}
            
            post_uid = task_data['post_uid']
            comment_text = task_data['comment_text']
            image_path = task_data['image_path']
            
            # Upload image first
            photo_id = WebFacebookAPI.upload_image_to_facebook(token, image_path)
            if not photo_id:
                return {'success': False, 'error': 'Upload ảnh thất bại'}
            
            # Send comment with image
            success, comment_id = WebFacebookAPI.comment_with_image(post_uid, token, comment_text, photo_id)
            
            if success:
                # Mark token as used
                self.token_manager.use_token(self.session_id, token_id)
                
                # Auto like if enabled
                if task_data['auto_like']:
                    like_success = WebFacebookAPI.like_post(token, post_uid)
                    logger.info(f"Auto like {'successful' if like_success else 'failed'} for post {post_uid}")
                
                return {
                    'success': True,
                    'comment_id': comment_id,
                    'post_uid': post_uid,
                    'token_id': token_id,
                    'with_image': True,
                    'photo_id': photo_id
                }
            else:
                # Comment failed
                if comment_id is None:
                    self.token_manager.mark_token_dead(self.session_id, token_id)
                
                return {
                    'success': False,
                    'error': 'Comment với ảnh thất bại',
                    'post_uid': post_uid,
                    'token_id': token_id
                }
                
        except Exception as e:
            logger.error(f"Error in image spam task: {e}")
            return {'success': False, 'error': str(e)}