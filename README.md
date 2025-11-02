# 🧩 Product Management System API

Backend Service menggunakan **FastAPI** dan **MongoDB** untuk mengelola data User, Autentikasi (JWT), serta Produk dengan Upload Gambar.

---

## 📋 Daftar Isi

- [Fitur Utama](#-fitur-utama)
- [Teknologi](#-teknologi-yang-digunakan)
- [Instalasi](#-instalasi)
- [Menjalankan Proyek](#-menjalankan-proyek)
- [Struktur Folder](#-struktur-folder)
- [API Endpoints](#-api-endpoints)
- [Contoh Request](#-contoh-request-api)
- [Upload Gambar](#-upload-gambar)
- [Catatan Penting](#-catatan-penting)

---

## ✨ Fitur Utama

- 🔐 **Autentikasi JWT** - Login aman dengan token
- 👥 **User Management** - CRUD lengkap untuk user
- 🛍️ **Product Management** - Kelola produk dengan upload gambar
- 📸 **Image Upload** - Support upload gambar produk (JPG, PNG)
- 🔒 **Password Hashing** - Keamanan password dengan bcrypt
- 📊 **MongoDB** - Database NoSQL yang scalable
- 📚 **Auto Documentation** - Swagger UI & ReDoc

---

## 🛠️ Teknologi yang Digunakan

| Teknologi | Kegunaan |
|-----------|----------|
| **FastAPI** | Framework backend modern |
| **MongoDB** | Database NoSQL |
| **Uvicorn** | ASGI server |
| **Passlib (bcrypt)** | Hashing password |
| **Python-JOSE** | JWT authentication |
| **Pydantic v2** | Validasi data schema |
| **CORS Middleware** | Akses dari frontend |

---

## 🎥 Screen Recording Demo

Lihat demo lengkap penggunaan API dengan Swagger UI:

👉 **[Klik di sini untuk menonton Screen Recording](https://drive.google.com/drive/folders/1GfCd1oXINHK0LLYxwE6Qx4eyBe2o0q44?usp=sharing)**

Video ini menunjukkan:
- ✅ Cara login dan mendapatkan JWT token
- ✅ Menggunakan Swagger UI untuk testing
- ✅ CRUD operations untuk Users & Products
- ✅ Upload gambar produk
- ✅ Testing semua endpoint

---

## 📦 Instalasi

### 1️⃣ Clone Repository

```bash
git clone <repository-url>
cd EVALUASI_SHARING_SESSION
```

### 2️⃣ Buat Virtual Environment

```bash
python -m venv venv
```

### 3️⃣ Aktifkan Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Linux / macOS:**
```bash
source venv/bin/activate
```

### 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 5️⃣ Konfigurasi Environment

Buat file `.env` di root folder:

```env
MONGO_URI=mongodb://localhost:27017
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## 🚀 Menjalankan Proyek

### Jalankan Server

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Akses Dokumentasi API

- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **Health Check:** [http://localhost:8000/](http://localhost:8000/)

---

## 📂 Struktur Folder

```
EVALUASI_SHARING_SESSION/
├── app/
│   ├── api/
│   │   ├── auth.py          # Endpoint autentikasi
│   │   ├── products.py      # Endpoint produk
│   │   └── users.py         # Endpoint users
│   ├── core/
│   │   ├── database.py      # Koneksi MongoDB
│   │   └── security.py      # JWT & password hashing
│   ├── schemas/
│   │   ├── auth.py          # Schema autentikasi
│   │   ├── product.py       # Schema produk
│   │   └── user.py          # Schema user
│   └── main.py              # Entry point aplikasi
├── uploads/                 # Folder penyimpanan gambar
├── venv/                    # Virtual environment
├── requirements.txt         # Dependencies
└── README.md               # Dokumentasi
```

---

## 🔌 API Endpoints

### 🔐 Authentication (`/api/v1/auth`)

| Method | Endpoint | Deskripsi | Auth Required |
|--------|----------|-----------|---------------|
| `POST` | `/login` | Login dan dapatkan JWT token | ❌ |
| `GET` | `/me` | Ambil data user yang login | ✅ |

**Alur Kerja:**
1. User login dengan email & password
2. Server verifikasi password dengan bcrypt
3. Jika valid, server return JWT token
4. Token digunakan untuk akses endpoint protected

---

### 👤 Users (`/api/v1/users`)

| Method | Endpoint | Deskripsi | Auth Required |
|--------|----------|-----------|---------------|
| `POST` | `/` | Buat user baru | ❌ |
| `GET` | `/` | Lihat semua user | ✅ |
| `GET` | `/{user_id}` | Lihat detail user | ✅ |
| `PUT` | `/{user_id}` | Update data user | ✅ |
| `DELETE` | `/{user_id}` | Hapus user | ✅ |

**Fitur:**
- Password otomatis di-hash dengan bcrypt
- Email harus unique (tidak boleh duplikat)
- Validasi input menggunakan Pydantic

---

### 🛒 Products (`/api/v1/products`)

| Method | Endpoint | Deskripsi | Auth Required |
|--------|----------|-----------|---------------|
| `POST` | `/` | Tambah produk baru | ✅ |
| `GET` | `/` | Lihat semua produk milik user | ✅ |
| `GET` | `/{product_id}` | Lihat detail produk | ✅ |
| `PUT` | `/{product_id}` | Update produk | ✅ |
| `DELETE` | `/{product_id}` | Hapus produk | ✅ |

**Fitur:**
- Upload gambar produk (opsional)
- Setiap produk terhubung dengan user melalui `owner_id`
- Field `low_stock_limit` diabaikan jika `is_active = False`
- Gambar disimpan di folder `/uploads`

---

## 📝 Contoh Request API

### 🔑 Login

**Request:**
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "admin@example.com",
  "password": "123456"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

### 👤 Buat User Baru

**Request:**
```http
POST /api/v1/users/
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "id": "507f1f77bcf86cd799439011",
  "username": "john_doe",
  "email": "john@example.com",
  "created_at": "2024-11-03T10:30:00"
}
```

---

### 🛍️ Tambah Produk dengan Gambar

**Request:**
```http
POST /api/v1/products/
Authorization: Bearer <your-token>
Content-Type: multipart/form-data

name: Meja Makan Kayu Jati
category: Furniture
price: 3500000
stock: 10
unit: pcs
is_active: true
image: <file>
```

**Response:**
```json
{
  "id": "507f1f77bcf86cd799439012",
  "name": "Meja Makan Kayu Jati",
  "category": "Furniture",
  "price": 3500000,
  "stock": 10,
  "unit": "pcs",
  "is_active": true,
  "image_url": "http://192.168.0.102:8000/uploads/20241103121045_meja_jati.png",
  "owner_id": "507f1f77bcf86cd799439011",
  "created_at": "2024-11-03T12:10:45"
}
```

---

### 🗑️ Hapus Produk

**Request:**
```http
DELETE /api/v1/products/{product_id}
Authorization: Bearer <your-token>
```

**Response:**
```json
{
  "message": "Produk berhasil dihapus ✅"
}
```

---

## 📸 Upload Gambar

### Ketentuan Upload

- **Format:** `.jpg`, `.jpeg`, `.png`
- **Ukuran maksimal:** 2 MB
- **Lokasi:** `/uploads` folder
- **Akses:** `http://localhost:8000/uploads/<filename>`

### Contoh URL Gambar

```
http://127.0.0.1:8000/uploads/20241103121045_meja_jati.png
```

**Naming Convention:**
```
<timestamp>_<original_filename>
```

---

## 🧪 Testing dengan Swagger UI

### Langkah-langkah:

1. **Jalankan server:**
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Buka Swagger UI:**
   ```
   http://127.0.0.1:8000/docs
   ```

3. **Login untuk dapat token:**
   - Klik endpoint `POST /api/v1/auth/login`
   - Masukkan email & password
   - Copy token dari response

4. **Authorize:**
   - Klik tombol **🔒 Authorize** di kanan atas
   - Masukkan: `Bearer <your-token>`
   - Klik **Authorize**

5. **Test endpoint protected:**
   - Sekarang semua endpoint yang butuh auth bisa dicoba

---

## 📌 Catatan Penting

### Security

- ⚠️ **Jangan hardcode SECRET_KEY** - Gunakan file `.env`
- 🔒 **Password selalu di-hash** dengan bcrypt
- 🎫 **Token JWT expire** setelah waktu yang ditentukan
- 🚫 **Endpoint protected** butuh Bearer token

### Configuration

- 📡 **Ubah BASE_URL** di `products.py` sesuai IP server Anda
- 🗄️ **Database default:** `product_management`
- 📁 **Folder uploads** harus writeable

### Production Checklist

- [ ] Set `SECRET_KEY` yang strong di `.env`
- [ ] Gunakan MongoDB connection string production
- [ ] Disable `--reload` di uvicorn
- [ ] Set proper CORS origins
- [ ] Gunakan HTTPS untuk production
- [ ] Setup proper file upload limits
- [ ] Backup database secara berkala

---
