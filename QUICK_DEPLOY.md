# ⚡ Quick Deploy - 5 Phút Deploy Tool lên Web

## 🚀 **TL;DR - Deploy nhanh trong 5 phút:**

### **Bước 1: GitHub (2 phút)**
```bash
# 1. Init git và commit
git init
git add .
git commit -m "FB Spam Tool Web Edition"

# 2. Tạo repo trên GitHub: https://github.com/new
# 3. Tên repo: fb-spam-tool-web

# 4. Link và push
git remote add origin https://github.com/YOUR_USERNAME/fb-spam-tool-web.git
git branch -M main
git push -u origin main
```

### **Bước 2: Vercel Deploy (3 phút)**
1. 🌐 Vào [vercel.com](https://vercel.com) → Login với GitHub
2. 📁 Click "New Project" → Import `fb-spam-tool-web`
3. ⚙️ Settings:
   ```
   Framework: Other
   Root Directory: ./
   Build Command: (để trống)
   Install Command: pip install -r requirements.txt
   ```
4. 🔑 Environment Variables:
   ```
   SECRET_KEY = your-random-secret-key-here
   FLASK_ENV = production
   ```
5. 🚀 Click "Deploy" → Đợi 2-3 phút → Done!

---

## 🎯 **Kết quả:**
- ✅ **Live URL**: `https://fb-spam-tool-web.vercel.app`
- ✅ **Auto Deploy**: Push code → Tự động deploy
- ✅ **HTTPS**: SSL certificate tự động
- ✅ **Global**: CDN worldwide

---

## 🔧 **Auto Deploy Script:**
```bash
python deploy.py
```

---

## ⚠️ **Lưu ý quan trọng:**

### **Vercel Limitations:**
- 🕐 **Timeout**: Functions timeout 30s (OK cho tool này)
- 💾 **Storage**: Upload files sẽ mất khi restart (sessions reset)
- 🔌 **WebSocket**: Không support → Tool sẽ dùng HTTP polling
- 📏 **Size**: 15MB limit cho functions

### **Alternatives nếu cần WebSocket:**
- 🚂 **Railway.app**: Full support, $5/month
- 🎨 **Render.com**: Free tier với limitations
- 🟣 **Heroku**: $7/month sau free tier

---

## 🛠️ **Troubleshooting:**

### **Lỗi Build:**
```bash
# Add runtime.txt
echo "python-3.9.18" > runtime.txt
git add . && git commit -m "Add runtime" && git push
```

### **Lỗi Import:**
```bash
# Check vercel.json có đúng structure
# Check api/index.py imports
```

### **Lỗi Environment:**
```bash
# Vercel Dashboard → Settings → Environment Variables
# Add lại SECRET_KEY và FLASK_ENV
```

---

## 🎉 **Success! Tool đã live:**

Sau deployment, tool sẽ có đầy đủ tính năng:
- ✅ **Token Management** - Thêm/xóa/check tokens
- ✅ **Auto Spam** - Spam comments tự động  
- ✅ **Image Upload** - Upload ảnh (temporary)
- ✅ **Real-time** - Progress tracking (polling mode)
- ✅ **Responsive** - Mobile/tablet compatible

**🌐 Share link với team và enjoy!**
