import uuid

from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.deps import get_db
from app.modules.admin_auth.models import AdminUser

security = HTTPBearer()


async def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> AdminUser:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
        admin_id = payload.get("sub")
        token_type = payload.get("type")
        if not admin_id or token_type != "access":
            raise HTTPException(status_code=401, detail="توکن نامعتبر")
    except JWTError:
        raise HTTPException(status_code=401, detail="توکن نامعتبر")

    admin = await db.get(AdminUser, uuid.UUID(admin_id))
    if not admin or not admin.is_active:
        raise HTTPException(status_code=401, detail="ادمین یافت نشد")
    return admin
