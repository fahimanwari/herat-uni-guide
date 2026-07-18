import uuid

from pydantic import BaseModel, ConfigDict, EmailStr


class RegisterRequest(BaseModel):
    email: str
    password: str
    full_name: str
    phone: str | None = None


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: dict


class RefreshRequest(BaseModel):
    refresh_token: str


class UserProfile(BaseModel):
    id: str
    email: str
    full_name: str
    phone: str | None
    is_verified: bool


# --- Admin ---

class UserListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: str
    full_name: str
    phone: str | None
    is_active: bool
    is_verified: bool


class UserUpdate(BaseModel):
    is_active: bool | None = None
    is_verified: bool | None = None
