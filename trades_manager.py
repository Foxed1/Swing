import json
import os
from datetime import datetime
from config import RISK_PERCENT

TRADES_FILE = "active_trades_v2.json"

def save_trade(symbol, entry_price, targets, stop_loss, indicators):
    """
    حفظ الصفقة الجديدة مع بيانات التحليل الفني
    """
    trades = load_trades()
    
    trade_data = {
        "symbol": symbol,
        "entry_price": entry_price,
        "targets": targets,
        "stop_loss": stop_loss,
        "opened_at": datetime.now().isoformat(),
        "indicators": {
            "ma_status": indicators['ma_status'],
            "pivot_levels": indicators['pivot_levels'],
            "candle_pattern": indicators['candle_pattern'],
            "volume": indicators['volume']
        },
        "risk_management": {
            "risk_percent": RISK_PERCENT,
            "reward_ratio": round((targets[0]/entry_price - 1)/(1 - stop_loss/entry_price), 2)
        }
    }
    
    trades.append(trade_data)
    
    with open(TRADES_FILE, 'w') as f:
        json.dump(trades, f, indent=4)

def load_trades():
    """
    تحميل جميع الصفقات النشطة
    """
    if not os.path.exists(TRADES_FILE):
        return []
        
    with open(TRADES_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def remove_trade(symbol):
    """
    إزالة الصفقة عند الإغلاق
    """
    trades = [t for t in load_trades() if t["symbol"] != symbol]
    
    with open(TRADES_FILE, 'w') as f:
        json.dump(trades, f, indent=4)

def update_trade(symbol, new_data):
    """
    تحديث بيانات الصفقة (مثل تعديل وقف الخسارة)
    """
    trades = load_trades()
    updated = False
    
    for trade in trades:
        if trade["symbol"] == symbol:
            trade.update(new_data)
            updated = True
            
    if updated:
        with open(TRADES_FILE, 'w') as f:
            json.dump(trades, f, indent=4)

def get_trade(symbol):
    """
    استرجاع بيانات صفقة محددة
    """
    trades = load_trades()
    return next((t for t in trades if t["symbol"] == symbol), None)

# دالة مساعدة لحساب الربح/الخسارة
def calculate_pnl(trade, current_price):
    entry = trade["entry_price"]
    return ((current_price - entry) / entry) * 100
