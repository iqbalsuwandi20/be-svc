# 🧩 Product Management System API (be-svc)

Proyek **Backend Service** menggunakan **FastAPI** dan **MongoDB** untuk mengelola data **User**, **Autentikasi (JWT)**, serta **Produk dengan Upload Gambar**.

---

## 🚀 Menjalankan Proyek

### ▶️ Perintah Menjalankan Server

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

Setelah dijalankan, API bisa diakses melalui:

Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc

⚙️ Langkah Instalasi
1️⃣ Buat Virtual Environment
python -m venv venv

2️⃣ Aktifkan Virtual Environment
# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Konfigurasi Koneksi MongoDB
MONGO_URI=mongodb://localhost:27017

📂 Struktur Folder
EVALUASI_SHARING_SESSION/
├── app/
│   ├── api/
│   │   ├── auth.py
│   │   ├── products.py
│   │   └── users.py
│   ├── core/
│   │   ├── database.py
│   │   └── security.py
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── product.py
│   │   └── user.py
│   └── main.py
├── uploads/
├── venv/
├── requirements.txt
└── README.md

🧠 Penjelasan Modul
| Metode | Endpoint             | Deskripsi                                                  |
| ------ | -------------------- | ---------------------------------------------------------- |
| `POST` | `/api/v1/auth/login` | Login menggunakan email & password, menghasilkan JWT token |
| `GET`  | `/api/v1/auth/me`    | Mengambil data user yang sedang login menggunakan token    |

Alur kerja:
Mencari user berdasarkan email di MongoDB.
Memverifikasi password menggunakan bcrypt.
Mengembalikan token JWT jika valid.
Endpoint /me digunakan untuk mendapatkan data user yang sedang login.

👤 users.py

Berfungsi untuk CRUD (Create, Read, Update, Delete) data user.

Endpoint:
| Metode   | Endpoint                  | Deskripsi                       |
| -------- | ------------------------- | ------------------------------- |
| `POST`   | `/api/v1/users/`          | Membuat user baru               |
| `GET`    | `/api/v1/users/`          | Menampilkan semua user          |
| `GET`    | `/api/v1/users/{user_id}` | Menampilkan user berdasarkan ID |
| `PUT`    | `/api/v1/users/{user_id}` | Mengubah data user              |
| `DELETE` | `/api/v1/users/{user_id}` | Menghapus user berdasarkan ID   |

Catatan:
Password di-hash otomatis menggunakan bcrypt.
Email dicek agar tidak duplikat sebelum disimpan.

🛒 products.py

Berfungsi untuk mengelola produk (CRUD) dan upload gambar produk.

Endpoint:
| Metode   | Endpoint                        | Deskripsi                                      |
| -------- | ------------------------------- | ---------------------------------------------- |
| `POST`   | `/api/v1/products/`             | Tambah produk baru (dengan opsi upload gambar) |
| `GET`    | `/api/v1/products/`             | Ambil semua produk milik user login            |
| `GET`    | `/api/v1/products/{product_id}` | Ambil detail produk berdasarkan ID             |
| `PUT`    | `/api/v1/products/{product_id}` | Update produk dan gambar (jika ada)            |
| `DELETE` | `/api/v1/products/{product_id}` | Hapus produk milik user login                  |

Ketentuan Upload:
Format gambar: .jpg, .jpeg, .png
Ukuran maksimal: 2 MB
Disimpan di folder /uploads
URL gambar akan otomatis disimpan di database
Contoh: http://192.168.0.102:8000/uploads/namafile.png

Catatan tambahan:
Tiap produk terhubung dengan user melalui owner_id (berasal dari token JWT).
Field low_stock_limit akan diabaikan jika is_active bernilai False.

⚙️ core/database.py
Mengatur koneksi ke MongoDB dan membuat objek koleksi:
users_collection = db["users"]
products_collection = db["products"]

Database default: product_management.

🔒 core/security.py
Berisi fungsi untuk keamanan dan autentikasi JWT:
get_password_hash(password) → Hash password
verify_password(plain, hashed) → Verifikasi password
create_access_token(data) → Buat token JWT
get_current_user() → Mengambil user aktif dari token Bearer

📘 schemas/
Berisi definisi model data menggunakan Pydantic.
| File         | Fungsi                                   |
| ------------ | ---------------------------------------- |
| `auth.py`    | Schema login & token                     |
| `product.py` | Schema tambah, update, dan respon produk |
| `user.py`    | Schema pembuatan dan respon user         |

🧭 main.py
File utama aplikasi FastAPI.
Tugas:
Mendaftarkan router (auth, users, products)
Mengatur CORS agar API bisa diakses dari frontend
Melayani file gambar statis dari folder /uploads
Endpoint utama / sebagai health check MongoDB
Contoh respon:
{
  "message": "Welcome to Product Management System API 🚀 — MongoDB Connected ✅"
}

🧾 Contoh Request API
🔑 Login
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "admin@example.com",
  "password": "123456"
}

✅ Response:
{
  "access_token": "xxxxx.yyyyy.zzzzz",
  "token_type": "bearer"
}

👤 Tambah User Baru
POST /api/v1/users/
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "password123"
}

🛍️ Tambah Produk
POST /api/v1/products/
Authorization: Bearer <token>
Content-Type: multipart/form-data

data: {
  "name": "Meja Makan Kayu Jati",
  "category": "Furniture",
  "price": 3500000,
  "stock": 10,
  "unit": "pcs",
  "is_active": true
}
image: <optional file>

🧹 Hapus Produk
DELETE /api/v1/products/{product_id}
Authorization: Bearer <token>


✅ Response:

{ "message": "Produk berhasil dihapus ✅" }

🧪 Pengujian dengan Swagger

Jalankan server:

uvicorn app.main:app --reload


Buka:

http://127.0.0.1:8000/docs


Klik tombol Authorize → masukkan token JWT dari hasil login.

Coba semua endpoint langsung dari halaman Swagger.

📁 Uploads & Gambar

Semua gambar yang diupload disimpan di folder:

/uploads


Dapat diakses melalui URL:

http://127.0.0.1:8000/uploads/<nama_file>.png


Contoh:

http://127.0.0.1:8000/uploads/20241103121045_meja_jati.png

🧩 Teknologi yang Digunakan

FastAPI – Framework utama backend

MongoDB – Database NoSQL

Uvicorn – ASGI server

Passlib (bcrypt) – Hashing password

Python-JOSE (JWT) – Autentikasi token

Pydantic v2 – Validasi data schema

CORS Middleware – Akses API dari frontend

🧠 Catatan Penting

Semua endpoint yang membutuhkan login wajib menggunakan Bearer Token.

Ubah BASE_URL di products.py sesuai alamat IP server kamu.

Gunakan .env untuk menyimpan informasi sensitif seperti SECRET_KEY atau MONGO_URI.

---
