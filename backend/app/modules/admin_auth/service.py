import uuid
import hashlib
from datetime import datetime, timedelta

from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.exceptions import NotFoundError
from .models import AdminUser, RefreshToken
from .schemas import TokenResponse

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_TOKEN_EXPIRE = 15  # minutes
REFRESH_TOKEN_EXPIRE = 7  # days


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


class AdminAuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def login(self, email: str, password: str) -> TokenResponse:
        q = select(AdminUser).where(AdminUser.email == email)
        admin = (await self.db.execute(q)).scalar_one_or_none()
        if not admin or not pwd_context.verify(password, admin.hashed_password):
            raise NotFoundError("ایمیل یا رمز عبور اشتباه است")
        if not admin.is_active:
            raise NotFoundError("حساب شما غیرفعال است")

        return await self._create_tokens(admin.id)

    async def refresh(self, refresh_token: str) -> TokenResponse:
        token_hash = hash_token(refresh_token)
        q = select(RefreshToken).where(
            RefreshToken.token_hash == token_hash,
            RefreshToken.revoked == False,
        )
        db_token = (await self.db.execute(q)).scalar_one_or_none()

        if not db_token or db_token.expires_at < datetime.utcnow():
            raise NotFoundError("توکن نامعتبر یا منقضی شده است")

        # Revoke old token (rotation)
        db_token.revoked = True
        await self.db.commit()

        # Create new tokens
        return await self._create_tokens(db_token.admin_id)

    async def _create_tokens(self, admin_id: uuid.UUID) -> TokenResponse:
        now = datetime.utcnow()

        # Access token
        access_payload = {
            "sub": str(admin_id),
            "exp": now + timedelta(minutes=ACCESS_TOKEN_EXPIRE),
            "type": "access",
        }
        access_token = jwt.encode(access_payload, settings.jwt_secret, algorithm="HS256")

        # Refresh token
        refresh_payload = {
            "sub": str(admin_id),
            "exp": now + timedelta(days=REFRESH_TOKEN_EXPIRE),
            "type": "refresh",
        }
        refresh_token = jwt.encode(refresh_payload, settings.jwt_secret, algorithm="HS256")

        # Save refresh token hash
        self.db.add(RefreshToken(
            id=uuid.uuid4(),
            admin_id=admin_id,
            token_hash=hash_token(refresh_token),
            expires_at=now + timedelta(days=REFRESH_TOKEN_EXPIRE),
        ))
        await self.db.commit()

        return TokenResponse(access_token=access_token, refresh_token=refresh_token)

    async def create_admin(self, email: str, password: str, full_name: str, role: str = "editor"):
        admin = AdminUser(
            id=uuid.uuid4(),
            email=email,
            hashed_password=pwd_context.hash(password),
            full_name=full_name,
            role=role,
        )
        self.db.add(admin)
        await self.db.commit()
        return admin
