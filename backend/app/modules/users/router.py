import uuid
from fastapi import APIRouter, Depends, Request, Query
from pydantic import BaseModel
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from app.core.security import get_current_admin
from app.core.rate_limit import rate_limiter
from app.modules.admin_auth.models import AdminUser
from .service import UserService
from .schemas import RegisterRequest, LoginRequest, TokenResponse, RefreshRequest, UserListItem, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


# --- Public ---

@router.post("/register", response_model=TokenResponse)
async def register(payload: RegisterRequest, request: Request, db: AsyncSession = Depends(get_db)):
    client_ip = request.client.host
    await rate_limiter.check_rate_limit(f"register:{client_ip}", limit=3, window=60)
    return await UserService(db).register(
        payload.email, payload.password, payload.full_name, payload.phone
    )


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, request: Request, db: AsyncSession = Depends(get_db)):
    client_ip = request.client.host
    await rate_limiter.check_rate_limit(f"login:{client_ip}", limit=5, window=60)
    return await UserService(db).login(payload.email, payload.password)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(payload: RefreshRequest, db: AsyncSession = Depends(get_db)):
    return await UserService(db).refresh(payload.refresh_token)


# --- Admin ---

@router.get("/admin/list", response_model=list[UserListItem])
async def list_users(
    db: AsyncSession = Depends(get_db),
    admin: AdminUser = Depends(get_current_admin),
):
    from .models import User
    q = select(User).order_by(User.created_at.desc())
    return list((await db.execute(q)).scalars())


@router.patch("/admin/{user_id}")
async def update_user(
    user_id: uuid.UUID,
    payload: UserUpdate,
    db: AsyncSession = Depends(get_db),
    admin: AdminUser = Depends(get_current_admin),
):
    from .models import User
    from app.core.exceptions import NotFoundError
    user = await db.get(User, user_id)
    if user is None:
        raise NotFoundError("کاربر یافت نشد")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(user, key, value)
    await db.commit()
    await db.refresh(user)
    return {"id": str(user.id), "email": user.email, "is_active": user.is_active}


class LinkSessionRequest(BaseModel):
    session_id: str


@router.post("/link-session")
async def link_session(
    payload: LinkSessionRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """Link anonymous session to logged-in user."""
    # Get current user from token
    from app.core.security import security
    from jose import jwt, JWTError
    from app.config import settings

    try:
        auth_header = request.headers.get("Authorization", "")
        token = auth_header.replace("Bearer ", "")
        payload_jwt = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
        user_id = payload_jwt.get("sub")
        if not user_id:
            return {"error": "توکن نامعتبر"}
    except (JWTError, Exception):
        return {"error": "توکن نامعتبر"}

    # Update mock_exam_sessions
    from app.modules.mock_kankor.models import MockExamSession
    q = (
        update(MockExamSession)
        .where(MockExamSession.session_id == payload.session_id)
        .values(user_id=uuid.UUID(user_id))
    )
    result = await db.execute(q)
    await db.commit()

    return {"linked": result.rowcount}
