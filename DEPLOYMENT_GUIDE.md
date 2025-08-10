# 🚀 Hướng Dẫn Deploy Tool Spam FB Token lên Vercel

## 📋 **Chuẩn bị trước khi deploy:**

### 1️⃣ **Tài khoản cần thiết:**
- ✅ GitHub account
- ✅ Vercel account (đăng ký free tại [vercel.com](https://vercel.com))

### 2️⃣ **Tools cần cài đặt:**
- ✅ Git
- ✅ GitHub Desktop (tùy chọn)

---

## 🔧 **Bước 1: Push code lên GitHub**

### **Cách 1: Sử dụng Git Command Line**

```bash
# 1. Khởi tạo Git repository
git init

# 2. Thêm tất cả files
git add .

# 3. Commit đầu tiên
git commit -m "Initial commit: FB Spam Tool Web Edition"

# 4. Tạo repository trên GitHub rồi link
git remote add origin https://github.com/YOUR_USERNAME/fb-spam-tool-web.git

# 5. Push lên GitHub
git branch -M main
git push -u origin main
```

### **Cách 2: Sử dụng GitHub Desktop**

1. Mở GitHub Desktop
2. Click "Add an Existing Repository"
3. Chọn folder chứa project
4. Commit changes với message: "Initial commit: FB Spam Tool Web Edition"
5. Click "Publish repository" 
6. Chọn tên repository: `fb-spam-tool-web`
7. Click "Publish Repository"

---

## 🌐 **Bước 2: Deploy lên Vercel**

### **Option A: Deploy qua Vercel Dashboard (Khuyến nghị)**

1. **Truy cập Vercel:**
   - Vào [vercel.com](https://vercel.com)
   - Login bằng GitHub account

2. **Import Project:**
   - Click "New Project"
   - Chọn repository `fb-spam-tool-web` từ GitHub
   - Click "Import"

3. **Configure Project:**
   ```
   Project Name: fb-spam-tool-web
   Framework Preset: Other
   Root Directory: ./
   Build Command: (để trống)
   Output Directory: (để trống)
   Install Command: pip install -r requirements.txt
   ```

4. **Environment Variables:**
   ```
   SECRET_KEY = your-secure-secret-key-here
   FLASK_ENV = production
   PORT = 5000
   ```

5. **Deploy:**
   - Click "Deploy"
   - Đợi 2-3 phút để Vercel build và deploy
   - Nhận link website: `https://fb-spam-tool-web.vercel.app`

### **Option B: Deploy qua Vercel CLI**

```bash
# 1. Cài đặt Vercel CLI
npm i -g vercel

# 2. Login Vercel
vercel login

# 3. Deploy
vercel

# 4. Follow prompts:
# - Link to existing project? N
# - Project name: fb-spam-tool-web
# - Directory: ./
# - Override settings? N

# 5. Deploy production
vercel --prod
```

---

## ⚙️ **Bước 3: Environment Variables Setup**

### **Trên Vercel Dashboard:**

1. Vào Project Settings
2. Tab "Environment Variables"
3. Thêm các biến:

```env
SECRET_KEY = fb-tool-secret-key-2024-production
FLASK_ENV = production
PORT = 5000
MAX_CONTENT_LENGTH = 52428800
UPLOAD_FOLDER = /tmp/uploads
```

### **Lưu ý quan trọng:**
- ⚠️ **SECRET_KEY**: Đổi thành key riêng của bạn (random string)
- ⚠️ **Upload**: Vercel sử dụng `/tmp` cho temporary files
- ⚠️ **Database**: Sessions sẽ reset khi function restart (bình thường)

---

## 🔄 **Auto Deploy Setup**

### **GitHub Integration:**
- Vercel tự động deploy khi có commit mới trên main branch
- Mỗi commit → 1 deployment preview
- Main branch → Production deployment

### **Custom Domain (Tùy chọn):**
1. Vào Project Settings → Domains
2. Thêm domain của bạn: `your-domain.com`
3. Configure DNS records theo hướng dẫn

---

## 🐛 **Troubleshooting**

### **Lỗi thường gặp:**

**1. Build Error - Python Version:**
```
Solution: Thêm runtime.txt với nội dung: python-3.9.18
```

**2. Import Error - Module not found:**
```
Solution: Đảm bảo PYTHONPATH được set trong vercel.json
```

**3. SocketIO Connection Error:**
```
Solution: Vercel Serverless không support WebSocket. 
Sử dụng polling mode hoặc deploy lên VPS.
```

**4. File Upload Error:**
```
Solution: Upload sẽ vào /tmp và reset sau mỗi function call.
Consider external storage (AWS S3, Cloudinary).
```

### **Vercel Limitations:**
- ⚠️ **Serverless**: Functions timeout sau 30s
- ⚠️ **Storage**: Files upload reset khi function restart
- ⚠️ **WebSocket**: Không support, chỉ HTTP polling
- ⚠️ **Memory**: Limited memory cho functions

---

## 🌟 **Alternative Deployment Options**

### **Nếu cần WebSocket real-time:**

**1. Railway.app:**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy
railway login
railway init
railway up
```

**2. Render.com:**
- Connect GitHub repo
- Select "Web Service"
- Build: `pip install -r requirements.txt`
- Start: `python app.py`

**3. Heroku:**
```bash
# Install Heroku CLI
heroku create fb-spam-tool-web
git push heroku main
```

---

## ✅ **Checklist Deploy**

### **Trước khi deploy:**
- [ ] Code đã commit và push lên GitHub
- [ ] File vercel.json đã có
- [ ] requirements.txt đầy đủ dependencies
- [ ] .gitignore loại trừ files không cần thiết
- [ ] SECRET_KEY đã đổi thành production key

### **Sau khi deploy:**
- [ ] Website accessible qua Vercel URL
- [ ] Token management hoạt động
- [ ] File upload hoạt động (tạm thời)
- [ ] API endpoints response đúng
- [ ] Logs không có error critical

---

## 🎯 **Production Tips**

### **Security:**
- 🔒 Đổi SECRET_KEY thành random string mạnh
- 🔒 Limit rate limiting cho API endpoints
- 🔒 Add CORS headers nếu cần

### **Performance:**
- ⚡ Optimize images trong static folder
- ⚡ Minify CSS/JS files
- ⚡ Add CDN cho static assets

### **Monitoring:**
- 📊 Sử dụng Vercel Analytics
- 📊 Monitor function execution time
- 📊 Check error logs regularly

---

## 🎉 **Kết quả:**

Sau khi hoàn thành, bạn sẽ có:
- ✅ **Live website**: `https://your-project.vercel.app`
- ✅ **Auto deployment**: Push code → Auto deploy
- ✅ **SSL certificate**: HTTPS automatic
- ✅ **Global CDN**: Fast loading worldwide
- ✅ **99.9% uptime**: Reliable hosting

**🚀 Tool Spam FB Token của bạn đã sẵn sàng phục vụ users trên toàn thế giới!**
