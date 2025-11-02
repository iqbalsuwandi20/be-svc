from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from app.core.database import users_collection
from app.core.security import get_password_hash
from app.schemas.user import UserCreate, UserUpdate, UserResponse

router = APIRouter(prefix="/api/v1/users", tags=["Users"])

# === Helper ===
def user_helper(user) -> dict:
    """Konversi dokumen MongoDB menjadi format JSON-friendly."""
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
    }


# === CREATE USER ===
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    """
    Tambah user baru ke MongoDB.
    - Cek duplikat email
    - Hash password sebelum disimpan
    """
    # Cek apakah email sudah terdaftar
    if users_collection.find_one({"email": str(user.email)}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email sudah terdaftar"
        )

    # Hash password
    password_str = str(user.password)
    hashed_password = get_password_hash(password_str)

    new_user = {
        "username": str(user.username),
        "email": str(user.email),
        "password": hashed_password,
    }

    result = users_collection.insert_one(new_user)
    created_user = users_collection.find_one({"_id": result.inserted_id})
    return user_helper(created_user)


# === GET ALL USERS ===
@router.get("/", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
def get_users():
    """
    Ambil semua user yang ada di database.
    """
    users = list(users_collection.find())
    return [user_helper(u) for u in users]


# === GET USER BY ID ===
@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user_by_id(user_id: str):
    """
    Ambil data user berdasarkan ID.
    """
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User tidak ditemukan"
        )
    return user_helper(user)


# === UPDATE USER ===
@router.put("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_user(user_id: str, update_data: UserUpdate):
    """
    Update data user berdasarkan ID.
    Jika password diubah, otomatis di-hash ulang.
    """
    update_dict = {k: v for k, v in update_data.dict().items() if v is not None}

    if "password" in update_dict:
        update_dict["password"] = get_password_hash(str(update_dict["password"]))

    result = users_collection.update_one(
        {"_id": ObjectId(user_id)}, {"$set": update_dict}
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User tidak ditemukan"
        )

    updated_user = users_collection.find_one({"_id": ObjectId(user_id)})
    return user_helper(updated_user)


# === DELETE USER ===
@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(user_id: str):
    """
    Hapus user berdasarkan ID.
    """
    result = users_collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User tidak ditemukan"
        )

    return {"message": "User berhasil dihapus ✅"}
