"""
Mines game logic - 5x5 field with mines
"""
import random
import hashlib
from typing import List, Tuple, Dict
from ..core.config import settings


# Multiplier table for mines game
# [num_mines][num_revealed_cells] = multiplier
MINES_MULTIPLIERS = {
    2: [1.08, 1.17, 1.29, 1.41, 1.56, 1.74, 1.94, 2.18, 2.47, 2.83, 3.26, 3.81, 4.5, 5.4, 6.6, 8.25, 10.61, 14.14, 19.8, 29.7, 49.5, 99, 297],
    3: [1.12, 1.25, 1.4, 1.58, 1.79, 2.04, 2.35, 2.73, 3.2, 3.79, 4.55, 5.52, 6.82, 8.59, 11.07, 14.71, 20.23, 29.05, 44.2, 72.73, 132, 297],
    4: [1.17, 1.33, 1.52, 1.76, 2.06, 2.43, 2.91, 3.52, 4.32, 5.39, 6.86, 8.95, 11.98, 16.45, 23.28, 34.37, 53.36, 88.93, 163.2, 339.2, 848],
    5: [1.22, 1.42, 1.67, 1.98, 2.38, 2.89, 3.56, 4.45, 5.68, 7.41, 9.9, 13.64, 19.48, 29.22, 46.75, 79.48, 146.4, 297.4, 647.2, 1648],
    6: [1.27, 1.52, 1.84, 2.25, 2.79, 3.51, 4.49, 5.85, 7.8, 10.63, 14.96, 21.81, 33.03, 52.85, 90.44, 167.1, 332.2, 730.9, 1828],
    7: [1.33, 1.63, 2.04, 2.59, 3.33, 4.35, 5.77, 7.82, 10.89, 15.56, 23.34, 36.71, 60.52, 105.9, 199.8, 410.6, 948.1, 2532],
    8: [1.39, 1.75, 2.27, 3.01, 4.06, 5.57, 7.83, 11.32, 16.96, 26.47, 42.35, 71.26, 127.3, 246, 522.8, 1253, 3422],
    9: [1.46, 1.90, 2.55, 3.52, 5.00, 7.30, 10.95, 16.95, 27.43, 46.58, 84.25, 163.2, 346.4, 813, 2176, 6765],
    10: [1.53, 2.06, 2.89, 4.16, 6.24, 9.74, 15.81, 26.81, 48.47, 93.12, 193, 437.2, 1093, 3124, 10311],
    11: [1.61, 2.25, 3.30, 5.00, 7.89, 13.13, 22.97, 42.95, 86.18, 185.9, 442.3, 1185, 3594, 12979],
    12: [1.69, 2.47, 3.81, 6.16, 10.47, 18.79, 36.11, 75.18, 169.6, 423.9, 1185, 3794, 14377],
    13: [1.79, 2.73, 4.47, 7.89, 14.96, 30.42, 67.61, 166.2, 457.6, 1423, 5125, 21965],
    14: [1.89, 3.04, 5.35, 10.47, 22.23, 52.85, 139.6, 415.8, 1415, 5693, 27704],
    15: [2.00, 3.42, 6.54, 14.14, 34.37, 95.43, 297.4, 1066, 4532, 23661],
    16: [2.13, 3.88, 8.17, 19.8, 55.44, 180.4, 704.8, 3292, 19016],
    17: [2.27, 4.45, 10.61, 29.22, 95.43, 375.7, 1858, 11508],
    18: [2.43, 5.17, 14.14, 46.75, 191.6, 959.9, 6067],
    19: [2.61, 6.09, 19.8, 82.64, 446.6, 3318],
    20: [2.83, 7.30, 29.7, 168.3, 1485],
    21: [3.09, 8.99, 49.5, 446.6],
    22: [3.42, 11.48, 99],
    23: [3.85, 16.17],
    24: [4.45]
}


def generate_mines_field(num_mines: int, seed: str) -> List[int]:
    """
    Generate mines positions using seed
    
    Args:
        num_mines: Number of mines (2-24)
        seed: Random seed for generation
    
    Returns:
        List of 25 cell states (0 = safe, 1 = mine)
    """
    # Create field with 25 cells
    field = [0] * 25
    
    # Use seed to generate deterministic mine positions
    random.seed(seed)
    mine_positions = random.sample(range(25), num_mines)
    
    for pos in mine_positions:
        field[pos] = 1
    
    return field


