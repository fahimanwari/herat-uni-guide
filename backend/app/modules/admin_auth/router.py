from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from app.core.rate_limit import rate_limiter
from .service import AdminAuthService
from .schemas import LoginRequest, TokenResponse, RefreshRequest

router = APIRouter(prefix="/admin/auth", tags=["admin-auth"])


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, request: Request, db: AsyncSession = Depends(get_db)):
    # Rate limit: 5 login attempts per minute per IP
    client_ip = request.client.host
    await rate_limiter.check_rate_limit(f"login:{client_ip}", limit=5, window=60)
    return await AdminAuthService(db).login(payload.email, payload.password)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(payload: RefreshRequest, db: AsyncSession = Depends(get_db)):
    return await AdminAuthService(db).refresh(payload.refresh_token)
