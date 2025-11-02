from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext

# === Konfigurasi JWT ===
SECRET_KEY = "mysecretkey123"  # ⚠️ ganti di production pakai env var!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# === Konfigurasi Hashing Password ===
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# === Fungsi Hash & Verifikasi Password ===
def get_password_hash(password: str) -> str:
    """
    Hash password menggunakan bcrypt (maks. 72 karakter).
    """
    if not isinstance(password, str):
        password = str(password)
    return pwd_context.hash(password[:72])


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifikasi password plain text terhadap hash bcrypt.
    """
    if not isinstance(plain_password, str):
        plain_password = str(plain_password)
    return pwd_context.verify(plain_password[:72], hashed_password)


# === Fungsi JWT Token ===
def create_access_token(data: dict) -> str:
    """
    Membuat JWT access token dengan waktu kadaluarsa.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> dict | None:
    """
    Verifikasi dan decode JWT token.
    Return payload jika valid, atau None jika gagal.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


# === HTTP Bearer Auth ===
oauth2_scheme = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    """
    Mengambil data user dari JWT token Bearer.
    - Memvalidasi token
    - Mengembalikan payload user
    """
    token = credentials.credentials
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalid atau kadaluarsa",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload
