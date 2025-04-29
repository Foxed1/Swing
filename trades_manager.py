import json
import os
import logging
from datetime import datetime
from config import RISK_PERCENT

# إعدادات التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TRADES_FILE = "active_trades.json"

def load_trades():
    """تحميل جميع الصفقات النشطة من الملف"""
    try:
        if not os.path.exists(TRADES_FILE):
            return []
            
        with open(TRADES_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"❌ خطأ في تحميل الصفقات: {e}")
        return []

def save_trade(symbol, entry_price, targets, stop_loss, indicators, **kwargs):
    """حفظ الصفقة الجديدة مع بيانات التحليل الفني"""
    trades = load_trades()
    
    trade_data = {
        "symbol": symbol,
        "entry_price": entry_price,
        "targets": targets,
        "stop_loss": stop_loss,
        "indicators": indicators,
        "opened_at": datetime.now().isoformat(),
        **kwargs
    }
    
    trades.append(trade_data)
    
    try:
        with open(TRADES_FILE, 'w') as f:
            json.dump(trades, f, indent=4)
        logger.info(f"💾 تم حفظ صفقة {symbol}")
    except Exception as e:
        logger.error(f"❌ فشل حفظ صفقة {symbol}: {e}")

def remove_trade(symbol):
    """إزالة الصفقة عند الإغلاق"""
    trades = [t for t in load_trades() if t["symbol"] != symbol]
    
    try:
        with open(TRADES_FILE, 'w') as f:
            json.dump(trades, f, indent=4)
        logger.info(f"🗑️ تم إغلاق صفقة {symbol}")
    except Exception as e:
        logger.error(f"❌ فشل إغلاق صفقة {symbol}: {e}")

def update_trade(symbol, new_data):
    """تحديث بيانات صفقة موجودة"""
    trades = load_trades()
    updated = False
    
    for trade in trades:
        if trade["symbol"] == symbol:
            trade.update(new_data)
            updated = True
            
    if updated:
        try:
            with open(TRADES_FILE, 'w') as f:
                json.dump(trades, f, indent=4)
            logger.info(f"🔄 تم تحديث صفقة {symbol}")
        except Exception as e:
            logger.error(f"❌ فشل تحديث صفقة {symbol}: {e}")
