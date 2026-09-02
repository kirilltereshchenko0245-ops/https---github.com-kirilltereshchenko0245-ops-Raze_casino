"""
Tower game logic - Climb 10 levels, avoid mines
"""
import random
import hashlib
from typing import List, Dict, Tuple
from ..core.config import settings


# Tower multipliers for each level
# Based on the screenshot provided
TOWER_MULTIPLIERS = [
    1.21,  # Level 1
    1.51,  # Level 2
    1.88,  # Level 3
    2.36,  # Level 4
    2.94,  # Level 5
    3.68,  # Level 6
    4.60,  # Level 7
    5.75,  # Level 8
    7.19,  # Level 9
    8.99   # Level 10 (top)
]


def generate_tower_path(seed: str, num_levels: int = 10, doors_per_level: int = 3) -> List[int]:
    """
    Generate safe door for each level
    
    Args:
        seed: Random seed for generation
        num_levels: Number of levels (default 10)
        doors_per_level: Number of doors per level (default 3)
    
    Returns:
        List of safe door indices for each level [0-2, 0-2, ...]
    """
    random.seed(seed)
    path = []
    
    for level in range(num_levels):
        safe_door = random.randint(0, doors_per_level - 1)
        path.append(safe_door)
    
    return path


def calculate_tower_multiplier(current_level: int) -> float:
    """
    Get multiplier for current level
    
    Args:
        current_level: Current level (0-9)
    
    Returns:
        Multiplier for that level
    """
    if current_level < 0 or current_level >= len(TOWER_MULTIPLIERS):
        return 1.0
    
    return TOWER_MULTIPLIERS[current_level]


def calculate_tower_payout(bet_amount: float, multiplier: float) -> Tuple[float, float, float]:
    """
    Calculate payout for tower game
    
    Returns:
        (gross_payout, commission, net_payout)
    """
    gross_payout = bet_amount * multiplier
    commission = gross_payout * settings.CASINO_COMMISSION
    net_payout = gross_payout - commission
    
    return gross_payout, commission, net_payout


