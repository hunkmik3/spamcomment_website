# 🚀 Tool Spam FB Token - Professional Web Edition

Phiên bản web của tool Spam Comment Facebook với giao diện hiện đại, responsive và đầy đủ chức năng như phiên bản desktop.

## ✨ Tính Năng Chính

### 🔑 Quản Lý Token
- **Nhập token hàng loạt**: Hỗ trợ nhập nhiều token cùng lúc qua giao diện web
- **Kiểm tra trạng thái**: Tự động kiểm tra token LIVE/DIE với real-time updates
- **Quản lý thông minh**: Xóa token trùng, token DIE, copy token qua web interface
- **Rate limiting**: Hệ thống giới hạn tốc độ để tránh bị block
- **Session-based**: Mỗi người dùng có session riêng biệt

### 🚀 Auto Spam Comment  
- **Multi-threading**: Hỗ trợ chạy nhiều thread đồng thời
- **Delay tùy chỉnh**: Cài đặt thời gian delay giữa các comment
- **Comment + Ảnh**: Hỗ trợ upload và gửi comment kèm hình ảnh
- **Auto Like**: Tự động like bài viết sau khi comment
- **Real-time progress**: Theo dõi tiến độ comment trên web



### 📊 Monitoring & Logs
- **Real-time logs**: Theo dõi hoạt động trong thời gian thực qua WebSocket
- **Progress tracking**: Hiển thị tiến độ comment với progress bar
- **Status monitoring**: Dashboard theo dõi trạng thái token và tool
- **Statistics**: Thống kê chi tiết về tokens và comments

### 🌐 Web Features
- **Responsive Design**: Giao diện responsive với Bootstrap 5
- **Real-time Updates**: WebSocket cho cập nhật tức thì
- **File Upload**: Drag & drop upload ảnh với preview
- **Session Management**: Quản lý session riêng biệt cho mỗi user
- **Modern UI**: Giao diện hiện đại với animations và effects

## 🛠️ Cài Đặt & Chạy

### Yêu cầu hệ thống
- Python 3.8+
- Trình duyệt web hiện đại (Chrome, Firefox, Safari, Edge)

### 1. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 2. Cấu hình environment (tùy chọn)
Tạo file `.env`:
```env
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
PORT=5000
```

### 3. Chạy ứng dụng

#### Development Mode
```bash
python app.py
```

#### Production Mode với Gunicorn
```bash
gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:5000 app:app
```

### 4. Truy cập ứng dụng
Mở trình duyệt và truy cập: `http://localhost:5000`

## 📁 Cấu Trúc Project

```
├── app.py                      # Flask application chính
├── requirements.txt            # Python dependencies
├── README_WEB.md              # Documentation cho web version
├── models/                    # Models và business logic
│   ├── __init__.py
│   ├── facebook_api.py        # Facebook API wrapper cho web
│   ├── token_manager.py       # Token management với session support
│   └── spam_manager.py        # Spam management với WebSocket
├── templates/                 # HTML templates
│   ├── base.html             # Base template với Bootstrap
│   ├── index.html            # Main dashboard
│   ├── 404.html              # Error pages
│   ├── 500.html
│   └── modals/               # Modal templates
│       ├── add_tokens.html
│       ├── upload_images.html
│       └── token_details.html
├── static/                   # Static files
│   ├── css/
│   │   └── main.css         # Custom CSS với responsive design
│   ├── js/
│   │   └── main.js          # JavaScript với AJAX và WebSocket
│   └── images/              # Static images
├── utils/                   # Utility functions
│   ├── __init__.py
│   └── helpers.py          # Helper functions cho web
└── uploads/                # Upload folder cho images
    ├── images/             # User uploaded images (by session)
    └── temp/              # Temporary files
```

## 🎯 Hướng Dẫn Sử Dụng

### 1. Thêm Token
1. Click "➕ Nhập Token" 
2. Dán các token Facebook vào textarea (mỗi token một dòng)
3. Click "✅ Thêm Token"
4. Hệ thống sẽ tự động loại bỏ token trùng lặp

### 2. Kiểm Tra Token
1. Chọn các token cần kiểm tra bằng checkbox
2. Click "🔍 Kiểm Tra Đã Chọn"
3. Theo dõi tiến độ kiểm tra real-time
4. Kết quả sẽ hiển thị màu xanh (LIVE) hoặc đỏ (DIE)

### 3. Upload Ảnh
1. Click "📁 Upload Ảnh"
2. Chọn file hoặc kéo thả ảnh vào vùng upload
3. Preview ảnh được chọn
4. Click "📤 Upload Ảnh"
5. Ảnh sẽ được sử dụng cho comment kèm ảnh

