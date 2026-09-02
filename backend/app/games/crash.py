"""
Crash game logic with Provably Fair system
"""
import hashlib
import hmac
from typing import Tuple
from ..core.config import settings


def generate_crash_point(server_seed: str, client_seed: str, nonce: int) -> float:
    """
    Generate crash point using Provably Fair algorithm
    
    Algorithm based on popular crash games:
    1. Combine seeds and nonce
    2. Generate hash
    3. Convert to crash multiplier
    4. Apply house edge
    
    Returns crash point (e.g., 1.56, 2.34, 150.23)
    """
    # Create combined string
    combined = f"{server_seed}:{client_seed}:{nonce}"
    
    # Generate HMAC-SHA256 hash
    hash_result = hmac.new(
        key=server_seed.encode(),
        msg=f"{client_seed}:{nonce}".encode(),
        digestmod=hashlib.sha256
    ).hexdigest()
    
    # Take first 13 characters and convert to number
    hex_substring = hash_result[:13]
    crash_value = int(hex_substring, 16)
    
    # Calculate crash point with house edge
    # House edge: 4% (96% RTP)
    house_edge = settings.HOUSE_EDGE
    
    # Generate crash point
    if crash_value == 0:
        crash_point = 1.00
    else:
        # Calculate multiplier
        e = 2 ** 52
        crash_point = (100 * e - house_edge * e) / (crash_value % e)
        crash_point = max(1.00, crash_point / 100)
        
        # Round to 2 decimal places
        crash_point = round(crash_point, 2)
    
    return crash_point


def calculate_crash_distribution(num_games: int = 10000) -> dict:
    """
    Calculate distribution of crash points for testing
    Returns statistics about crash point frequency
    """
    import random
    
    distribution = {
        "1.00-1.50": 0,
        "1.50-3.00": 0,
        "3.00-10.00": 0,
        "10.00-50.00": 0,
        "50.00-500.00": 0,
        "500.00+": 0
    }
    
    server_seed = hashlib.sha256(b"test_server").hexdigest()
    
    for i in range(num_games):
        client_seed = hashlib.sha256(f"test_client_{i}".encode()).hexdigest()
        crash_point = generate_crash_point(server_seed, client_seed, i)
        
        if crash_point < 1.50:
            distribution["1.00-1.50"] += 1
        elif crash_point < 3.00:
            distribution["1.50-3.00"] += 1
        elif crash_point < 10.00:
            distribution["3.00-10.00"] += 1
        elif crash_point < 50.00:
            distribution["10.00-50.00"] += 1
        elif crash_point < 500.00:
            distribution["50.00-500.00"] += 1
        else:
            distribution["500.00+"] += 1
    
    # Convert to percentages
    for key in distribution:
        distribution[key] = round(distribution[key] / num_games * 100, 2)
    
    return distribution


def verify_crash_result(
    server_seed: str,
    client_seed: str,
    nonce: int,
    claimed_crash_point: float
) -> bool:
    """
    Verify that crash result is fair
    Used by players to check game fairness
    """
    calculated = generate_crash_point(server_seed, client_seed, nonce)
    return abs(calculated - claimed_crash_point) < 0.01


def calculate_payout(bet_amount: float, multiplier: float, crash_point: float) -> Tuple[bool, float]:
    """
    Calculate payout for crash game
    
    Args:
        bet_amount: Amount bet
        multiplier: Multiplier player cashed out at
        crash_point: Point where game crashed
    
    Returns:
        (is_win, payout_amount)
    """
    # Player wins if they cashed out before crash
    if multiplier < crash_point:
        # Win
        gross_payout = bet_amount * multiplier
        commission = gross_payout * settings.CASINO_COMMISSION
        net_payout = gross_payout - commission
        profit = net_payout - bet_amount
        
        return True, profit
    else:
        # Lost (crashed before cashout)
        return False, -bet_amount


# ============= Game Flow =============

class CrashGame:
    """Crash game manager"""
    
    def __init__(self, server_seed: str, client_seed: str, nonce: int):
        self.server_seed = server_seed
        self.client_seed = client_seed
        self.nonce = nonce
        self.crash_point = generate_crash_point(server_seed, client_seed, nonce)
        self.hash = self.generate_hash()
    
    def generate_hash(self) -> str:
        """Generate hash for next game (provably fair)"""
        return hashlib.sha256(
            f"{self.server_seed}:{self.client_seed}:{self.nonce}".encode()
        ).hexdigest()
    
    def can_cashout(self, current_multiplier: float) -> bool:
        """Check if player can cashout at current multiplier"""
        return current_multiplier < self.crash_point
    
    def get_result(self, cashout_multiplier: float) -> dict:
        """Get game result"""
        is_win = cashout_multiplier < self.crash_point
        
        return {
            "crash_point": self.crash_point,
            "cashout_multiplier": cashout_multiplier,
            "is_win": is_win,
            "can_verify": True,
            "server_seed": self.server_seed,
            "client_seed": self.client_seed,
            "nonce": self.nonce,
            "hash": self.hash
        }


# Test the distribution
if __name__ == "__main__":
    print("Testing Crash Game Distribution...")
    dist = calculate_crash_distribution(10000)
    print("\nDistribution over 10,000 games:")
    for range_name, percentage in dist.items():
        print(f"{range_name}: {percentage}%")
    
    # Test specific game
    print("\n\nTest game:")
    server = hashlib.sha256(b"server_test").hexdigest()
    client = hashlib.sha256(b"client_test").hexdigest()
    game = CrashGame(server, client, 1)
    print(f"Crash point: {game.crash_point}x")
    print(f"Hash: {game.hash}")
    print(f"Can verify: {verify_crash_result(server, client, 1, game.crash_point)}")
