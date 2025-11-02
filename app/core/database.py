from pymongo import MongoClient
import os

# === Konfigurasi Koneksi MongoDB ===
# ⚠️ Gunakan environment variable untuk keamanan
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

try:
    client = MongoClient(MONGO_URI)
    db = client["product_management"]

    # === Koleksi ===
    users_collection = db["users"]
    products_collection = db["products"]

    print("✅ MongoDB connected successfully.")
except Exception as e:
    print("❌ Failed to connect to MongoDB:", e)
    raise e
