"""
Authentication API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from datetime import datetime
import secrets

from ..db import get_db
from ..db.models import User
from ..core.security import verify_telegram_init_data, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


class InitRequest(BaseModel):
    init_data: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict


@router.post("/init", response_model=AuthResponse)
async def init_auth(request: InitRequest, db: AsyncSession = Depends(get_db)):
    """
    Initialize user authentication via Telegram Mini App init data
    """
    # Verify Telegram init data
    user_data = verify_telegram_init_data(request.init_data)
    
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid init data")
    
    telegram_id = user_data.get("id")
    username = user_data.get("username")
    first_name = user_data.get("first_name")
    last_name = user_data.get("last_name")
    is_premium = user_data.get("is_premium", False)
    
    # Check if user exists
    result = await db.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        # Create new user
        referral_code = f"REF{telegram_id}_{secrets.token_hex(3).upper()}"
        
        user = User(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            is_premium=is_premium,
            referral_code=referral_code,
            created_at=datetime.utcnow()
        )
        
        db.add(user)
        await db.commit()
        await db.refresh(user)
    else:
        # Update user info
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.is_premium = is_premium
        user.last_active = datetime.utcnow()
        
        await db.commit()
        await db.refresh(user)
    
    # Create access token
    access_token = create_access_token(
        data={"sub": str(user.telegram_id), "user_id": user.id}
    )
    
    # Return user data
    user_dict = {
        "id": user.id,
        "telegram_id": user.telegram_id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_premium": user.is_premium,
        "balance": user.balance,
        "referral_balance": user.referral_balance,
        "wager_amount": user.wager_amount,
        "referral_code": user.referral_code,
        "is_banned": user.is_banned,
        "task_completed": user.task_completed,
        "theme": user.theme,
        "chat_enabled": user.chat_enabled
    }
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_dict
    }


@router.get("/me")
async def get_current_user(
    telegram_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get current user data"""
    result = await db.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": user.id,
        "telegram_id": user.telegram_id,
        "username": user.username,
        "first_name": user.first_name,
        "balance": user.balance,
        "referral_balance": user.referral_balance,
        "wager_amount": user.wager_amount,
        "referral_code": user.referral_code,
        "theme": user.theme,
        "chat_enabled": user.chat_enabled
    }
