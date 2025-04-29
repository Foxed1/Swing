import json
import os
from datetime import datetime
import logging
from config import RISK_PERCENT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TRADES_FILE = "active_trades_v2.json"

def save_trade(symbol, entry_price, targets, stop_loss, indicators, **kwargs):
    trades = load_trades()
    trade_data = {
        "symbol": symbol,
        "entry_price": entry_price,
        "targets": targets,
        "stop_loss": stop_loss,
        "indicators": indicators,
        **kwargs  # يدعم حقولاً مخصصة مثل partial_taken
    }
    
    trades.append(trade_data)
    with open(TRADES_FILE, 'w') as f:
        json.dump(trades, f, indent=4)
    
    logger.info(f"💾 تم حفظ صفقة {symbol} | السعر: {entry_price}")

def load_trades():
    if not os.path.exists(TRADES_FILE):
        return []
    try:
        with open(TRADES_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"❌ خطأ في تحميل الصفقات: {e}")
        return []

def remove_trade(symbol):
    trades = [t for t in load_trades() if t["symbol"] != symbol]
    with open(TRADES_FILE, 'w') as f:
        json.dump(trades, f, indent=4)
    logger.info(f"🗑️ تم إغلاق صفقة {symbol}")
