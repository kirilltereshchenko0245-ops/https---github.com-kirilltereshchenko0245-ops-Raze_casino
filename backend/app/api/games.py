"""
Games API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import secrets
import json

from ..db import get_db
from ..db.models import User, Game, GameType, GameStatus, Transaction, TransactionType, TransactionStatus
from ..games import CrashGame, MinesGame, TowerGame, RouletteGame
from ..core.config import settings

router = APIRouter(prefix="/games", tags=["games"])


# ============= CRASH GAME =============

class CrashBetRequest(BaseModel):
    bet_amount: float
    client_seed: Optional[str] = None


class CrashCashoutRequest(BaseModel):
    game_id: int
    cashout_multiplier: float


@router.post("/crash/bet")
async def crash_bet(
    request: CrashBetRequest,
    telegram_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Place bet on crash game"""
    # Get user
    result = await db.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.is_banned:
        raise HTTPException(status_code=403, detail="User is banned")
    
    # Validate bet
    if request.bet_amount < settings.MIN_BET:
        raise HTTPException(status_code=400, detail=f"Minimum bet is ${settings.MIN_BET}")
    
    if request.bet_amount > user.balance:
        raise HTTPException(status_code=400, detail="Insufficient balance")
    
    # Deduct bet from balance
    user.balance -= request.bet_amount
    
    # Generate seeds
    server_seed = secrets.token_hex(32)
    client_seed = request.client_seed or secrets.token_hex(16)
    nonce = await get_user_nonce(db, user.id)
    
    # Create crash game
    crash_game = CrashGame(server_seed, client_seed, nonce)
    
    # Create game record
    game = Game(
        user_id=user.id,
        game_type=GameType.CRASH,
        status=GameStatus.ACTIVE,
        bet_amount=request.bet_amount,
        server_seed=server_seed,
        client_seed=client_seed,
        nonce=nonce,
        hash=crash_game.hash,
        game_data=json.dumps({"crash_point": crash_game.crash_point}),
        created_at=datetime.utcnow()
    )
    
    db.add(game)
    await db.commit()
    await db.refresh(game)
    
    return {
        "game_id": game.id,
        "crash_point": crash_game.crash_point,
        "hash": crash_game.hash,
        "client_seed": client_seed,
        "nonce": nonce
    }


