import datetime

BALANCE_FILE = 'balance.txt'
CAPITAL = 1000
COMMISSION = 4.95

def save_balance_to_file(balance):
    """Saves the balance to a txt file."""
    with open(BALANCE_FILE, 'w') as f:
        f.write(str(CAPITAL)) # for the moment its capital

def load_balance_from_file():
    """Loads the balance from a txt file. If not found, returns the initial CAPITAL."""
    try:
        with open(BALANCE_FILE, 'r') as f:
            return float(f.read().strip())
    except FileNotFoundError:
        return CAPITAL
