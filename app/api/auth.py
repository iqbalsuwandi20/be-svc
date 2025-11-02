from fastapi import APIRouter, HTTPException, status, Depends
from app.core.security import verify_password, create_access_token, get_current_user
from app.core.database import users_collection
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.user import UserResponse

router = APIRouter(tags=["Auth"])

# === LOGIN ===
@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def login_user(login_data: LoginRequest):
    """
    Login user berdasarkan email & password, 
    lalu kembalikan JWT token jika valid.
    """
    user = users_collection.find_one({"email": login_data.email})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email tidak terdaftar"
        )

    # Verifikasi password
    if not verify_password(login_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Password salah"
        )

    # Generate JWT token
    access_token = create_access_token({
        "sub": str(user["_id"]),
        "email": user["email"]
    })

    return TokenResponse(access_token=access_token, token_type="bearer")


# === GET CURRENT USER ===
@router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_me(current_user=Depends(get_current_user)):
    """
    Ambil data user yang sedang login berdasarkan JWT token aktif.
    """
    email = current_user.get("email")
    user = users_collection.find_one({"email": email})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User tidak ditemukan"
        )

    return UserResponse(
        id=str(user["_id"]),
        username=user["username"],
        email=user["email"]
    )