@router.post("/crash/cashout")
async def crash_cashout(
    request: CrashCashoutRequest,
    telegram_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Cashout from crash game"""
    # Get game
    result = await db.execute(
        select(Game).where(Game.id == request.game_id)
    )
    game = result.scalar_one_or_none()
    
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    if game.status != GameStatus.ACTIVE:
        raise HTTPException(status_code=400, detail="Game already finished")
    
    # Get user
    result = await db.execute(select(User).where(User.id == game.user_id))
    user = result.scalar_one_or_none()
    
    # Parse game data
    game_data = json.loads(game.game_data)
    crash_point = game_data["crash_point"]
    
    # Check if cashout is valid
    if request.cashout_multiplier >= crash_point:
        # Crashed - player lost
        game.status = GameStatus.LOST
        game.profit = -game.bet_amount
        game.finished_at = datetime.utcnow()
        
        await db.commit()
        
        return {
            "success": False,
            "crash_point": crash_point,
            "cashout_multiplier": request.cashout_multiplier,
            "profit": -game.bet_amount,
            "message": "Crashed!"
        }
    
    # Calculate win
    gross_payout = game.bet_amount * request.cashout_multiplier
    commission = gross_payout * settings.CASINO_COMMISSION
    net_payout = gross_payout - commission
    profit = net_payout - game.bet_amount
    
    # Update game
    game.status = GameStatus.CASHED_OUT
    game.potential_win = gross_payout
    game.profit = profit
    game.commission = commission
    game.finished_at = datetime.utcnow()
    
    # Update user balance
    user.balance += net_payout
    
    # Add transaction
    transaction = Transaction(
        user_id=user.id,
        type=TransactionType.GAME_WIN,
        status=TransactionStatus.COMPLETED,
        amount=profit,
        balance_before=user.balance - net_payout,
        balance_after=user.balance,
        description=f"Crash win x{request.cashout_multiplier}",
        created_at=datetime.utcnow()
    )
    db.add(transaction)
    
    await db.commit()
    
    return {
        "success": True,
        "crash_point": crash_point,
        "cashout_multiplier": request.cashout_multiplier,
        "profit": profit,
        "commission": commission,
        "new_balance": user.balance,
        "message": f"Won ${profit:.2f}!"
    }


# Helper function
async def get_user_nonce(db: AsyncSession, user_id: int) -> int:
    """Get next nonce for user"""
    result = await db.execute(
        select(Game).where(Game.user_id == user_id).order_by(Game.id.desc()).limit(1)
    )
    last_game = result.scalar_one_or_none()
    
    if last_game:
        return last_game.nonce + 1
    return 0


# ============= MINES GAME =============

class MinesStartRequest(BaseModel):
    bet_amount: float
    num_mines: int
    client_seed: Optional[str] = None


class MinesRevealRequest(BaseModel):
    game_id: int
    cell_index: int


class MinesCashoutRequest(BaseModel):
    game_id: int


@router.post("/mines/start")
async def mines_start(
    request: MinesStartRequest,
    telegram_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Start mines game"""
    result = await db.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.scalar_one_or_none()
    
    if not user or user.is_banned:
        raise HTTPException(status_code=403)
    
    if request.bet_amount < settings.MIN_BET or request.bet_amount > user.balance:
        raise HTTPException(status_code=400, detail="Invalid bet amount")
    
    if request.num_mines < 2 or request.num_mines > 24:
        raise HTTPException(status_code=400, detail="Mines must be between 2 and 24")
    
    # Deduct bet
    user.balance -= request.bet_amount
    
    # Generate seeds
    server_seed = secrets.token_hex(32)
    client_seed = request.client_seed or secrets.token_hex(16)
    nonce = await get_user_nonce(db, user.id)
    
    # Create game
    mines_game = MinesGame(request.bet_amount, request.num_mines, server_seed, client_seed, nonce)
    
    game = Game(
        user_id=user.id,
        game_type=GameType.MINES,
        status=GameStatus.ACTIVE,
        bet_amount=request.bet_amount,
        server_seed=server_seed,
        client_seed=client_seed,
        nonce=nonce,
        hash=secrets.token_hex(16),
        game_data=json.dumps({
            "num_mines": request.num_mines,
            "field": mines_game.field,
            "revealed": []
        })
    )
    
    db.add(game)
    await db.commit()
    await db.refresh(game)
    
    return {
        "game_id": game.id,
        "num_mines": request.num_mines,
        "field_size": 25
    }


@router.post("/mines/reveal")
async def mines_reveal(
    request: MinesRevealRequest,
    telegram_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Reveal cell in mines game"""
    result = await db.execute(select(Game).where(Game.id == request.game_id))
    game = result.scalar_one_or_none()
    
    if not game or game.status != GameStatus.ACTIVE:
        raise HTTPException(status_code=400)
    
    game_data = json.loads(game.game_data)
    field = game_data["field"]
    revealed = game_data.get("revealed", [])
    
    if request.cell_index in revealed:
        raise HTTPException(status_code=400, detail="Cell already revealed")
    
    is_mine = field[request.cell_index] == 1
    revealed.append(request.cell_index)
    
    if is_mine:
        # Hit mine - game lost
        game.status = GameStatus.LOST
        game.profit = -game.bet_amount
        game.finished_at = datetime.utcnow()
        game_data["revealed"] = revealed
        game.game_data = json.dumps(game_data)
        
        await db.commit()
        
        return {
            "is_mine": True,
            "game_finished": True,
            "field": field
        }
    else:
        # Safe cell
        from ..games.mines import calculate_mines_multiplier
        multiplier = calculate_mines_multiplier(game_data["num_mines"], len(revealed))
        
        game_data["revealed"] = revealed
        game.game_data = json.dumps(game_data)
        await db.commit()
        
        return {
            "is_mine": False,
            "multiplier": multiplier,
            "revealed_count": len(revealed)
        }


@router.post("/mines/cashout")
async def mines_cashout(
    request: MinesCashoutRequest,
    telegram_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Cashout mines game"""
    result = await db.execute(select(Game).where(Game.id == request.game_id))
    game = result.scalar_one_or_none()
    
    if not game or game.status != GameStatus.ACTIVE:
        raise HTTPException(status_code=400)
    
    game_data = json.loads(game.game_data)
    revealed = game_data.get("revealed", [])
    
    from ..games.mines import calculate_mines_multiplier, calculate_mines_payout
    
    multiplier = calculate_mines_multiplier(game_data["num_mines"], len(revealed))
    gross_payout, net_payout = calculate_mines_payout(game.bet_amount, multiplier)
    profit = net_payout - game.bet_amount
    commission = gross_payout - net_payout
    
    # Update game
    game.status = GameStatus.CASHED_OUT
    game.profit = profit
    game.commission = commission
    game.finished_at = datetime.utcnow()
    
    # Update user balance
    result = await db.execute(select(User).where(User.id == game.user_id))
    user = result.scalar_one_or_none()
    user.balance += net_payout
    
    await db.commit()
    
    return {
        "profit": profit,
        "multiplier": multiplier,
        "new_balance": user.balance
    }


# Continue with Tower and Roulette endpoints...
# (Similar structure for tower and roulette)

@router.get("/history")
async def game_history(
    telegram_id: int,
    limit: int = 20,
    offset: int = 0,
    db: AsyncSession = Depends(get_db)
):
    """Get user's game history"""
    result = await db.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404)
    
    result = await db.execute(
        select(Game)
        .where(Game.user_id == user.id)
        .order_by(Game.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    games = result.scalars().all()
    
    history = []
    for game in games:
        history.append({
            "id": game.id,
            "game_type": game.game_type.value,
            "bet_amount": game.bet_amount,
            "profit": game.profit,
            "status": game.status.value,
            "created_at": game.created_at.isoformat()
        })
    
    return {"games": history, "total": len(games)}
