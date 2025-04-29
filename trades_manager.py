import json
from datetime import datetime, timedelta

def load_trades():
    try:
        with open('open_trades.json', 'r') as file:
            return json.load(file)
    except:
        return []

def save_trade(symbol, entry_price, target_price, stop_loss):
    trades = load_trades()
    trades.append({
        "symbol": symbol,
        "entry_price": entry_price,
        "target_price": target_price,
        "stop_loss": stop_loss,
        "open_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    with open('open_trades.json', 'w') as file:
        json.dump(trades, file, indent=4)

def save_all_trades(trades):
    with open('open_trades.json', 'w') as file:
        json.dump(trades, file, indent=4)

def remove_trade(symbol):
    trades = load_trades()
    trades = [trade for trade in trades if trade["symbol"] != symbol]
    save_all_trades(trades)

def clean_old_trades(trades):
    now = datetime.now()
    threshold = now - timedelta(days=30)
    new_trades = []
    for trade in trades:
        open_time_str = trade.get('open_time')
        if open_time_str:
            open_time = datetime.strptime(open_time_str, '%Y-%m-%d %H:%M:%S')
            if open_time > threshold:
                new_trades.append(trade)
            else:
                print(f"🧹 حذف صفقة قديمة على {trade['symbol']} فتحت بتاريخ {open_time_str}")
        else:
            new_trades.append(trade)
    return new_trades
