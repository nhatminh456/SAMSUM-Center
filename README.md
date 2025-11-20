# 📱 SAMSUM E-COMMERCE WEB APPLICATION

> Ứng dụng web bán điện thoại Samsung với Flask Backend API + Vue.js Frontend

---

## 🎯 GIỚI THIỆU

Project **Samsum** là một ứng dụng web e-commerce hoàn chỉnh, được xây dựng với:
- **Backend**: Flask (Python) + SQLite Database
- **Frontend**: Vue.js 3 + Vue Router + Pinia
- **UI/UX**: Bootstrap, Responsive Design

---

## ✨ TÍNH NĂNG CHÍNH

### Người dùng:
- 🔐 Đăng ký / Đăng nhập tài khoản
- 📱 Xem danh sách sản phẩm (40+ điện thoại Samsung)
- 🔍 Tìm kiếm sản phẩm
- 📂 Lọc theo danh mục (S-Series, A-Series, M-Series, Z-Series)
- ⭐ Xem sản phẩm bán chạy (Best Sellers)
- 📄 Xem chi tiết sản phẩm
- 🛒 Thêm vào giỏ hàng
- 💳 Thanh toán đơn hàng
- 📜 Xem lịch sử mua hàng

### Admin:
- ➕ Thêm sản phẩm mới
- ✏️ Sửa thông tin sản phẩm
- 🗑️ Xóa sản phẩm
- 📊 Quản lý đơn hàng

---

## 🛠️ CÔNG NGHỆ SỬ DỤNG

### Backend:
- **Flask 3.0** - Python web framework
- **SQLAlchemy** - ORM (Object-Relational Mapping)
- **SQLite** - Database
- **Flask-CORS** - Cross-Origin Resource Sharing

### Frontend:
- **Vue 3** - Progressive JavaScript Framework
- **Vue Router** - Routing
- **Pinia** - State Management
- **Bootstrap** - CSS Framework
- **Axios** - HTTP Client

---

## 📋 YÊU CẦU HỆ THỐNG

- **Python 3.8+**
- **Node.js 14+** & npm
- **Git** (optional)
- **Modern Web Browser** (Chrome, Firefox, Edge)

---

## 🚀 HƯỚNG DẪN CÀI ĐẶT

### Phương án 1: Sử dụng File .bat (Khuyến nghị - Windows)

1. **Cài đặt Python** (nếu chưa có):
   - Tải tại: https://www.python.org/downloads/
   - ⚠️ **Nhớ tick "Add Python to PATH"**

2. **Migrate dữ liệu**:
   - Double-click: `RunMigration.bat`
   - Chờ script chạy xong

3. **Chạy Flask Server**:
   - Double-click: `RunFlaskServer.bat`
   - Server sẽ chạy tại: http://localhost:5000

4. **Chạy Vue Frontend** (Terminal mới):
   - Double-click: `RunServe.bat` (trong folder Samsum)
   - App sẽ chạy tại: http://localhost:8080

### Phương án 2: Thủ công (Tất cả hệ điều hành)

**Backend:**
```bash
cd backend
python -m pip install -r requirements.txt
python migrate_data.py
python app.py
```

**Frontend:** (Terminal mới)
```bash
cd Samsum
npm install
npm run serve
```

---

## 📁 CẤU TRÚC PROJECT

```
Samsum/
├── backend/                    # Flask Backend API
│   ├── app.py                 # Main Flask application
│   ├── models.py              # Database models
│   ├── routes.py              # API endpoints
│   ├── migrate_data.py        # Data migration script
│   ├── requirements.txt       # Python dependencies
│   ├── README.md              # Backend docs
│   └── samsum.db              # SQLite database (auto-created)
│
├── Samsum/                    # Vue.js Frontend
│   ├── src/
│   │   ├── components/        # Vue components
│   │   ├── router/            # Vue Router
│   │   ├── stores/            # Pinia stores
│   │   ├── assets/            # Images, CSS
│   │   ├── App.vue            # Main Vue component
│   │   ├── main.js            # Entry point
│   │   └── constaint.js       # API configuration
│   ├── public/                # Static files
│   ├── package.json           # npm dependencies
│   └── vue.config.js          # Vue config
│
├── RunFlaskServer.bat         # Quick start Flask (Windows)
├── RunMigration.bat           # Quick migration (Windows)
├── SETUP_GUIDE.md             # Chi tiết hướng dẫn
└── FLASK_BACKEND_SUMMARY.md   # Tóm tắt Flask backend
```

---

## 🌐 API ENDPOINTS

### Products:
```
GET    /api/products                    # Tất cả sản phẩm
GET    /api/products/:id                # Chi tiết sản phẩm
GET    /api/products/category/:id       # Theo danh mục
GET    /api/products/bestseller         # Sản phẩm bán chạy
GET    /api/products/search?q=...       # Tìm kiếm
POST   /api/products                    # Tạo mới
PUT    /api/products/:id                # Cập nhật
DELETE /api/products/:id                # Xóa
```

