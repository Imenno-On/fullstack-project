from fastapi import Depends, HTTPException
from app.core.security import bearer_scheme, decode_token
from app.models.user import User
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from sqlalchemy import select

async def get_current_user(
    auth: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    session: AsyncSession = Depends(get_session),
) -> User:
    payload = decode_token(auth.credentials)
    email: str = payload.get("sub")
    res = await session.execute(select(User).where(User.email == email))
    user = res.scalar_one_or_none()
    if not user:
        raise HTTPException(401, "User not found")
    return user