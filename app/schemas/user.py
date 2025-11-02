from pydantic import BaseModel, EmailStr, Field
from typing import Optional


# === USER REQUEST SCHEMAS ===
class UserCreate(BaseModel):
    """
    Schema untuk membuat user baru.
    """
    username: str = Field(..., example="john_doe")
    email: EmailStr = Field(..., example="john@example.com")
    password: str = Field(..., example="strongpassword123")


class UserUpdate(BaseModel):
    """
    Schema untuk memperbarui data user.
    """
    username: Optional[str] = Field(None, example="john_updated")
    email: Optional[EmailStr] = Field(None, example="john_updated@example.com")
    password: Optional[str] = Field(None, example="newsecurepassword")


# === USER RESPONSE SCHEMA ===
class UserResponse(BaseModel):
    """
    Schema untuk response user (tanpa menampilkan password).
    """
    id: str
    username: str
    email: EmailStr

    class Config:
        orm_mode = True
