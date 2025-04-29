# trades_manager.py
import json
import os

TRADES_FILE = "trades_v2.json"

def save_trade(symbol, entry_price, targets, stop_loss):
    trades = load_trades()
    trades.append({
        "symbol": symbol,
        "entry_price": entry_price,
        "targets": targets,
        "stop_loss": stop_loss,
        "partial_taken": False,
        "opened_at": int(time.time())
    })
    with open(TRADES_FILE, 'w') as f:
        json.dump(trades, f, indent=2)

def load_trades():
    if not os.path.exists(TRADES_FILE):
        return []
    with open(TRADES_FILE) as f:
        return json.load(f)

def remove_trade(symbol):
    trades = [t for t in load_trades() if t["symbol"] != symbol]
    with open(TRADES_FILE, 'w') as f:
        json.dump(trades, f, indent=2)
