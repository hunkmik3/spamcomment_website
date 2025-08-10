#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tool Spam FB Token - Main Entry Point
@origin 250724-01 (Plants1.3)
"""

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from ui.main_window import AccountManagerApp
from utils.styles import global_stylesheet


def main():
    """Khởi chạy ứng dụng chính"""
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    app.setStyleSheet(global_stylesheet)

    window = AccountManagerApp()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main() 