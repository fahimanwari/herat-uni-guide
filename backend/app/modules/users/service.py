import uuid
import hashlib
from datetime import datetime, timedelta

from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.exceptions import NotFoundError
from .models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_TOKEN_EXPIRE = 60  # minutes
REFRESH_TOKEN_EXPIRE = 30  # days


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register(self, email: str, password: str, full_name: str, phone: str | None = None):
        # Check if email exists
        existing = (await self.db.execute(
            select(User).where(User.email == email)
        )).scalars().first()
        if existing:
            raise NotFoundError("این ایمیل قبلاً ثبت شده است")

        # Check if phone exists
        if phone:
            existing_phone = (await self.db.execute(
                select(User).where(User.phone == phone)
            )).scalars().first()
            if existing_phone:
                raise NotFoundError("این شماره تلفن قبلاً ثبت شده است")

        user = User(
            id=uuid.uuid4(),
            email=email,
            phone=phone,
            full_name=full_name,
            hashed_password=pwd_context.hash(password),
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

        return await self._create_tokens(user)

    async def login(self, email: str, password: str):
        user = (await self.db.execute(
            select(User).where(User.email == email)
        )).scalars().first()

        if not user or not pwd_context.verify(password, user.hashed_password):
            raise NotFoundError("ایمیل یا رمز عبور اشتباه است")

        if not user.is_active:
            raise NotFoundError("حساب شما غیرفعال است")

        return await self._create_tokens(user)

    async def refresh(self, refresh_token: str):
        try:
            payload = jwt.decode(refresh_token, settings.jwt_secret, algorithms=["HS256"])
            user_id = payload.get("sub")
            token_type = payload.get("type")
            if not user_id or token_type != "refresh":
                raise NotFoundError("توکن نامعتبر")
        except JWTError:
            raise NotFoundError("توکن نامعتبر یا منقضی شده")

        user = await self.db.get(User, uuid.UUID(user_id))
        if not user or not user.is_active:
            raise NotFoundError("کاربر یافت نشد")

        return await self._create_tokens(user)

    async def get_profile(self, user_id: uuid.UUID):
        user = await self.db.get(User, user_id)
        if not user:
            raise NotFoundError("کاربر یافت نشد")
        return user

    async def _create_tokens(self, user: User):
        now = datetime.utcnow()

        # jti تصادفی — دو لاگین در یک ثانیه نباید توکن یکسان بسازند
        access_payload = {
            "sub": str(user.id),
            "exp": now + timedelta(minutes=ACCESS_TOKEN_EXPIRE),
            "type": "access",
            "jti": str(uuid.uuid4()),
        }
        access_token = jwt.encode(access_payload, settings.jwt_secret, algorithm="HS256")

        refresh_payload = {
            "sub": str(user.id),
            "exp": now + timedelta(days=REFRESH_TOKEN_EXPIRE),
            "type": "refresh",
            "jti": str(uuid.uuid4()),
        }
        refresh_token = jwt.encode(refresh_payload, settings.jwt_secret, algorithm="HS256")

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": {
                "id": str(user.id),
                "email": user.email,
                "full_name": user.full_name,
                "phone": user.phone,
            },
        }
