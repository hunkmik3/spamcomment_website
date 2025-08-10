# 🚀 Tool Spam FB Token - Professional Edition

Một ứng dụng desktop chuyên nghiệp được xây dựng bằng PyQt5 để quản lý và spam comment Facebook một cách tự động và hiệu quả.

## ✨ Tính năng chính

### 🔑 Quản lý Token
- **Nhập token hàng loạt**: Hỗ trợ nhập nhiều token cùng lúc
- **Kiểm tra trạng thái**: Tự động kiểm tra token LIVE/DIE
- **Quản lý thông minh**: Xóa token trùng, token DIE, copy token
- **Rate limiting**: Hệ thống giới hạn tốc độ để tránh bị block

### 🚀 Auto Spam Comment
- **Multi-threading**: Hỗ trợ chạy nhiều thread đồng thời
- **Delay tùy chỉnh**: Cài đặt thời gian delay giữa các comment
- **Comment + Ảnh**: Hỗ trợ gửi comment kèm hình ảnh
- **Auto Like**: Tự động like bài viết sau khi comment

### 💬 Live Chat
- **Gửi comment nhanh**: 2 khu vực live chat riêng biệt
- **Auto fetch page name**: Tự động lấy tên page từ UID
- **Real-time**: Gửi comment ngay lập tức không cần delay

### 📊 Monitoring & Logs
- **Real-time logs**: Theo dõi hoạt động trong thời gian thực
- **Progress tracking**: Hiển thị tiến độ comment
- **Status monitoring**: Theo dõi trạng thái token và tool

## 🛠️ Cài đặt

### Yêu cầu hệ thống
- Python 3.7+
- Windows 10/11 (khuyến nghị)

### Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### Chạy ứng dụng
```bash
python main.py
```

## 📁 Cấu trúc project

```
├── main.py                 # Entry point
├── requirements.txt        # Dependencies
├── README.md              # Documentation
├── .gitignore             # Git ignore rules
├── ui/                    # User Interface
│   ├── __init__.py
│   ├── main_window.py     # Main window
│   └── components/        # UI Components
│       ├── __init__.py
│       ├── token_table.py # Token management table
│       └── add_token_dialog.py # Add token dialog
└── utils/                 # Utilities
    ├── __init__.py
    ├── facebook_api.py    # Facebook API wrapper
    ├── token_manager.py   # Token management logic
    └── styles.py          # UI styling
```

## 🎯 Hướng dẫn sử dụng

### 1. Thêm Token
1. Click "➕ Nhập Token"
2. Nhập các token Facebook (mỗi token một dòng)
3. Click "✅ Thêm Token"

### 2. Kiểm tra Token
1. Chọn các token muốn kiểm tra
2. Right-click → "Kiểm Tra Tokens Đã Chọn"
3. Đợi kết quả LIVE/DIE

### 3. Cài đặt Spam
1. **Min/Max Delay**: Thời gian delay giữa các comment (ms)
2. **Max Threads**: Số luồng chạy đồng thời
3. **Số Comment**: Số comment muốn gửi cho mỗi post
4. **Comment + Ảnh**: Số comment kèm hình ảnh

### 4. Nhập dữ liệu
1. **Post UID**: Nhập UID các bài viết (mỗi UID một dòng)
2. **Comment**: Nhập nội dung comment (mỗi comment một dòng)
3. **Folder Ảnh**: Chọn thư mục chứa ảnh (tùy chọn)

### 5. Chạy Tool
1. Click "▶️ Start Spam"
2. Theo dõi tiến độ trong phần Logs
3. Click "⏹️ Stop" để dừng

### 6. Live Chat
- Sử dụng 2 khu vực Live Chat để gửi comment nhanh
- Nhập Post UID và nội dung comment
- Click "🚀 Gửi Comment Ngay"

## ⚙️ Cài đặt nâng cao

### Rate Limiting
- Hệ thống tự động giới hạn số comment/token
- Tránh bị Facebook block tài khoản

### Image Management
- Hỗ trợ các định dạng: JPG, JPEG, PNG, GIF
- Tự động chọn ảnh ngẫu nhiên cho comment

### Error Handling
- Tự động đánh dấu token DIE khi gặp lỗi
- Log chi tiết các lỗi và hoạt động

## 🔒 Bảo mật

- **Không lưu token**: Token chỉ được lưu trong bộ nhớ
- **Log an toàn**: Không log thông tin nhạy cảm
- **Rate limiting**: Bảo vệ tài khoản khỏi bị block

## ⚠️ Lưu ý quan trọng

1. **Sử dụng có trách nhiệm**: Chỉ spam comment hợp pháp
2. **Tuân thủ ToS**: Tuân thủ Terms of Service của Facebook
3. **Backup token**: Lưu backup token quan trọng
4. **Test trước**: Test với số lượng nhỏ trước khi chạy lớn

## 🐛 Troubleshooting

### Lỗi thường gặp
- **Token không hoạt động**: Kiểm tra lại token hoặc tạo token mới
- **Bị block**: Giảm số thread và tăng delay
- **Lỗi ảnh**: Kiểm tra định dạng và kích thước ảnh

### Log files
- `dead_tokens.log`: Danh sách token đã chết
- Console logs: Thông tin chi tiết trong ứng dụng

## 📞 Hỗ trợ

Nếu gặp vấn đề, vui lòng:
1. Kiểm tra logs trong ứng dụng
2. Đảm bảo token còn hoạt động
3. Thử giảm số thread và tăng delay

## 📄 License

Project này được phát triển cho mục đích giáo dục và nghiên cứu. Người dùng chịu trách nhiệm về việc sử dụng tool.

---

**⚠️ Disclaimer**: Tool này chỉ dành cho mục đích giáo dục. Người dùng phải tuân thủ luật pháp và quy định của Facebook. 