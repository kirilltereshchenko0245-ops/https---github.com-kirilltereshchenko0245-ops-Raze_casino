"""
Database models
"""
from datetime import datetime
from sqlalchemy import Column, Integer, BigInteger, String, Float, Boolean, DateTime, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()


class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, index=True, nullable=False)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    is_premium = Column(Boolean, default=False)
    
    # Balances
    balance = Column(Float, default=0.0)
    referral_balance = Column(Float, default=0.0)
    wager_amount = Column(Float, default=0.0)  # Amount needed to wager
    
    # Referral
    referral_code = Column(String, unique=True, nullable=False)
    referred_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Status
    is_banned = Column(Boolean, default=False)
    task_completed = Column(Boolean, default=False)  # Channel subscription
    
    # Settings
    theme = Column(String, default="dark")  # dark/light
    chat_enabled = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow)
    last_bonus_claimed = Column(DateTime, nullable=True)
    
    # Relationships
    referred_by = relationship("User", remote_side=[id], backref="referrals")
    games = relationship("Game", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")
    chat_messages = relationship("ChatMessage", back_populates="user")


class GameType(str, enum.Enum):
    """Game types"""
    CRASH = "crash"
    MINES = "mines"
    TOWER = "tower"
    ROULETTE = "roulette"


class GameStatus(str, enum.Enum):
    """Game status"""
    ACTIVE = "active"
    WON = "won"
    LOST = "lost"
    CASHED_OUT = "cashed_out"


class Game(Base):
    """Game model"""
    __tablename__ = "games"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    game_type = Column(SQLEnum(GameType), nullable=False)
    status = Column(SQLEnum(GameStatus), default=GameStatus.ACTIVE)
    
    bet_amount = Column(Float, nullable=False)
    potential_win = Column(Float, default=0.0)
    profit = Column(Float, default=0.0)
    commission = Column(Float, default=0.0)
    
    # Game specific data (JSON stored as text)
    game_data = Column(Text, nullable=True)  # JSON string
    
    # Provably fair
    server_seed = Column(String, nullable=False)
    client_seed = Column(String, nullable=False)
    nonce = Column(Integer, default=0)
    hash = Column(String, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    finished_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="games")


class TransactionType(str, enum.Enum):
    """Transaction types"""
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    GAME_WIN = "game_win"
    GAME_LOSS = "game_loss"
    REFERRAL_BONUS = "referral_bonus"
    REFERRAL_COMMISSION = "referral_commission"
    DAILY_BONUS = "daily_bonus"
    PROMOCODE = "promocode"
    REF_TRANSFER = "ref_transfer"
    ADMIN_ADJUST = "admin_adjust"


class TransactionStatus(str, enum.Enum):
    """Transaction status"""
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Transaction(Base):
    """Transaction model"""
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    type = Column(SQLEnum(TransactionType), nullable=False)
    status = Column(SQLEnum(TransactionStatus), default=TransactionStatus.PENDING)
    
    amount = Column(Float, nullable=False)
    balance_before = Column(Float, nullable=False)
    balance_after = Column(Float, nullable=False)
    
    description = Column(Text, nullable=True)
    meta_data = Column(Text, nullable=True)  # JSON string (renamed from metadata)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="transactions")


class Withdrawal(Base):
    """Withdrawal request model"""
    __tablename__ = "withdrawals"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    amount = Column(Float, nullable=False)
    fee = Column(Float, nullable=False)
    final_amount = Column(Float, nullable=False)
    
    method = Column(String, nullable=False)  # cryptobot/xrocket
    wallet_address = Column(String, nullable=True)
    
    status = Column(SQLEnum(TransactionStatus), default=TransactionStatus.PENDING)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime, nullable=True)
    processed_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    reject_reason = Column(Text, nullable=True)


class Promocode(Base):
    """Promocode model"""
    __tablename__ = "promocodes"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, nullable=False)
    amount = Column(Float, nullable=False)
    
    max_uses = Column(Integer, default=0)  # 0 = unlimited
    current_uses = Column(Integer, default=0)
    
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)


class PromocodeUse(Base):
    """Promocode usage tracking"""
    __tablename__ = "promocode_uses"
    
    id = Column(Integer, primary_key=True, index=True)
    promocode_id = Column(Integer, ForeignKey("promocodes.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    amount = Column(Float, nullable=False)
    used_at = Column(DateTime, default=datetime.utcnow)


class ChatMessage(Base):
    """Chat message model"""
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    message = Column(Text, nullable=False)
    is_deleted = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="chat_messages")


class AdminLog(Base):
    """Admin action logs"""
    __tablename__ = "admin_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    admin_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    action = Column(String, nullable=False)
    target_user_id = Column(Integer, nullable=True)
    details = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
