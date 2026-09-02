"""
Application configuration
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    DATABASE_URL: str
    REDIS_URL: str
    
    # Telegram
    BOT_TOKEN: str
    ADMIN_ID: int
    CHANNEL_ID: int
    LOGS_CHANNEL_ID: int
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 43200  # 30 days
    
    # Payment APIs
    CRYPTOBOT_API_KEY: Optional[str] = None
    XROCKET_API_KEY: Optional[str] = None
    
    # Game Settings
    HOUSE_EDGE: float = 0.04  # 4%
    RTP: float = 0.96  # 96%
    MIN_BET: float = 0.30
    CASINO_COMMISSION: float = 0.05  # 5%
    
    # Referral Settings
    REF_BONUS_REGULAR: float = 0.15
    REF_BONUS_PREMIUM: float = 0.20
    REF_DEPOSIT_PERCENT: float = 0.35  # 35%
    REF_BONUS_10_REFS: float = 3.00
    REF_WAGER_MULTIPLIER: int = 10
    REF_MIN_TRANSFER: float = 0.90
    
    # Withdrawal Settings
    MIN_DEPOSIT: float = 0.50
    MIN_WITHDRAWAL: float = 2.00
    WITHDRAWAL_FEE: float = 0.05  # 5%
    
    # Frontend
    FRONTEND_URL: str = "http://localhost:5173"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
