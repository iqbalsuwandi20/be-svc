from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles  # ✅ untuk serving file gambar
from fastapi.middleware.cors import CORSMiddleware
import os

from app.api import auth, users, products
from app.core.database import db


# === Inisialisasi Aplikasi ===
app = FastAPI(
    title="Product Management System API",
    version="1.0.0",
    description=(
        "Backend API untuk sistem manajemen produk. "
        "Mendukung autentikasi JWT, CRUD user & produk, dan integrasi MongoDB."
    ),
)

# === CORS ini di bawah FastAPI ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # sementara izinkan semua asal (bisa ganti nanti)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Konfigurasi Static File (Gambar Upload) ===
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)  # otomatis buat folder kalau belum ada
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")


# === Registrasi Router ===
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(products.router, prefix="/api/v1/products", tags=["Products"])


# === Root Endpoint (Health Check) ===
@app.get("/", tags=["Root"])
def read_root():
    """
    Endpoint utama untuk memastikan API dan koneksi MongoDB berjalan normal.
    """
    try:
        collections = db.list_collection_names()
        return {
            "message": "Welcome to Product Management System API 🚀 — MongoDB Connected ✅",
            "collections": collections,
        }
    except Exception as e:
        return {"error": f"Gagal terhubung ke database: {str(e)}"}
