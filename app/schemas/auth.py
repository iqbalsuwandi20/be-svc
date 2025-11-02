from pydantic import BaseModel, EmailStr

# === AUTH REQUEST SCHEMAS ===
class LoginRequest(BaseModel):
    """
    Schema untuk request login user.
    """
    email: EmailStr
    password: str


# === AUTH RESPONSE SCHEMAS ===
class TokenResponse(BaseModel):
    """
    Schema untuk response setelah login sukses.
    """
    access_token: str
    token_type: str = "bearer"
