# -*- coding: utf-8 -*-
"""
Stylesheet cho giao diện ứng dụng
@origin 250724-01 (Plants1.3)
"""

global_stylesheet = """
/* Main Window */
QMainWindow {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #667eea, stop:1 #764ba2);
}

QWidget#centralWidget {
    background: transparent;
}

QScrollArea {
    background: transparent;
    border: none;
}

/* Modern GroupBox */
QGroupBox {
    background: rgba(255, 255, 255, 0.95);
    border: 2px solid #e1e8ed;
    border-radius: 12px;
    margin-top: 15px;
    font: bold 13pt "Segoe UI";
    color: #2c3e50;
    padding-top: 10px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 15px;
    padding: 0 8px;
    color: #34495e;
    background: rgba(255, 255, 255, 0.95);
    border-radius: 6px;
}

/* Modern Table */
QTableWidget {
    background: rgba(255, 255, 255, 0.9);
    color: #2c3e50;
    border: 1px solid #e1e8ed;
    border-radius: 8px;
    gridline-color: #ecf0f1;
    selection-background-color: #3498db;
    selection-color: white;
}

QHeaderView::section {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #3498db, stop:1 #2980b9);
    color: white;
    padding: 8px;
    border: none;
    font: bold 10pt "Segoe UI";
}

QTableWidget::item {
    padding: 6px;
    border-bottom: 1px solid #ecf0f1;
}

QTableWidget::item:selected {
    background: #3498db;
    color: white;
}

/* Modern Input Fields */
QLineEdit, QPlainTextEdit, QTextEdit {
    background: rgba(255, 255, 255, 0.9);
    color: #2c3e50;
    border: 2px solid #e1e8ed;
    border-radius: 8px;
    padding: 8px;
    font: 10pt "Segoe UI";
}

QLineEdit:focus, QPlainTextEdit:focus, QTextEdit:focus {
    border: 2px solid #3498db;
    background: rgba(255, 255, 255, 0.95);
}

/* Modern Buttons */
QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #3498db, stop:1 #2980b9);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font: bold 10pt "Segoe UI";
    min-height: 20px;
}

QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #5dade2, stop:1 #3498db);
}

QPushButton:pressed {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #2980b9, stop:1 #21618c);
}

QPushButton:disabled {
    background: #bdc3c7;
    color: #7f8c8d;
}

/* Special Button Styles */
QPushButton#startButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #27ae60, stop:1 #229954);
}

QPushButton#startButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #2ecc71, stop:1 #27ae60);
}

QPushButton#stopButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #e74c3c, stop:1 #c0392b);
}

QPushButton#stopButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #ec7063, stop:1 #e74c3c);
}

/* Modern Labels */
QLabel {
    font-family: 'Segoe UI';
    color: #2c3e50;
    font-size: 10pt;
}

QLabel#titleLabel {
    font: bold 16pt "Segoe UI";
    color: #34495e;
}

QLabel#statusLabel {
    font: bold 12pt "Segoe UI";
    color: #27ae60;
}

QLabel#progressLabel {
    font: bold 11pt "Segoe UI";
    color: #3498db;
}

/* Modern CheckBox */
QCheckBox {
    color: #2c3e50;
    font: 10pt "Segoe UI";
    spacing: 8px;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 2px solid #bdc3c7;
    border-radius: 4px;
    background: white;
}

QCheckBox::indicator:checked {
    background: #3498db;
    border: 2px solid #3498db;
    image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iOSIgdmlld0JveD0iMCAwIDEyIDkiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik0xIDQuNUw0LjUgOEwxMSAxIiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPgo8L3N2Zz4K);
}

/* ScrollBar */
QScrollBar:vertical {
    background: rgba(255, 255, 255, 0.1);
    width: 12px;
    border-radius: 6px;
}

QScrollBar::handle:vertical {
    background: rgba(52, 152, 219, 0.8);
    border-radius: 6px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background: rgba(52, 152, 219, 1);
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

/* Tool Tips */
QToolTip {
    background: #2c3e50;
    color: white;
    border: 1px solid #34495e;
    border-radius: 6px;
    padding: 8px;
    font: 9pt "Segoe UI";
}

/* Menu */
QMenu {
    background: rgba(255, 255, 255, 0.95);
    border: 1px solid #e1e8ed;
    border-radius: 8px;
    padding: 5px;
}

QMenu::item {
    padding: 8px 20px;
    border-radius: 4px;
    color: #2c3e50;
}

QMenu::item:selected {
    background: #3498db;
    color: white;
}

/* Dialog */
QDialog {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #667eea, stop:1 #764ba2);
}

/* Status Colors */
.status-live {
    background: #d5f4e6;
    color: #27ae60;
    border: 1px solid #a8e6cf;
}

.status-die {
    background: #fadbd8;
    color: #e74c3c;
    border: 1px solid #f5b7b1;
}

.status-processing {
    background: #d6eaf8;
    color: #3498db;
    border: 1px solid #a9cce3;
}
""" 