### Users:
```
POST   /api/users/register              # Đăng ký
POST   /api/users/login                 # Đăng nhập
GET    /api/users                       # Danh sách users
GET    /api/users/:id                   # Chi tiết user
```

### Cart:
```
GET    /api/cart/:userId                # Giỏ hàng theo user
POST   /api/cart                        # Thêm vào giỏ
PUT    /api/cart/:id                    # Cập nhật
DELETE /api/cart/:id                    # Xóa item
DELETE /api/cart/clear/:userId          # Xóa toàn bộ
```

### Orders:
```
GET    /api/orders                      # Tất cả đơn hàng
GET    /api/orders/:userId              # Đơn hàng theo user
POST   /api/orders                      # Tạo đơn hàng
```

---

## 🗄️ DATABASE SCHEMA

### Users
- id (String, PK)
- email (String, Unique)
- password (String)
- created_at (DateTime)

### Categories
- id (Integer, PK)
- tenDM (String) - Tên danh mục

### Products
- id (String, PK)
- tenSP (String) - Tên sản phẩm
- gia (Integer) - Giá
- categoryID (Integer, FK)
- image (String)
- mota (Text) - Mô tả
- namSX (Integer) - Năm sản xuất
- thongso (Text) - Thông số kỹ thuật
- bestSeller (Boolean)

### Cart
- id (Integer, PK)
- user_id (String, FK)
- product_id (String, FK)
- quantity (Integer)
- created_at (DateTime)

### Orders
- id (Integer, PK)
- user_id (String, FK)
- total_amount (Integer)
- status (String)
- created_at (DateTime)

---

## ✅ ĐÁP ỨNG YÊU CẦU ĐỀ BÀI

| Yêu cầu | Hoàn thành |
|---------|-----------|
| Python Framework (Flask/Django) | ✅ Flask 3.0 |
| Web Interface (HTML/CSS/JS) | ✅ Vue.js + Bootstrap |
| CRUD Operations | ✅ Full CRUD |
| Database (SQLite) | ✅ SQLite + SQLAlchemy |
| Form & Validation | ✅ Server-side validation |
| Routing & HTTP Requests | ✅ RESTful API |
| Authentication | ✅ Login/Register |
| Responsive Design | ✅ Bootstrap responsive |

---

## 🧪 TESTING

### Test API:
```bash
# Health check
curl http://localhost:5000/api/health

# Get all products
curl http://localhost:5000/api/products

# Login
curl -X POST http://localhost:5000/api/users/login \
  -H "Content-Type: application/json" \
  -d '{"email":"tranminh29012005@gmail.com","password":"123"}'
```

### Test Frontend:
1. Mở: http://localhost:8080
2. Đăng nhập với: `tranminh29012005@gmail.com` / `123`
3. Thêm sản phẩm vào giỏ hàng
4. Thanh toán

---

## 📸 SCREENSHOTS

*(Thêm screenshots của ứng dụng nếu cần)*

---

## 🔐 SECURITY NOTES

⚠️ **Lưu ý**: Project này là phiên bản demo/học tập:
- Password chưa được hash
- Không có JWT authentication
- Không có rate limiting
- SQLite không phù hợp production

**Cải thiện cho Production:**
- Sử dụng bcrypt để hash password
- Implement JWT tokens
- Chuyển sang PostgreSQL/MySQL
- Thêm input sanitization
- HTTPS/SSL

---

## 🚀 DEPLOYMENT (Optional)

### Backend (PythonAnywhere):
1. Tạo account tại pythonanywhere.com
2. Upload code
3. Configure WSGI
4. Setup database

### Frontend (Netlify/Vercel):
1. Build: `npm run build`
2. Deploy folder `dist/`

---

## 📝 TODO / IMPROVEMENTS

- [ ] Hash passwords với bcrypt
- [ ] JWT authentication
- [ ] Product images upload
- [ ] Admin dashboard
- [ ] Order history details
- [ ] Product reviews & ratings
- [ ] Email notifications
- [ ] Payment gateway integration
- [ ] Deploy to production

---

## 👥 CREDITS

- **Developer**: [Your Name]
- **Framework**: Flask + Vue.js
- **Database**: SQLite
- **UI**: Bootstrap

---

## 📞 SUPPORT

Nếu gặp vấn đề:
1. Xem file `SETUP_GUIDE.md`
2. Xem file `FLASK_BACKEND_SUMMARY.md`
3. Kiểm tra log terminal
4. Kiểm tra Python đã cài đúng chưa

---

## 📄 LICENSE

MIT License - Free to use for educational purposes

---

**🎉 Chúc bạn thành công với project!**
