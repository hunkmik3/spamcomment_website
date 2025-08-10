# -*- coding: utf-8 -*-
"""
Add Token Dialog Component
@origin 250724-01 (Plants1.3)
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPlainTextEdit, 
    QPushButton, QMessageBox
)


class AddTokenDialog(QDialog):
    """Dialog thêm token"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nhập Token")
        self.resize(450, 400)
        self.tokens = []
        self.setup_ui()
        
    def setup_ui(self):
        """Thiết lập giao diện dialog"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Label hướng dẫn
        label = QLabel("🔑 Nhập Token - Mỗi token một dòng:")
        label.setStyleSheet("font: bold 12pt; color: #2c3e50; padding: 10px;")
        layout.addWidget(label)
        
        # Text area nhập token
        self.token_text = QPlainTextEdit()
        self.token_text.setPlaceholderText("Nhập token ở đây, mỗi token một dòng...\nVí dụ:\nEAAG...\nEAAG...\nEAAG...")
        self.token_text.setMinimumHeight(200)
        layout.addWidget(self.token_text)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        self.btn_ok = QPushButton("✅ Thêm Token")
        self.btn_ok.setMinimumHeight(40)
        self.btn_cancel = QPushButton("❌ Hủy")
        self.btn_cancel.setMinimumHeight(40)
        btn_layout.addWidget(self.btn_ok)
        btn_layout.addWidget(self.btn_cancel)
        layout.addLayout(btn_layout)
        
        # Connect signals
        self.btn_ok.clicked.connect(self.on_ok)
        self.btn_cancel.clicked.connect(self.reject)
        
    def on_ok(self):
        """Xử lý khi nhấn OK"""
        tokens_str = self.token_text.toPlainText().strip()
        if tokens_str:
            tokens = tokens_str.splitlines()
            self.tokens = [tk_.strip() for tk_ in tokens if tk_.strip()]
            if self.tokens:
                self.accept()
            else:
                QMessageBox.warning(self, "Cảnh báo", "Không có token hợp lệ nào được nhập!")
        else:
            QMessageBox.warning(self, "Cảnh báo", "Không có token nào được nhập!")
            
    def get_tokens(self) -> list:
        """Lấy danh sách tokens đã nhập"""
        return self.tokens 