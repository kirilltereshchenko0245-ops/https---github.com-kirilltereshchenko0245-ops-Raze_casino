"""
Roulette game logic - x2, x3, x5, x30 multipliers
"""
import random
import hashlib
from typing import Dict, Tuple, List
from ..core.config import settings


# Roulette configuration
ROULETTE_MULTIPLIERS = {
    "x2": {
        "multiplier": 2.0,
        "color": "blue",
        "weight": 47,  # 47% chance
        "sectors": 47
    },
    "x3": {
        "multiplier": 3.0,
        "color": "yellow", 
        "weight": 30,  # 30% chance
        "sectors": 30
    },
    "x5": {
        "multiplier": 5.0,
        "color": "red",
        "weight": 20,  # 20% chance
        "sectors": 20
    },
    "x30": {
        "multiplier": 30.0,
        "color": "green",
        "weight": 3,  # 3% chance
        "sectors": 3
    }
}

# Total sectors = 100 (for easy probability calculation)
TOTAL_SECTORS = 100


def generate_roulette_result(server_seed: str, client_seed: str, nonce: int) -> Dict:
    """
    Generate roulette result using provably fair system
    
    Returns:
        {
            "sector": int (0-99),
            "result": str ("x2", "x3", "x5", "x30"),
            "multiplier": float,
            "color": str
        }
    """
    # Create seed
    combined_seed = f"{server_seed}:{client_seed}:{nonce}"
    hash_result = hashlib.sha256(combined_seed.encode()).hexdigest()
    
    # Convert hash to number between 0-99
    sector = int(hash_result[:8], 16) % TOTAL_SECTORS
    
    # Determine result based on sector
    # Sectors: 0-46 = x2, 47-76 = x3, 77-96 = x5, 97-99 = x30
    if sector < 47:
        result = "x2"
    elif sector < 77:
        result = "x3"
    elif sector < 97:
        result = "x5"
    else:
        result = "x30"
    
    config = ROULETTE_MULTIPLIERS[result]
    
    return {
        "sector": sector,
        "result": result,
        "multiplier": config["multiplier"],
        "color": config["color"]
    }


def calculate_roulette_payout(bet_amount: float, bet_on: str, actual_result: str) -> Tuple[bool, float, float]:
    """
    Calculate payout for roulette bet
    
    Args:
        bet_amount: Amount bet
        bet_on: What player bet on ("x2", "x3", "x5", "x30")
        actual_result: Actual result
    
    Returns:
        (is_win, profit, commission)
    """
    if bet_on == actual_result:
        # Win
        multiplier = ROULETTE_MULTIPLIERS[actual_result]["multiplier"]
        gross_payout = bet_amount * multiplier
        commission = gross_payout * settings.CASINO_COMMISSION
        net_payout = gross_payout - commission
        profit = net_payout - bet_amount
        
        return True, profit, commission
    else:
        # Lose
        return False, -bet_amount, 0


def generate_roulette_wheel() -> List[Dict]:
    """
    Generate roulette wheel sectors for UI
    
    Returns list of sectors with colors
    """
    wheel = []
    
    # Create 100 sectors based on probabilities
    # x2 (blue): 0-46
    for i in range(47):
        wheel.append({"sector": i, "type": "x2", "color": "blue"})
    
    # x3 (yellow): 47-76
    for i in range(47, 77):
        wheel.append({"sector": i, "type": "x3", "color": "yellow"})
    
    # x5 (red): 77-96
    for i in range(77, 97):
        wheel.append({"sector": i, "type": "x5", "color": "red"})
    
    # x30 (green): 97-99
    for i in range(97, 100):
        wheel.append({"sector": i, "type": "x30", "color": "green"})
    
    return wheel


