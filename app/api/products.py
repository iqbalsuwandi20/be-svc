from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File, Form
from bson import ObjectId
from datetime import datetime
import os
import json

from app.core.database import products_collection
from app.core.security import get_current_user
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse

router = APIRouter(prefix="/api/v1/products", tags=["Products"])

BASE_URL = "http://192.168.0.102:8000"

# === Konfigurasi Upload ===
UPLOAD_DIR = "uploads"
MAX_FILE_SIZE = 2 * 1024 * 1024  # 2 MB
os.makedirs(UPLOAD_DIR, exist_ok=True)


# === Helper ===
def product_helper(product) -> dict:
    """Konversi dokumen MongoDB ke format JSON-friendly"""
    return {
        "id": str(product["_id"]),
        "name": product["name"],
        "category": product["category"],
        "description": product.get("description"),
        "price": product["price"],
        "stock": product["stock"],
        "unit": product["unit"],
        "is_active": product["is_active"],
        "low_stock_limit": product.get("low_stock_limit"),
        "image_url": product.get("image_url"),
        "owner_id": str(product["owner_id"]),
    }


# === CREATE PRODUCT ===
@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    data: str = Form(...),  # JSON dikirim dalam bentuk string
    image: UploadFile = File(None),
    current_user=Depends(get_current_user),
):
    """
    Tambah produk baru dengan field JSON + upload gambar.
    """
    # === Parse JSON data ===
    try:
        product_data = json.loads(data)
        product = ProductCreate(**product_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid JSON format: {e}"
        )

    # === Validasi & Upload Gambar ===
    image_url = None
    if image:
        if not image.content_type.startswith("image/"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File harus berupa gambar (.jpg, .jpeg, .png)"
            )

        contents = await image.read()
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ukuran gambar maksimal 2MB"
            )

        filename = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{image.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        with open(file_path, "wb") as f:
            f.write(contents)

        image_url = f"{BASE_URL}/uploads/{filename}"

    # === Logika Status Produk ===
    if not product.is_active:
        product.low_stock_limit = None  # abaikan field kalau produk nonaktif

    # === Simpan ke MongoDB ===
    new_product = product.dict()
    new_product["image_url"] = image_url
    new_product["owner_id"] = current_user["sub"]

    result = products_collection.insert_one(new_product)
    created_product = products_collection.find_one({"_id": result.inserted_id})

    return product_helper(created_product)


# === GET ALL PRODUCTS ===
@router.get("/", response_model=list[ProductResponse], status_code=status.HTTP_200_OK)
def get_all_products(current_user=Depends(get_current_user)):
    """
    Ambil semua produk milik user yang sedang login.
    """
    products = products_collection.find({"owner_id": current_user["sub"]})
    return [product_helper(p) for p in products]


# === GET PRODUCT BY ID ===
@router.get("/{product_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK)
def get_product_by_id(product_id: str, current_user=Depends(get_current_user)):
    """
    Ambil detail produk berdasarkan ID (hanya milik user yang login).
    """
    product = products_collection.find_one({
        "_id": ObjectId(product_id),
        "owner_id": current_user["sub"],
    })

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produk tidak ditemukan atau bukan milikmu"
        )

    return product_helper(product)


# === UPDATE PRODUCT ===
@router.put("/{product_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK)
async def update_product(
    product_id: str,
    data: str = Form(...),
    image: UploadFile = File(None),
    current_user=Depends(get_current_user),
):
    """
    Update produk (JSON + optional gambar baru)
    """
    # === Parse JSON ===
    try:
        update_data = json.loads(data)
        update_product = ProductUpdate(**update_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid JSON format: {e}"
        )

    update_dict = {k: v for k, v in update_product.dict().items() if v is not None}

    # === Kalau ada gambar baru ===
    if image:
        if not image.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File harus berupa gambar")

        contents = await image.read()
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="Ukuran gambar maksimal 2MB")

        filename = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{image.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        with open(file_path, "wb") as f:
            f.write(contents)

        update_dict["image_url"] = f"{BASE_URL}/uploads/{filename}"

    # === Update ke MongoDB ===
    result = products_collection.update_one(
        {"_id": ObjectId(product_id), "owner_id": current_user["sub"]},
        {"$set": update_dict},
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Produk tidak ditemukan atau bukan milikmu")

    updated_product = products_collection.find_one({"_id": ObjectId(product_id)})
    return product_helper(updated_product)



# === DELETE PRODUCT ===
@router.delete("/{product_id}", status_code=status.HTTP_200_OK)
def delete_product(product_id: str, current_user=Depends(get_current_user)):
    """
    Hapus produk milik user yang sedang login.
    """
    result = products_collection.delete_one({
        "_id": ObjectId(product_id),
        "owner_id": current_user["sub"],
    })

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produk tidak ditemukan atau bukan milikmu"
        )

    return {"message": "Produk berhasil dihapus ✅"}
