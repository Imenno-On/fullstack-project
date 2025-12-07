from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_session
from app.models.test import Test
from app.schemas.test_schema import TestCreate, TestUpdate, TestResponse
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/tests", tags=["Tests"])

# ---------- CREATE ----------
@router.post("/", response_model=TestResponse, status_code=status.HTTP_201_CREATED)
async def create_test(
    test_data: TestCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    new_test = Test(**test_data.dict(), owner_id=current_user.id)
    session.add(new_test)
    await session.commit()
    await session.refresh(new_test)
    return new_test

# ---------- READ (list) ----------
@router.get("/", response_model=List[TestResponse])
async def list_tests(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    res = await session.execute(select(Test).where(Test.owner_id == current_user.id))
    return res.scalars().all()

# ---------- READ (single) ----------
@router.get("/{test_id}", response_model=TestResponse)
async def get_test(
    test_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    res = await session.execute(
        select(Test).where(Test.id == test_id, Test.owner_id == current_user.id)
    )
    test = res.scalar_one_or_none()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    return test

# ---------- UPDATE ----------
@router.put("/{test_id}", response_model=TestResponse)
async def update_test(
    test_id: int,
    payload: TestUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    res = await session.execute(
        select(Test).where(Test.id == test_id, Test.owner_id == current_user.id)
    )
    test = res.scalar_one_or_none()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(test, field, value)
    await session.commit()
    await session.refresh(test)
    return test

# ---------- DELETE ----------
@router.delete("/{test_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_test(
    test_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    res = await session.execute(
        select(Test).where(Test.id == test_id, Test.owner_id == current_user.id)
    )
    test = res.scalar_one_or_none()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    await session.delete(test)
    await session.commit()
