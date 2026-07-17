from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from app.core.rate_limit import rate_limiter
from .service import UserService
from .schemas import RegisterRequest, LoginRequest, TokenResponse, RefreshRequest

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=TokenResponse)
async def register(payload: RegisterRequest, request: Request, db: AsyncSession = Depends(get_db)):
    # Rate limit: 3 registrations per minute per IP
    client_ip = request.client.host
    await rate_limiter.check_rate_limit(f"register:{client_ip}", limit=3, window=60)
    return await UserService(db).register(
        payload.email, payload.password, payload.full_name, payload.phone
    )


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, request: Request, db: AsyncSession = Depends(get_db)):
    # Rate limit: 5 login attempts per minute per IP
    client_ip = request.client.host
    await rate_limiter.check_rate_limit(f"login:{client_ip}", limit=5, window=60)
    return await UserService(db).login(payload.email, payload.password)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(payload: RefreshRequest, db: AsyncSession = Depends(get_db)):
    return await UserService(db).refresh(payload.refresh_token)