class RouletteGame:
    """Roulette game manager"""
    
    def __init__(self, bet_amount: float, bet_on: str, server_seed: str, client_seed: str, nonce: int):
        self.bet_amount = bet_amount
        self.bet_on = bet_on
        self.server_seed = server_seed
        self.client_seed = client_seed
        self.nonce = nonce
        
        # Validate bet
        if bet_on not in ROULETTE_MULTIPLIERS:
            raise ValueError(f"Invalid bet type: {bet_on}")
        
        # Generate result
        self.result = generate_roulette_result(server_seed, client_seed, nonce)
        self.hash = hashlib.sha256(
            f"{server_seed}:{client_seed}:{nonce}".encode()
        ).hexdigest()
    
    def get_result(self) -> Dict:
        """Get game result"""
        is_win, profit, commission = calculate_roulette_payout(
            self.bet_amount,
            self.bet_on,
            self.result["result"]
        )
        
        if is_win:
            gross_payout = self.bet_amount * self.result["multiplier"]
            net_payout = gross_payout - commission
        else:
            gross_payout = 0
            net_payout = 0
        
        return {
            "bet_amount": self.bet_amount,
            "bet_on": self.bet_on,
            "result": self.result["result"],
            "sector": self.result["sector"],
            "multiplier": self.result["multiplier"],
            "color": self.result["color"],
            "is_win": is_win,
            "profit": profit,
            "commission": commission,
            "gross_payout": gross_payout,
            "net_payout": net_payout,
            "hash": self.hash,
            "can_verify": True
        }
    
    def get_animation_data(self) -> Dict:
        """
        Get data for roulette animation
        
        Returns sector to land on and spin duration
        """
        # Calculate spins (3-5 full rotations + landing position)
        base_spins = 3
        extra_rotation = random.uniform(0, 2)
        total_rotation = (base_spins + extra_rotation) * 360
        
        # Add sector position
        sector_angle = (self.result["sector"] / TOTAL_SECTORS) * 360
        final_angle = total_rotation + sector_angle
        
        return {
            "final_angle": final_angle,
            "sector": self.result["sector"],
            "duration": 5000,  # 5 seconds
            "result": self.result["result"]
        }


def verify_roulette_result(
    server_seed: str,
    client_seed: str,
    nonce: int,
    claimed_sector: int,
    claimed_result: str
) -> bool:
    """Verify roulette result is fair"""
    actual = generate_roulette_result(server_seed, client_seed, nonce)
    
    return (actual["sector"] == claimed_sector and 
            actual["result"] == claimed_result)


def calculate_roulette_stats(num_spins: int = 10000) -> Dict:
    """
    Calculate distribution statistics for testing
    """
    results = {"x2": 0, "x3": 0, "x5": 0, "x30": 0}
    
    server_seed = hashlib.sha256(b"test_server").hexdigest()
    
    for i in range(num_spins):
        client_seed = hashlib.sha256(f"test_{i}".encode()).hexdigest()
        result = generate_roulette_result(server_seed, client_seed, i)
        results[result["result"]] += 1
    
    # Convert to percentages
    stats = {}
    for key, count in results.items():
        percentage = (count / num_spins) * 100
        expected = ROULETTE_MULTIPLIERS[key]["weight"]
        stats[key] = {
            "actual": round(percentage, 2),
            "expected": expected,
            "count": count
        }
    
    return stats


# Test
if __name__ == "__main__":
    print("Testing Roulette Game...")
    
    # Test distribution
    print("\nDistribution over 10,000 spins:")
    stats = calculate_roulette_stats(10000)
    for multiplier, data in stats.items():
        print(f"  {multiplier}: {data['actual']}% (expected: {data['expected']}%) - {data['count']} times")
    
    # Test single game
    print("\nTest game:")
    game = RouletteGame(
        bet_amount=1.0,
        bet_on="x5",
        server_seed="test_server",
        client_seed="test_client",
        nonce=1
    )
    result = game.get_result()
    print(f"  Bet on: {result['bet_on']}")
    print(f"  Result: {result['result']} (sector {result['sector']})")
    print(f"  Win: {result['is_win']}")
    print(f"  Profit: ${result['profit']:.2f}")
    
    # Test animation data
    animation = game.get_animation_data()
    print(f"\nAnimation data:")
    print(f"  Final angle: {animation['final_angle']}°")
    print(f"  Duration: {animation['duration']}ms")
