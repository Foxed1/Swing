# trades_manager.py

import json
import os

TRADES_FILE = "open_trades.json"

def save_trade(symbol, entry_price, target_price, stop_price):
    trades = load_trades()
    trades.append({
        "symbol": symbol,
        "entry_price": entry_price,
        "target_price": target_price,
        "stop_price": stop_price
    })
    with open(TRADES_FILE, "w") as f:
        json.dump(trades, f, indent=4)

def load_trades():
    if not os.path.exists(TRADES_FILE):
        return []
    with open(TRADES_FILE, "r") as f:
        return json.load(f)

def remove_trade(symbol):
    trades = load_trades()
    trades = [t for t in trades if t["symbol"] != symbol]
    with open(TRADES_FILE, "w") as f:
        json.dump(trades, f, indent=4)
