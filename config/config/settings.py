import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FILTERS = {
    'max_supply': 1_000_000_000,
    'min_mcap': 150_000,
    'min_liquidity': 90_000,
    'min_liquidity_lock': 99,
    'max_dev_holding': 0.20,
    'max_top10_holding': 0.35,
    'min_markers': 200,
    'min_holders': 100,
    'min_volume': 500_000
}

CHECK_INTERVAL = 120  # Seconds