### 4. Cài Đặt Spam
- **Min/Max Delay**: Thời gian delay giữa các comment (milliseconds)
- **Max Threads**: Số luồng chạy đồng thời  
- **Số Comment**: Số comment muốn gửi cho mỗi post
- **Comment + Ảnh**: Số comment kèm hình ảnh
- **Auto Like**: Tự động like bài viết sau khi comment

### 5. Nhập Dữ Liệu
1. **Post UID**: Nhập UID các bài viết (mỗi UID một dòng)
   - Hệ thống tự động fetch tên page từ UID
2. **Comment**: Nhập nội dung comment (mỗi comment một dòng)

### 6. Chạy Auto Spam
1. Điền đầy đủ thông tin cài đặt
2. Click "▶️ Start Spam"
3. Theo dõi tiến độ qua progress bar và logs real-time
4. Click "⏹️ Stop" để dừng bất cứ lúc nào



## ⚙️ API Endpoints

### Token Management
- `GET /api/tokens` - Lấy danh sách tokens
- `POST /api/tokens` - Thêm tokens mới
- `POST /api/tokens/check` - Kiểm tra trạng thái tokens
- `POST /api/tokens/delete` - Xóa tokens

### File Management
- `POST /api/upload` - Upload ảnh
- `GET /api/images` - Lấy danh sách ảnh đã upload

### Page Information
- `POST /api/page-info` - Lấy thông tin page từ UID

### Spam Management  
- `POST /api/spam/start` - Bắt đầu spam comments
- `POST /api/spam/stop` - Dừng spam comments
- `GET /api/spam/status` - Lấy trạng thái spam



### WebSocket Events
- `connect/disconnect` - Kết nối WebSocket
- `token_check_progress` - Tiến độ kiểm tra token
- `tokens_checked` - Kết quả kiểm tra token
- `spam_started/progress/completed/stopped` - Events cho spam process


## 🔒 Bảo Mật

- **Session-based**: Mỗi user có session riêng, tokens không chia sẻ
- **No persistent storage**: Tokens chỉ lưu trong memory, tự động xóa khi hết session
- **Rate limiting**: Bảo vệ tài khoản khỏi bị Facebook block
- **Input validation**: Validate và sanitize tất cả input từ user
- **Secure file upload**: Kiểm tra file type và kích thước upload

## 🚀 Deployment

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["gunicorn", "--worker-class", "eventlet", "-w", "1", "--bind", "0.0.0.0:5000", "app:app"]
```

### Heroku Deployment
1. Tạo `Procfile`:
```
web: gunicorn --worker-class eventlet -w 1 app:app
```

2. Deploy:
```bash
git init
git add .
git commit -m "Initial commit"
heroku create your-app-name
git push heroku main
```

### VPS Deployment với Nginx
1. Install dependencies và chạy app với Gunicorn
2. Cấu hình Nginx reverse proxy:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /socket.io/ {
        proxy_pass http://127.0.0.1:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## ⚠️ Lưu Ý Quan Trọng

1. **Sử dụng có trách nhiệm**: Chỉ spam comment hợp pháp và phù hợp
2. **Tuân thủ ToS**: Tuân thủ Terms of Service của Facebook
3. **Backup token**: Lưu backup token quan trọng vì session có thể hết hạn
4. **Test trước**: Test với số lượng nhỏ trước khi chạy số lượng lớn
5. **Monitor rate limits**: Theo dõi rate limiting để tránh bị block

## 🐛 Troubleshooting

### Lỗi thường gặp
- **Token không hoạt động**: Kiểm tra lại token hoặc tạo token mới
- **Bị block**: Giảm số thread và tăng delay
- **Lỗi upload ảnh**: Kiểm tra định dạng và kích thước ảnh (max 50MB)
- **WebSocket disconnect**: Refresh trang hoặc kiểm tra kết nối internet

### Performance Optimization
- Giảm số threads nếu server yếu
- Tăng delay nếu bị rate limit
- Sử dụng ảnh có kích thước nhỏ hơn
- Clean up session định kỳ

## 📞 Hỗ Trợ

Nếu gặp vấn đề:
1. Kiểm tra logs trong ứng dụng (màn hình logs real-time)
2. Đảm bảo tokens còn hoạt động  
3. Thử giảm số thread và tăng delay
4. Refresh trang web nếu WebSocket bị disconnect

## 📄 License

Project này được phát triển cho mục đích giáo dục và nghiên cứu. Người dùng chịu trách nhiệm về việc sử dụng tool.

---

**⚠️ Disclaimer**: Tool này chỉ dành cho mục đích giáo dục. Người dùng phải tuân thủ luật pháp và quy định của Facebook.