def calculate_mines_multiplier(num_mines: int, revealed_cells: int) -> float:
    """
    Get multiplier for current state
    
    Args:
        num_mines: Number of mines in game
        revealed_cells: Number of safe cells revealed
    
    Returns:
        Current multiplier
    """
    if num_mines not in MINES_MULTIPLIERS:
        return 1.0
    
    if revealed_cells == 0:
        return 1.0
    
    multipliers = MINES_MULTIPLIERS[num_mines]
    
    if revealed_cells > len(multipliers):
        return multipliers[-1]
    
    return multipliers[revealed_cells - 1]


def calculate_mines_payout(bet_amount: float, multiplier: float) -> Tuple[float, float]:
    """
    Calculate payout for mines game
    
    Returns:
        (gross_payout, net_payout)
    """
    gross_payout = bet_amount * multiplier
    commission = gross_payout * settings.CASINO_COMMISSION
    net_payout = gross_payout - commission
    
    return gross_payout, net_payout


class MinesGame:
    """Mines game manager"""
    
    def __init__(self, bet_amount: float, num_mines: int, server_seed: str, client_seed: str, nonce: int):
        self.bet_amount = bet_amount
        self.num_mines = num_mines
        self.server_seed = server_seed
        self.client_seed = client_seed
        self.nonce = nonce
        
        # Generate field
        combined_seed = f"{server_seed}:{client_seed}:{nonce}"
        self.field = generate_mines_field(num_mines, combined_seed)
        
        # Game state
        self.revealed_cells: List[int] = []
        self.is_finished = False
        self.is_won = False
        self.current_multiplier = 1.0
    
    def reveal_cell(self, cell_index: int) -> Dict:
        """
        Reveal a cell
        
        Returns:
            {
                "success": bool,
                "is_mine": bool,
                "multiplier": float,
                "game_finished": bool
            }
        """
        if self.is_finished:
            return {
                "success": False,
                "error": "Game already finished"
            }
        
        if cell_index in self.revealed_cells:
            return {
                "success": False,
                "error": "Cell already revealed"
            }
        
        if cell_index < 0 or cell_index >= 25:
            return {
                "success": False,
                "error": "Invalid cell index"
            }
        
        # Reveal cell
        self.revealed_cells.append(cell_index)
        is_mine = self.field[cell_index] == 1
        
        if is_mine:
            # Hit mine - game lost
            self.is_finished = True
            self.is_won = False
            return {
                "success": True,
                "is_mine": True,
                "multiplier": 0,
                "game_finished": True,
                "result": "lost"
            }
        else:
            # Safe cell
            num_revealed = len(self.revealed_cells)
            self.current_multiplier = calculate_mines_multiplier(self.num_mines, num_revealed)
            
            # Check if all safe cells revealed (jackpot)
            total_safe_cells = 25 - self.num_mines
            if num_revealed >= total_safe_cells:
                self.is_finished = True
                self.is_won = True
            
            return {
                "success": True,
                "is_mine": False,
                "multiplier": self.current_multiplier,
                "game_finished": self.is_finished,
                "revealed_cells": num_revealed,
                "can_cashout": True
            }
    
    def cashout(self) -> Dict:
        """
        Cashout current game
        
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
        
        if len(self.revealed_cells) == 0:
            return {
                "success": False,
                "error": "No cells revealed"
            }
        
        self.is_finished = True
        self.is_won = True
        
        gross_payout, net_payout = calculate_mines_payout(
            self.bet_amount,
            self.current_multiplier
        )
        
        profit = net_payout - self.bet_amount
        commission = gross_payout - net_payout
        
        return {
            "success": True,
            "profit": profit,
            "multiplier": self.current_multiplier,
            "commission": commission,
            "gross_payout": gross_payout,
            "net_payout": net_payout
        }
    
    def get_field_for_client(self) -> List[int]:
        """
        Get field state for client (hide unrevealed cells)
        
        Returns:
            List where:
            -1 = unrevealed
            0 = safe revealed
            1 = mine revealed
        """
        client_field = [-1] * 25
        
        for cell_index in self.revealed_cells:
            client_field[cell_index] = self.field[cell_index]
        
        return client_field
    
    def reveal_full_field(self) -> List[int]:
        """Reveal full field (after game ends)"""
        return self.field.copy()


# Test
if __name__ == "__main__":
    print("Testing Mines Game...")
    
    # Test multipliers
    print("\nMultipliers for 5 mines:")
    for i in range(1, 11):
        mult = calculate_mines_multiplier(5, i)
        print(f"  {i} cells revealed: x{mult}")
    
    # Test game
    print("\nTest game with 5 mines:")
    game = MinesGame(1.0, 5, "server_seed", "client_seed", 1)
    print(f"Field: {game.field}")
    print(f"Mines at positions: {[i for i, v in enumerate(game.field) if v == 1]}")
