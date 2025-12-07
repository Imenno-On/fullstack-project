from fastapi import APIRouter, Depends
from ..core.dependencies import get_current_user
from app.schemas.user_schema import UserResponse

router = APIRouter()

@router.get("/users/me", response_model=UserResponse)
def read_me(current_user=Depends(get_current_user)):
    return UserResponse(email=current_user.email)
