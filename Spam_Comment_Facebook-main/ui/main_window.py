# -*- coding: utf-8 -*-
"""
Main Window - Cửa sổ chính của ứng dụng
@origin 250724-01 (Plants1.3)
"""

import os
import time
import random
import threading
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QLineEdit, QTextEdit, QPlainTextEdit, QGroupBox,
    QCheckBox, QFormLayout, QScrollArea, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QColor, QBrush, QFont, QPainter, QPixmap

from ui.components.token_table import TokenTable
from ui.components.add_token_dialog import AddTokenDialog
from utils.facebook_api import FacebookAPI
from utils.token_manager import TokenManager


class AccountManagerApp(QMainWindow):
    """Cửa sổ chính của ứng dụng"""
    
    # Signals
    append_log_signal = pyqtSignal(str)
    update_progress_signal = pyqtSignal(int, int)
    update_status_signal = pyqtSignal(str, str)  # (status_text, color)
    update_token_ui_signal = pyqtSignal(object, object)  # (selected_rows, results)
    popup_signal = pyqtSignal(str, str, str)  # (title, message, type)
    update_token_item_signal = pyqtSignal(int, str, QColor)
    update_total_label_signal = pyqtSignal(str)
    update_token_status_signal = pyqtSignal(int, str)
    clear_live_comment_signal = pyqtSignal()
    clear_post_comment_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setup_window()
        self.setup_variables()
        self.setup_signals()
        self.setup_ui()
        self.setup_timers()

    def setup_window(self):
        """Thiết lập cửa sổ chính"""
        self.setObjectName("MainWindow")
        self.setWindowTitle("🚀 Tool Spam FB Token - Professional Edition")
        self.resize(1600, 900)
        self.setMinimumSize(1400, 800)
        # Xóa background image để tránh lỗi
        self.background_path = None

    def setup_variables(self):
        """Thiết lập các biến"""
        self.comments_sent_run = 0
        self.comments_sent_total = 0
        self.stop_event = threading.Event()
        self.lock_comments = threading.Lock()
        self.is_running = False
        self.total_comments = 0
        
        # Token management
        self.token_manager = TokenManager()
        
        # Image management
        self.images_folder = None
        self.all_images = []
        self.unused_images = []
        self.image_lock = threading.Lock()
        self.comments_posted = defaultdict(list)
        
        # Live comment flags
        self.sending_live_comment = False
        self.sending_live_comment2 = False

    def setup_signals(self):
        """Thiết lập các signal connections"""
        self.update_token_item_signal.connect(self.update_token_item)
        self.update_total_label_signal.connect(self.update_total_label)
        self.update_token_status_signal.connect(self.update_token_status)
        self.clear_live_comment_signal.connect(self.clear_live_comment)
        self.clear_post_comment_signal.connect(self.clear_post_comment)
        self.update_token_ui_signal.connect(self.update_token_ui)
        self.append_log_signal.connect(self.append_log)
        self.update_progress_signal.connect(self.update_progress_label)
        self.update_status_signal.connect(self.set_status_label)
        self.popup_signal.connect(self.show_popup)

    def setup_ui(self):
        """Thiết lập giao diện"""
        # Widget trung tâm trực tiếp (không dùng QScrollArea)
        self.central_widget = QWidget()
        self.central_widget.setObjectName("centralWidget")
        self.setCentralWidget(self.central_widget)

        # Layout chính
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(8)

        # Tạo các components
        self.setup_account_management(main_layout)
        self.setup_settings_and_logs(main_layout)
        self.setup_post_comment(main_layout)
        self.setup_live_chat(main_layout)
        self.setup_live_chat2(main_layout)

    def setup_account_management(self, main_layout):
        """Thiết lập phần quản lý tài khoản"""
        group_accounts = QGroupBox("🔑 Quản Lý Tài Khoản")
        accounts_layout = QVBoxLayout(group_accounts)
        accounts_layout.setSpacing(8)
        
        # Token table
        self.token_table = TokenTable()
        self.token_table.context_menu_requested.connect(self.handle_context_menu)
        self.token_table.setMinimumHeight(180)
        self.token_table.setMaximumHeight(200)
        accounts_layout.addWidget(self.token_table)

        # Buttons
        token_btn_layout = QHBoxLayout()
        token_btn_layout.setSpacing(8)
        
        btn_add_token = QPushButton("➕ Nhập Token")
        btn_add_token.setMinimumHeight(30)
        btn_add_token.clicked.connect(self.add_token)
        token_btn_layout.addWidget(btn_add_token)
        
        btn_choose_folder = QPushButton("📁 Chọn Folder Ảnh")
        btn_choose_folder.setMinimumHeight(30)
        btn_choose_folder.clicked.connect(self.choose_image_folder)
        token_btn_layout.addWidget(btn_choose_folder)
        
        token_btn_layout.addStretch()
        
        self.cb_like = QCheckBox("❤️ Tự động Like bài viết")
        self.cb_like.setChecked(False)
        token_btn_layout.addWidget(self.cb_like)
        
        accounts_layout.addLayout(token_btn_layout)
        main_layout.addWidget(group_accounts)

    def setup_settings_and_logs(self, main_layout):
        """Thiết lập phần settings và logs"""
        middle_layout = QHBoxLayout()
        middle_layout.setSpacing(10)
        
        # Settings group
        group_settings = QGroupBox("⚙️ Cài Đặt & Trạng Thái")
        settings_layout = QHBoxLayout(group_settings)
        settings_layout.setSpacing(15)
        
        # Left side - Settings
        settings_left = QVBoxLayout()
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignRight)
        form_layout.setSpacing(8)

        self.delay_min_edit = QLineEdit("500")
        self.delay_min_edit.setMaximumWidth(80)
        self.delay_min_edit.setMinimumHeight(25)
        form_layout.addRow("⏱️ Min Delay (ms):", self.delay_min_edit)

        self.delay_max_edit = QLineEdit("2500")
        self.delay_max_edit.setMaximumWidth(80)
        self.delay_max_edit.setMinimumHeight(25)
        form_layout.addRow("⏱️ Max Delay (ms):", self.delay_max_edit)

        self.max_threads_edit = QLineEdit("10")
        self.max_threads_edit.setMaximumWidth(80)
        self.max_threads_edit.setMinimumHeight(25)
        form_layout.addRow("🔄 Max Threads:", self.max_threads_edit)

        self.num_comments_edit = QLineEdit("0")
        self.num_comments_edit.setMaximumWidth(80)
        self.num_comments_edit.setMinimumHeight(25)
        form_layout.addRow("💬 Số Comment:", self.num_comments_edit)

        self.num_image_comments_edit = QLineEdit("0")
        self.num_image_comments_edit.setMaximumWidth(80)
        self.num_image_comments_edit.setMinimumHeight(25)
        form_layout.addRow("🖼️ Comment + Ảnh:", self.num_image_comments_edit)

        settings_left.addLayout(form_layout)
        settings_left.addStretch()

        # Right side - Status
        status_layout = QVBoxLayout()
        status_layout.setSpacing(8)
        
        self.status_label = QLabel("✅ Tool Đã Sẵn Sàng Chạy")
        self.status_label.setObjectName("statusLabel")
        self.status_label.setStyleSheet("font: bold 12pt; color: #27ae60; padding: 10px; background: rgba(39, 174, 96, 0.1); border-radius: 8px;")
        status_layout.addWidget(self.status_label)
        
        self.progress_label = QLabel("📊 Comment 0/0")
        self.progress_label.setObjectName("progressLabel")
        self.progress_label.setStyleSheet("font: bold 11pt; color: #3498db; padding: 10px; background: rgba(52, 152, 219, 0.1); border-radius: 8px;")
        status_layout.addWidget(self.progress_label)
        
        self.total_posted_label = QLabel("📈 Tổng comment đã chạy: 0")
        self.total_posted_label.setStyleSheet("font: bold 11pt; color: #f39c12; padding: 10px; background: rgba(243, 156, 18, 0.1); border-radius: 8px;")
        status_layout.addWidget(self.total_posted_label)
        status_layout.addStretch()
        
        settings_layout.addLayout(settings_left)
        settings_layout.addLayout(status_layout)
        middle_layout.addWidget(group_settings, 1)

        # Logs group
        group_logs = QGroupBox("📋 Logs & Hoạt Động")
        logs_layout = QVBoxLayout(group_logs)
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMinimumHeight(120)
        self.log_text.setMaximumHeight(150)
        self.log_text.setStyleSheet("font-family: 'Consolas', 'Monaco', monospace; font-size: 8pt;")
        logs_layout.addWidget(self.log_text)
        middle_layout.addWidget(group_logs, 1)
        main_layout.addLayout(middle_layout)

    def setup_post_comment(self, main_layout):
        """Thiết lập phần post và comment"""
        group_post = QGroupBox("🚀 Post & Comment - Auto Spam")
        post_layout = QGridLayout(group_post)
        post_layout.setSpacing(10)
        
        lbl_post_uid = QLabel("📝 Post UID:")
        lbl_post_uid.setStyleSheet("font: bold 11pt; color: #2c3e50;")
        post_layout.addWidget(lbl_post_uid, 0, 0)
        self.uid_text = QPlainTextEdit()
        self.uid_text.setMinimumHeight(60)
        self.uid_text.setMaximumHeight(70)
        self.uid_text.setPlaceholderText("Nhập Post UID, mỗi UID một dòng...")
        post_layout.addWidget(self.uid_text, 0, 1)
        
        lbl_comment = QLabel("💬 Comment:")
        lbl_comment.setStyleSheet("font: bold 11pt; color: #2c3e50;")
        post_layout.addWidget(lbl_comment, 0, 2)
        self.comment_text = QPlainTextEdit()
        self.comment_text.setMinimumHeight(60)
        self.comment_text.setMaximumHeight(70)
        self.comment_text.setPlaceholderText("Nhập nội dung comment, mỗi comment một dòng...")
        post_layout.addWidget(self.comment_text, 0, 3)
        
        # Button layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.btn_start = QPushButton("▶️ Start Spam")
        self.btn_start.setObjectName("startButton")
        self.btn_start.setMinimumHeight(35)
        self.btn_start.clicked.connect(self.start_tool)
        button_layout.addWidget(self.btn_start)
        
        self.btn_stop = QPushButton("⏹️ Stop")
        self.btn_stop.setObjectName("stopButton")
        self.btn_stop.setMinimumHeight(35)
        self.btn_stop.clicked.connect(self.stop_tool)
        button_layout.addWidget(self.btn_stop)
        
        button_layout.addStretch()
        post_layout.addLayout(button_layout, 1, 1, 1, 3)
        
        post_layout.setColumnStretch(1, 2)
        post_layout.setColumnStretch(3, 3)
        main_layout.addWidget(group_post)

        self.uid_text.textChanged.connect(self.on_post_uid_changed)

    def setup_live_chat(self, main_layout):
        """Thiết lập live chat 1"""
        group_live_chat = QGroupBox("💬 Live Chat - Gửi Comment Nhanh")
        live_chat_layout = QGridLayout(group_live_chat)
        live_chat_layout.setSpacing(10)
        
        lbl_live_uid = QLabel("📝 Post UID:")
        lbl_live_uid.setStyleSheet("font: bold 11pt; color: #2c3e50;")
        live_chat_layout.addWidget(lbl_live_uid, 0, 0)
        self.live_uid_edit = QPlainTextEdit()
        self.live_uid_edit.setMinimumHeight(50)
        self.live_uid_edit.setMaximumHeight(60)
        self.live_uid_edit.setPlaceholderText("Nhập Post UID để gửi comment...")
        live_chat_layout.addWidget(self.live_uid_edit, 0, 1)
        
        lbl_live_comment = QLabel("💬 Comment:")
        lbl_live_comment.setStyleSheet("font: bold 11pt; color: #2c3e50;")
        live_chat_layout.addWidget(lbl_live_comment, 0, 2)
        self.live_comment_edit = QPlainTextEdit()
        self.live_comment_edit.setMinimumHeight(50)
        self.live_comment_edit.setMaximumHeight(60)
        self.live_comment_edit.setPlaceholderText("Nhập nội dung comment...")
        live_chat_layout.addWidget(self.live_comment_edit, 0, 3)
        
        btn_live_send = QPushButton("🚀 Gửi Comment Ngay")
        btn_live_send.setMinimumHeight(30)
        btn_live_send.clicked.connect(self.send_live_comment)
        live_chat_layout.addWidget(btn_live_send, 1, 1, 1, 2)
        
        live_chat_layout.setColumnStretch(1, 2)
        live_chat_layout.setColumnStretch(3, 3)
        main_layout.addWidget(group_live_chat)

        self.live_uid_edit.textChanged.connect(self.on_live_uid_changed)

    def setup_live_chat2(self, main_layout):
        """Thiết lập live chat 2"""
        group_live_chat2 = QGroupBox("💬 Live Chat 2 - Gửi Comment Nhanh")
        live_chat_layout2 = QGridLayout(group_live_chat2)
        live_chat_layout2.setSpacing(10)
        
        lbl_live_uid2 = QLabel("📝 Post UID:")
        lbl_live_uid2.setStyleSheet("font: bold 11pt; color: #2c3e50;")
        live_chat_layout2.addWidget(lbl_live_uid2, 0, 0)
        self.live_uid_edit2 = QPlainTextEdit()
        self.live_uid_edit2.setMinimumHeight(50)
        self.live_uid_edit2.setMaximumHeight(60)
        self.live_uid_edit2.setPlaceholderText("Nhập Post UID để gửi comment...")
        live_chat_layout2.addWidget(self.live_uid_edit2, 0, 1)
        
        lbl_live_comment2 = QLabel("💬 Comment:")
        lbl_live_comment2.setStyleSheet("font: bold 11pt; color: #2c3e50;")
        live_chat_layout2.addWidget(lbl_live_comment2, 0, 2)
        self.live_comment_edit2 = QPlainTextEdit()
        self.live_comment_edit2.setMinimumHeight(50)
        self.live_comment_edit2.setMaximumHeight(60)
        self.live_comment_edit2.setPlaceholderText("Nhập nội dung comment...")
        live_chat_layout2.addWidget(self.live_comment_edit2, 0, 3)
        
        self.btn_live_send2 = QPushButton("🚀 Gửi Comment Ngay")
        self.btn_live_send2.setMinimumHeight(30)
        self.btn_live_send2.clicked.connect(self.send_live_comment2)
        live_chat_layout2.addWidget(self.btn_live_send2, 1, 1, 1, 2)
        
        live_chat_layout2.setColumnStretch(1, 2)
        live_chat_layout2.setColumnStretch(3, 3)
        main_layout.addWidget(group_live_chat2)

        self.live_uid_edit2.textChanged.connect(self.on_live_uid_changed2)

    def setup_timers(self):
        """Thiết lập các timer cho auto fetch"""
        self.uid_post_timer = QTimer()
        self.uid_post_timer.setSingleShot(True)
        self.uid_post_timer.timeout.connect(self.handle_post_uid_auto)
        
        self.uid_live_timer = QTimer()
        self.uid_live_timer.setSingleShot(True)
        self.uid_live_timer.timeout.connect(self.handle_live_uid_auto)
        
        self.uid_live_timer2 = QTimer()
        self.uid_live_timer2.setSingleShot(True)
        self.uid_live_timer2.timeout.connect(self.handle_live_uid_auto2)

    def paintEvent(self, event):
        """Vẽ ảnh nền (đã tắt)"""
        # Xóa background image để tránh lỗi
        super().paintEvent(event)

    # ================== Auto Fetch Page Name ==================
    def on_post_uid_changed(self):
        if getattr(self, 'is_updating_post_uid', False):
            return
        self.uid_post_timer.start(1000)

    def handle_post_uid_auto(self):
        text = self.uid_text.toPlainText().strip()
        if not text:
            return
        lines = text.splitlines()
        new_lines = []
        for line in lines:
            original = line.strip()
            page_name = self.fetch_page_name_auto(original)
            if page_name:
                new_lines.append(f"{original} ({page_name})")
            else:
                new_lines.append(original)
        new_text = "\n".join(new_lines)
        if new_text != text:
            self.is_updating_post_uid = True
            self.uid_text.setPlainText(new_text)
            self.is_updating_post_uid = False

    def on_live_uid_changed(self):
        if getattr(self, 'is_updating_live_uid', False):
            return
        self.uid_live_timer.start(1000)

    def handle_live_uid_auto(self):
        text = self.live_uid_edit.toPlainText().strip()
        if not text:
            return
        lines = text.splitlines()
        new_lines = []
        for line in lines:
            original = line.strip()
            page_name = self.fetch_page_name_auto(original)
            if page_name:
                new_lines.append(f"{original} ({page_name})")
            else:
                new_lines.append(original)
        new_text = "\n".join(new_lines)
        if new_text != text:
            self.is_updating_live_uid = True
            self.live_uid_edit.setPlainText(new_text)
            self.is_updating_live_uid = False

    def on_live_uid_changed2(self):
        if getattr(self, 'is_updating_live_uid2', False):
            return
        self.uid_live_timer2.start(1000)

    def handle_live_uid_auto2(self):
        text = self.live_uid_edit2.toPlainText().strip()
        if not text:
            return
        lines = text.splitlines()
        new_lines = []
        for line in lines:
            original = line.strip()
            page_name = self.fetch_page_name_auto(original)
            if page_name:
                new_lines.append(f"{original} ({page_name})")
            else:
                new_lines.append(original)
        new_text = "\n".join(new_lines)
        if new_text != text:
            self.is_updating_live_uid2 = True
            self.live_uid_edit2.setPlainText(new_text)
            self.is_updating_live_uid2 = False

    def fetch_page_name_auto(self, uid: str):
        """Lấy tên page tự động"""
        self.update_token_list()
        if not self.token_manager.available_tokens:
            return None
        token, _ = self.token_manager.available_tokens[0]
        return FacebookAPI.fetch_page_name(token, uid)

    # ================== Live Comment ==================
    def send_live_comment(self):
        if self.sending_live_comment:
            return
        self.sending_live_comment = True
        sender = self.sender()
        if sender:
            sender.setEnabled(False)
        threading.Thread(target=self._send_live_comment, daemon=True).start()

    def _send_live_comment(self):
        try:
            raw_post_id = self.live_uid_edit.toPlainText().strip()
            post_id = raw_post_id.split(" (")[0] if " (" in raw_post_id else raw_post_id
            comment = self.live_comment_edit.toPlainText().strip()
            
            if not post_id:
                self.popup_signal.emit("Cảnh báo", "Vui lòng nhập Post UID.", "warning")
                return
            if not comment:
                self.popup_signal.emit("Cảnh báo", "Vui lòng nhập comment.", "warning")
                return
                
            self.update_token_list()
            token, row = self.token_manager.get_token_from_queue()
            if not token:
                self.popup_signal.emit("Lỗi", "Không có token LIVE khả dụng.", "critical")
                return
                
            if not self.token_manager.can_use_token(token):
                self.write_log(f"Token {token[:25]}... đạt giới hạn rate. Bỏ qua.")
                return
                
            self.token_manager.use_token(token)
            success, comment_id = FacebookAPI.comment_text_only(post_id, token, comment)
            
            if success:
                self.popup_signal.emit("Thành công", f"[LIVE] Đã gửi comment live trên Post {post_id}", "info")
                self.clear_live_comment_signal.emit()
            else:
                self.popup_signal.emit("Lỗi", f"[LIVE] Gửi comment live thất bại trên Post {post_id}", "critical")
        finally:
            QTimer.singleShot(0, self.reset_live_comment_flag)

    def reset_live_comment_flag(self):
        for child in self.findChildren(QPushButton):
            if child.text() == "Gửi Comment":
                child.setEnabled(True)
        self.sending_live_comment = False

    def send_live_comment2(self):
        if self.sending_live_comment2:
            return
        self.sending_live_comment2 = True
        sender = self.sender()
        if sender:
            sender.setEnabled(False)
        threading.Thread(target=self._send_live_comment2, daemon=True).start()

    def _send_live_comment2(self):
        try:
            raw_post_id = self.live_uid_edit2.toPlainText().strip()
            post_id = raw_post_id.split(" (")[0] if " (" in raw_post_id else raw_post_id
            comment = self.live_comment_edit2.toPlainText().strip()
            
            if not post_id:
                self.popup_signal.emit("Cảnh báo", "Vui lòng nhập Post UID (Live Chat 2).", "warning")
                return
            if not comment:
                self.popup_signal.emit("Cảnh báo", "Vui lòng nhập comment (Live Chat 2).", "warning")
                return
                
            self.update_token_list()
            token, row = self.token_manager.get_token_from_queue()
            if not token:
                self.popup_signal.emit("Lỗi", "Không có token LIVE khả dụng (Live Chat 2).", "critical")
                return
                
            if not self.token_manager.can_use_token(token):
                self.write_log(f"Token {token[:25]}... đạt giới hạn rate. Bỏ qua.")
                return
                
            self.token_manager.use_token(token)
            success, comment_id = FacebookAPI.comment_text_only(post_id, token, comment)
            
            if success:
                self.popup_signal.emit("Thành công", f"[LIVE 2] Đã gửi comment live trên Post {post_id}", "info")
                self.live_comment_edit2.clear()
            else:
                self.popup_signal.emit("Lỗi", f"[LIVE 2] Gửi comment live thất bại trên Post {post_id}", "critical")
        finally:
            QTimer.singleShot(0, self.reset_live_comment_flag2)

    def reset_live_comment_flag2(self):
        self.btn_live_send2.setEnabled(True)
        self.sending_live_comment2 = False

    # ================== UI Updates ==================
    def append_log(self, text):
        self.log_text.append(text)

    def write_log(self, text: str):
        self.append_log_signal.emit(text)

    def update_progress_label(self, value: int, maximum: int):
        progress_text = f"Comment {value}/{maximum}" if maximum > 0 else "Comment 0/0"
        self.progress_label.setText(progress_text)

    def set_status_label(self, text: str, color: str):
        self.status_label.setText(text)
        self.status_label.setStyleSheet(f"font: 12pt; color: {color};")

    def update_status(self, text: str, color: str):
        self.update_status_signal.emit(text, color)

    def update_token_item(self, row, text, color):
        self.token_table.update_process_column(row, text, color)

    def update_total_label(self, text):
        self.total_posted_label.setText(text)

    def update_token_status(self, row, status):
        self.token_table.setItem(row, 2, QTableWidgetItem(status))

    def clear_live_comment(self):
        self.live_comment_edit.clear()

    def clear_post_comment(self):
        self.comment_text.clear()

    def show_popup(self, title, message, popup_type):
        if popup_type == "info":
            QMessageBox.information(self, title, message)
        elif popup_type == "warning":
            QMessageBox.warning(self, title, message)
        elif popup_type == "critical":
            QMessageBox.critical(self, title, message)

    def update_token_ui(self, selected_rows, results):
        selected_rows = list(selected_rows)
        for row, (status, account_name) in zip(selected_rows, results):
            self.token_table.update_token_status(row, status, account_name)

    def update_token_list(self):
        """Cập nhật danh sách token khả dụng"""
        tokens_with_rows = self.token_table.get_all_tokens_with_rows()
        self.token_manager.update_available_tokens(tokens_with_rows)

    # ================== Token Management ==================
    def add_token(self):
        dialog = AddTokenDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            tokens = dialog.get_tokens()
            for token in tokens:
                self.token_table.add_token("Unknown", token, "Chưa Check")
            self.update_token_list()
            QMessageBox.information(self, "Thông báo", f"Đã thêm {len(tokens)} token thành công!")
            self.write_log(f"Đã thêm {len(tokens)} token thành công.")

    def choose_image_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Chọn thư mục ảnh")
        if folder:
            self.images_folder = folder
            all_files = os.listdir(folder)
            self.all_images = [
                os.path.join(folder, f)
                for f in all_files
                if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))
            ]
            with self.image_lock:
                self.unused_images = list(self.all_images)
            self.write_log(f"Đã chọn folder ảnh: {folder}, có {len(self.all_images)} file ảnh.")
        else:
            self.write_log("Chưa chọn folder ảnh hoặc hủy.")

    def handle_context_menu(self, action_text: str, row: int):
        """Xử lý context menu của token table"""
        if action_text == "Xóa Tokens Đã Chọn":
            count = self.token_table.remove_selected_rows()
            self.write_log(f"Đã xóa {count} token được chọn.")
            
        elif action_text == "Xóa Tất Cả Tokens":
            count = self.token_table.remove_all_rows()
            self.token_manager.available_tokens.clear()
            self.write_log(f"Đã xóa toàn bộ {count} token.")
            
        elif action_text == "Kiểm Tra Tokens Đã Chọn":
            selected_rows = self.token_table.get_selected_rows()
            tokens = self.token_table.get_tokens_from_rows(selected_rows)
            if tokens:
                self.write_log(f"Đang kiểm tra {len(tokens)} token...")
                threading.Thread(target=self.check_tokens_thread, args=(selected_rows, tokens), daemon=True).start()
                
        elif action_text == "Xóa Tokens DIE":
            count = self.token_table.remove_die_tokens()
            self.write_log(f"Đã xóa {count} token DIE.")
            
        elif action_text == "Xóa Tokens Trùng":
            count = self.token_table.remove_duplicate_tokens()
            QMessageBox.information(self, "Thông Báo", "Đã xóa token trùng thành công!")
            self.write_log(f"Đã xóa {count} token trùng.")
            
        elif action_text == "Copy Token":
            selected_rows = self.token_table.get_selected_rows()
            tokens = self.token_table.get_tokens_from_rows(selected_rows)
            if tokens:
                from PyQt5.QtWidgets import QApplication
                QApplication.clipboard().setText("\n".join(tokens))
                self.write_log("Đã copy token.")
                
        elif action_text == "Copy Tên Tài Khoản":
            selected_rows = self.token_table.get_selected_rows()
            accounts = self.token_table.get_accounts_from_rows(selected_rows)
            if accounts:
                from PyQt5.QtWidgets import QApplication
                QApplication.clipboard().setText("\n".join(accounts))
                self.write_log("Đã copy tên tài khoản.")
        
        self.update_token_list()

    def check_tokens_thread(self, selected_rows, tokens):
        """Thread kiểm tra tokens"""
        results = self.token_manager.check_tokens_status(tokens)
        self.update_token_ui_signal.emit(list(selected_rows), results)
        live_count = sum(1 for status, _ in results if status == "LIVE")
        die_count = sum(1 for status, _ in results if status == "DIE")
        self.write_log(f"Kiểm tra token hoàn tất! LIVE={live_count}, DIE={die_count}")
        self.popup_signal.emit("Thông Báo", "Kiểm tra token hoàn tất!", "info")
        self.update_token_list()

    # ================== Tool Control ==================
    def start_tool(self):
        """Bắt đầu chạy tool"""
        if self.is_running:
            QMessageBox.warning(self, "Cảnh báo", "Tool đang chạy, vui lòng dừng hoặc đợi xong!")
            return
            
        try:
            min_delay = int(self.delay_min_edit.text().strip())
            max_delay = int(self.delay_max_edit.text().strip())
            num_comments = int(self.num_comments_edit.text().strip())
            max_workers = int(self.max_threads_edit.text().strip())
            num_image_comments = int(self.num_image_comments_edit.text().strip())
            
            if min_delay >= max_delay:
                QMessageBox.critical(self, "Error", "Min Delay phải nhỏ hơn Max Delay.")
                return
            if num_comments <= 0:
                QMessageBox.critical(self, "Error", "Số lượng bình luận phải lớn hơn 0.")
                return
            if max_workers <= 0:
                QMessageBox.critical(self, "Error", "Số luồng phải lớn hơn 0.")
                return
            if num_image_comments < 0:
                QMessageBox.critical(self, "Error", "Số comment kèm ảnh phải >= 0.")
                return
            if num_image_comments > num_comments:
                QMessageBox.warning(self, "Cảnh báo", "Số comment kèm ảnh lớn hơn số comment muốn chạy.\nHệ thống sẽ tự điều chỉnh cho phù hợp.")
                num_image_comments = num_comments

            raw_post_ids = self.uid_text.toPlainText().strip().splitlines()
            post_ids = []
            for line in raw_post_ids:
                line = line.strip()
                if " (" in line:
                    post_ids.append(line.split(" (")[0])
                else:
                    post_ids.append(line)
                    
            comments = self.comment_text.toPlainText().strip().splitlines()
            
            if not post_ids:
                QMessageBox.critical(self, "Error", "Vui lòng nhập Post UID.")
                return
            if not comments:
                QMessageBox.critical(self, "Error", "Vui lòng nhập nội dung comment.")
                return
            if len(comments) < num_comments:
                QMessageBox.critical(self, "Error", "Số comment trong box ít hơn số comment muốn chạy.\nVui lòng nhập thêm comment hoặc giảm Số Comment Muốn Chạy.")
                return
                
        except ValueError as err:
            QMessageBox.critical(self, "Error", f"Lỗi nhập liệu: {err}")
            return

        self.update_token_list()
        if not self.token_manager.available_tokens:
            QMessageBox.critical(self, "Error", "Không có token LIVE nào khả dụng.")
            return

        self.comments_sent_run = 0
        self.stop_event.clear()
        self.total_comments = len(post_ids) * num_comments
        self.update_progress_signal.emit(0, self.total_comments)
        self.is_running = True
        self.update_status("Tool Đang Chạy...", "green")
        self.update_total_label_signal.emit(f"Tổng comment đã chạy: {self.comments_sent_total}")

        threading.Thread(
            target=self._run_tool,
            args=(min_delay, max_delay, num_comments, max_workers, num_image_comments, post_ids, comments),
            daemon=True
        ).start()

    def _run_tool(self, min_delay, max_delay, num_comments, max_workers, num_image_comments, post_ids, comments):
        """Chạy tool trong thread riêng"""
        futures = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for post_id in post_ids:
                if self.stop_event.is_set():
                    break
                image_indices = set(random.sample(range(num_comments), num_image_comments))
                for i in range(num_comments):
                    if self.stop_event.is_set():
                        break
                    cmt_text = comments[i]
                    token, row = self.token_manager.get_token_from_queue()
                    if not token:
                        self.write_log("[ERROR] Hết token LIVE, dừng tool.")
                        self.stop_event.set()
                        break
                    with_image = (i in image_indices)
                    future = executor.submit(
                        self.run_comment_task, post_id, token, cmt_text, row, min_delay, max_delay, with_image
                    )
                    futures.append(future)
            for future in futures:
                future.result()

        self.popup_signal.emit("Thông Báo", "Hoàn thành comment cho tất cả các post.", "info")
        self.clear_post_comment_signal.emit()
        self.update_status("Tool Đã Sẵn Sàng Chạy", "blue")
        self.is_running = False

    def stop_tool(self):
        """Dừng tool"""
        if self.is_running:
            self.stop_event.set()
            self.is_running = False
            self.update_status("Tool đã dừng.", "red")
            self.popup_signal.emit("Thông Báo", "Công cụ đã dừng!", "info")
            self.write_log("Người dùng nhấn nút Stop -> Tool dừng.")
        else:
            self.popup_signal.emit("Thông Báo", "Tool chưa chạy hoặc đã dừng rồi!", "info")

    def run_comment_task(self, post_id, token, comment_text, row, min_delay, max_delay, with_image):
        """Task comment trong thread"""
        if self.stop_event.is_set():
            return
        delay = random.uniform(min_delay / 1000, max_delay / 1000)
        time.sleep(delay)
        self.comment_with_delay(post_id, token, comment_text, row, with_image)

    def comment_with_delay(self, post_id, token, comment_text, row, with_image):
        """Comment với delay"""
        if self.stop_event.is_set():
            return
        if not self.token_manager.can_use_token(token):
            self.write_log(f"Token {token[:25]}... đạt giới hạn rate. Bỏ qua.")
            return
        self.token_manager.use_token(token)
        
        try:
            photo_id = None
            if with_image:
                if self.images_folder and self.all_images:
                    with self.image_lock:
                        if not self.unused_images:
                            self.unused_images = list(self.all_images)
                        img_path = random.choice(self.unused_images)
                        self.unused_images.remove(img_path)
                    photo_id = FacebookAPI.upload_image_to_facebook(token, img_path)
                else:
                    self.write_log("[WARN] Muốn kèm ảnh nhưng chưa chọn folder hoặc folder rỗng => fallback text-only.")
                    
            success = False
            comment_id = None
            if photo_id:
                success, comment_id = FacebookAPI.comment_with_image(post_id, token, comment_text, photo_id)
                if not success:
                    self.write_log("[FAIL] Comment kèm ảnh => fallback text-only.")
                    success, comment_id = FacebookAPI.comment_text_only(post_id, token, comment_text)
            else:
                success, comment_id = FacebookAPI.comment_text_only(post_id, token, comment_text)
                
            if success and comment_id:
                with self.lock_comments:
                    self.comments_sent_run += 1
                    self.comments_sent_total += 1
                    self.update_progress_signal.emit(self.comments_sent_run, self.total_comments)
                    self.update_total_label_signal.emit(f"Tổng comment đã chạy: {self.comments_sent_total}")
                self.comments_posted[post_id].append((token, comment_id))
                self.token_manager.increment_comment_count(token)
                current_text = f"Đã chạy {self.token_manager.get_comment_count(token)} comment"
                self.update_token_item_signal.emit(row, current_text, self.get_status_color(row))
                if self.cb_like.isChecked():
                    FacebookAPI.like_post(token, post_id)
        except Exception as e:
            self.write_log(f"[ERROR] Yêu cầu bị lỗi: {e}")
            self.update_token_item_signal.emit(row, "Token không thể chạy", QColor("red"))
            self.mark_token_dead(token)

    def get_status_color(self, row):
        """Lấy màu status cho token"""
        status_item = self.token_table.item(row, 2)
        if status_item:
            status = status_item.text()
            if status == "LIVE":
                return QColor("lightgreen")
            elif status == "DIE":
                return QColor("lightcoral")
        return QColor("lightgray")

    def mark_token_dead(self, token):
        """Đánh dấu token chết"""
        for row in range(self.token_table.rowCount()):
            token_item = self.token_table.item(row, 1)
            if token_item and token_item.text() == token:
                self.update_token_status_signal.emit(row, "DIE")
                break
        self.write_log(f"Token {token[:25]}... bị đánh dấu DIE.")
        with open("dead_tokens.log", "a", encoding="utf-8") as f:
            f.write(f"{token}\n")
        self.token_manager.remove_token(token) 