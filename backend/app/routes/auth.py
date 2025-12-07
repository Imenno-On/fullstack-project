from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_session
from app.schemas.user_schema import UserCreate, Token
from app.models.user import User
from app.core.security import verify_password, get_password_hash, create_access_token

router = APIRouter()


@router.post("/auth/register", response_model=Token)
async def register(user: UserCreate, session: AsyncSession = Depends(get_session)):
    print("[DEBUG] email:", user.email)
    print("[DEBUG] password length:", len(user.password.encode()), "bytes")
    res = await session.execute(select(User).where(User.email == user.email))
    if res.scalar():
        raise HTTPException(400, "Email already registered")
    db_user = User(email=user.email, hashed_password=get_password_hash(user.password))
    session.add(db_user)
    await session.commit()
    token = create_access_token(data={"sub": user.email})
    return Token(access_token=token, token_type="bearer")

@router.post("/auth/login", response_model=Token)
async def login(form_data: UserCreate, session: AsyncSession = Depends(get_session)):
    res = await session.execute(select(User).where(User.email == form_data.email))
    user = res.scalar()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(400, "Incorrect email or password")
    token = create_access_token(data={"sub": user.email})
    return Token(access_token=token, token_type="bearer")