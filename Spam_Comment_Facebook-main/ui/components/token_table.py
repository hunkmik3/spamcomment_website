# -*- coding: utf-8 -*-
"""
Token Table Component
@origin 250724-01 (Plants1.3)
"""

from PyQt5.QtWidgets import (
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView,
    QMenu, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor, QBrush


class TokenTable(QTableWidget):
    """Bảng hiển thị và quản lý tokens"""
    
    # Signals
    token_selected = pyqtSignal(list)  # Danh sách row được chọn
    context_menu_requested = pyqtSignal(str, int)  # action, row
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_table()
        self.setup_context_menu()
        
    def setup_table(self):
        """Thiết lập bảng token"""
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(["👤 UID/Name", "🔑 Token", "📊 Status", "⚙️ Process"])
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().setDefaultSectionSize(32)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        self.setMinimumHeight(200)

    def setup_context_menu(self):
        """Thiết lập context menu"""
        self.context_menu = QMenu(self)
        actions = [
            "Xóa Tokens Đã Chọn",
            "Xóa Tất Cả Tokens", 
            "Kiểm Tra Tokens Đã Chọn",
            "Xóa Tokens DIE",
            "Xóa Tokens Trùng",
            "Copy Token",
            "Copy Tên Tài Khoản"
        ]
        for action_text in actions:
            action = self.context_menu.addAction(action_text)
            action.triggered.connect(lambda checked, text=action_text: self.handle_context_action(text))

    def show_context_menu(self, pos):
        """Hiển thị context menu"""
        index = self.indexAt(pos)
        if index.isValid():
            self.context_menu.exec_(self.mapToGlobal(pos))

    def handle_context_action(self, action_text):
        """Xử lý action từ context menu"""
        selected_rows = self.get_selected_rows()
        if not selected_rows and action_text not in ["Xóa Tất Cả Tokens", "Xóa Tokens DIE", "Xóa Tokens Trùng"]:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn ít nhất một token!")
            return
            
        self.context_menu_requested.emit(action_text, selected_rows[0] if selected_rows else -1)

    def get_selected_rows(self) -> list:
        """Lấy danh sách row được chọn"""
        return sorted({index.row() for index in self.selectedIndexes()})

    def add_token(self, uid: str, token: str, status: str = "Chưa Check"):
        """Thêm token vào bảng"""
        row = self.rowCount()
        self.insertRow(row)
        self.setItem(row, 0, QTableWidgetItem(uid))
        self.setItem(row, 1, QTableWidgetItem(token))
        self.setItem(row, 2, QTableWidgetItem(status))
        self.setItem(row, 3, QTableWidgetItem(""))

    def remove_selected_rows(self):
        """Xóa các row được chọn"""
        selected_rows = self.get_selected_rows()
        for row in sorted(selected_rows, reverse=True):
            self.removeRow(row)
        return len(selected_rows)

    def remove_all_rows(self):
        """Xóa tất cả rows"""
        count = self.rowCount()
        self.setRowCount(0)
        return count

    def remove_die_tokens(self):
        """Xóa tokens có status DIE"""
        rows_to_delete = []
        for row in range(self.rowCount()):
            status_item = self.item(row, 2)
            if status_item and status_item.text() == "DIE":
                rows_to_delete.append(row)
        
        for row in sorted(rows_to_delete, reverse=True):
            self.removeRow(row)
        return len(rows_to_delete)

    def remove_duplicate_tokens(self):
        """Xóa tokens trùng lặp"""
        seen = {}
        rows_to_delete = []
        for row in range(self.rowCount()):
            token_item = self.item(row, 1)
            if token_item:
                token = token_item.text()
                if token in seen:
                    rows_to_delete.append(row)
                else:
                    seen[token] = True
        
        for row in sorted(rows_to_delete, reverse=True):
            self.removeRow(row)
        return len(rows_to_delete)

    def get_tokens_from_rows(self, rows: list) -> list:
        """Lấy tokens từ các row được chỉ định"""
        tokens = []
        for row in rows:
            token_item = self.item(row, 1)
            if token_item:
                tokens.append(token_item.text())
        return tokens

    def get_accounts_from_rows(self, rows: list) -> list:
        """Lấy tên tài khoản từ các row được chỉ định"""
        accounts = []
        for row in rows:
            account_item = self.item(row, 0)
            if account_item:
                accounts.append(account_item.text())
        return accounts

    def update_token_status(self, row: int, status: str, account_name: str = None):
        """Cập nhật trạng thái token"""
        if account_name:
            self.setItem(row, 0, QTableWidgetItem(account_name))
        self.setItem(row, 2, QTableWidgetItem(status))
        
        # Cập nhật màu nền
        for col in range(self.columnCount()):
            item = self.item(row, col)
            if item:
                if status == "LIVE":
                    item.setBackground(QBrush(QColor("lightgreen")))
                else:
                    item.setBackground(QBrush(QColor("lightcoral")))

    def update_process_column(self, row: int, text: str, color: QColor = None):
        """Cập nhật cột Process"""
        item = QTableWidgetItem(text)
        if color:
            item.setBackground(QBrush(color))
        self.setItem(row, 3, item)

    def get_all_tokens_with_rows(self) -> list:
        """Lấy tất cả tokens với row index"""
        tokens_with_rows = []
        for row in range(self.rowCount()):
            token_item = self.item(row, 1)
            status_item = self.item(row, 2)
            if token_item and status_item:
                token = token_item.text()
                status = status_item.text()
                if status != "DIE":
                    tokens_with_rows.append((token, row))
        return tokens_with_rows 