class TowerGame:
    """Tower game manager"""
    
    def __init__(self, bet_amount: float, server_seed: str, client_seed: str, nonce: int):
        self.bet_amount = bet_amount
        self.server_seed = server_seed
        self.client_seed = client_seed
        self.nonce = nonce
        
        # Generate tower path (safe doors)
        combined_seed = f"{server_seed}:{client_seed}:{nonce}"
        self.safe_path = generate_tower_path(combined_seed, num_levels=10, doors_per_level=3)
        
        # Game state
        self.current_level = 0  # 0 = ground, 10 = top
        self.is_finished = False
        self.is_won = False
        self.current_multiplier = 1.0
        self.chosen_doors: List[int] = []
    
    def choose_door(self, door_index: int) -> Dict:
        """
        Choose a door to climb
        
        Args:
            door_index: Door index (0, 1, or 2)
        
        Returns:
            {
                "success": bool,
                "is_safe": bool,
                "current_level": int,
                "multiplier": float,
                "game_finished": bool
            }
        """
        if self.is_finished:
            return {
                "success": False,
                "error": "Game already finished"
            }
        
        if door_index < 0 or door_index > 2:
            return {
                "success": False,
                "error": "Invalid door index (must be 0, 1, or 2)"
            }
        
        # Check if door is safe
        safe_door = self.safe_path[self.current_level]
        is_safe = (door_index == safe_door)
        
        self.chosen_doors.append(door_index)
        
        if is_safe:
            # Climb to next level
            self.current_level += 1
            self.current_multiplier = calculate_tower_multiplier(self.current_level - 1)
            
            # Check if reached the top
            if self.current_level >= 10:
                self.is_finished = True
                self.is_won = True
                
                return {
                    "success": True,
                    "is_safe": True,
                    "current_level": self.current_level,
                    "multiplier": self.current_multiplier,
                    "game_finished": True,
                    "result": "won",
                    "message": "Reached the top! 🎉"
                }
            
            return {
                "success": True,
                "is_safe": True,
                "current_level": self.current_level,
                "multiplier": self.current_multiplier,
                "game_finished": False,
                "can_cashout": True
            }
        else:
            # Hit mine - game lost
            self.is_finished = True
            self.is_won = False
            
            return {
                "success": True,
                "is_safe": False,
                "current_level": self.current_level,
                "multiplier": 0,
                "game_finished": True,
                "result": "lost",
                "safe_door": safe_door
            }
    
    def cashout(self) -> Dict:
        """
        Cashout at current level
        
        Returns:
            {
                "success": bool,
                "profit": float,
                "multiplier": float
            }
        """
        if self.is_finished:
            return {
                "success": False,
                "error": "Game already finished"
            }
        
        if self.current_level == 0:
            return {
                "success": False,
                "error": "Cannot cashout at ground level"
            }
        
        self.is_finished = True
        self.is_won = True
        
        # Calculate payout
        gross_payout, commission, net_payout = calculate_tower_payout(
            self.bet_amount,
            self.current_multiplier
        )
        
        profit = net_payout - self.bet_amount
        
        return {
            "success": True,
            "profit": profit,
            "multiplier": self.current_multiplier,
            "level": self.current_level,
            "commission": commission,
            "gross_payout": gross_payout,
            "net_payout": net_payout
        }
    
    def get_level_state(self, level: int) -> Dict:
        """
        Get state for specific level (for visualization)
        
        Returns:
            {
                "level": int,
                "doors": [{"index": int, "revealed": bool, "is_safe": bool}],
                "multiplier": float
            }
        """
        if level < 0 or level >= 10:
            return {"error": "Invalid level"}
        
        doors = []
        for i in range(3):
            door_info = {
                "index": i,
                "revealed": False,
                "is_safe": None
            }
            
            # If this level was reached and finished, reveal
            if level < self.current_level or (level == self.current_level and self.is_finished):
                door_info["revealed"] = True
                door_info["is_safe"] = (i == self.safe_path[level])
            
            doors.append(door_info)
        
        return {
            "level": level,
            "doors": doors,
            "multiplier": calculate_tower_multiplier(level),
            "is_current": (level == self.current_level and not self.is_finished)
        }
    
    def get_full_path(self) -> List[int]:
        """
        Reveal full safe path (after game ends)
        Only call after game is finished
        """
        if not self.is_finished:
            return None
        
        return self.safe_path.copy()
    
    def get_game_summary(self) -> Dict:
        """Get complete game summary"""
        return {
            "bet_amount": self.bet_amount,
            "current_level": self.current_level,
            "current_multiplier": self.current_multiplier,
            "is_finished": self.is_finished,
            "is_won": self.is_won,
            "chosen_doors": self.chosen_doors,
            "can_verify": True,
            "server_seed": self.server_seed if self.is_finished else None,
            "client_seed": self.client_seed,
            "nonce": self.nonce
        }


def verify_tower_result(server_seed: str, client_seed: str, nonce: int, claimed_path: List[int]) -> bool:
    """
    Verify that tower result is fair
    """
    combined_seed = f"{server_seed}:{client_seed}:{nonce}"
    actual_path = generate_tower_path(combined_seed)
    
    return actual_path == claimed_path


# Test
if __name__ == "__main__":
    print("Testing Tower Game...")
    
    # Test multipliers
    print("\nTower multipliers by level:")
    for level in range(10):
        mult = calculate_tower_multiplier(level)
        print(f"  Level {level + 1}: x{mult}")
    
    # Test game
    print("\nTest game:")
    game = TowerGame(1.0, "server_seed", "client_seed", 1)
    print(f"Safe path: {game.safe_path}")
    
    print("\nSimulating climbing:")
    for level in range(5):
        safe_door = game.safe_path[level]
        result = game.choose_door(safe_door)
        print(f"  Level {level + 1}: Chose door {safe_door} -> {result}")
    
    # Cashout
    cashout_result = game.cashout()
    print(f"\nCashout: {cashout_result}")
