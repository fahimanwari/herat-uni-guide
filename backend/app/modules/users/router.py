from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from .service import UserService
from .schemas import RegisterRequest, LoginRequest, TokenResponse, RefreshRequest

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=TokenResponse)
async def register(payload: RegisterRequest, db: AsyncSession = Depends(get_db)):
    return await UserService(db).register(
        payload.email, payload.password, payload.full_name, payload.phone
    )


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
    return await UserService(db).login(payload.email, payload.password)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(payload: RefreshRequest, db: AsyncSession = Depends(get_db)):
    return await UserService(db).refresh(payload.refresh_token)
