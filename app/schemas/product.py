from pydantic import BaseModel, Field
from typing import Optional


# === PRODUCT REQUEST SCHEMAS ===
class ProductCreate(BaseModel):
    """
    Schema untuk membuat produk baru.
    """
    name: str = Field(..., example="Meja Makan Kayu Jati")
    category: str = Field(..., example="Meja")
    description: Optional[str] = Field(None, example="Meja makan kayu jati ukuran 2 meter")
    price: float = Field(..., gt=0, example=3400000)
    stock: int = Field(..., ge=0, example=12)
    unit: str = Field(..., example="Unit")
    is_active: bool = Field(default=True, example=True)
    low_stock_limit: Optional[int] = Field(None, example=5, description="Batas stok minimum sebelum dianggap menipis")
    image_url: Optional[str] = Field(None, example="/uploads/meja_jati.png")


class ProductUpdate(BaseModel):
    """
    Schema untuk memperbarui data produk.
    """
    name: Optional[str] = Field(None, example="Meja Makan Kayu Mahoni")
    category: Optional[str] = Field(None, example="Meja")
    description: Optional[str] = Field(None, example="Updated product description")
    price: Optional[float] = Field(None, gt=0, example=3500000)
    stock: Optional[int] = Field(None, ge=0, example=15)
    unit: Optional[str] = Field(None, example="Unit")
    is_active: Optional[bool] = Field(None, example=True)
    low_stock_limit: Optional[int] = Field(None, example=5)
    image_url: Optional[str] = Field(None, example="/uploads/meja_mahoni.png")


# === PRODUCT RESPONSE SCHEMA ===
class ProductResponse(BaseModel):
    """
    Schema untuk response data produk (setelah CRUD).
    """
    id: str
    name: str
    category: str
    description: Optional[str] = None
    price: float
    stock: int
    unit: str
    is_active: bool
    low_stock_limit: Optional[int] = None
    image_url: Optional[str] = None
    owner_id: str

    class Config:
        from_attributes = True  # ✅ Fix untuk Pydantic v2
