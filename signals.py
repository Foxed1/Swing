import logging
from technical_analyzer import calculate_moving_averages

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def analyze_levels(symbol):
    """
    دالة جديدة لتحليل مستويات الدعم/المقاومة
    (يمكن استبدالها بتحليل حقيقي من API أو مكتبة أخرى)
    """
    return {
        "levels": [],  # قائمة بمستويات الدعم/المقاومة
        "patterns": ["Hammer", "Bullish Engulfing"]  # أنماط افتراضية
    }

def check_entry_conditions(data, symbol):
    try:
        ma = calculate_moving_averages(data)
        levels = analyze_levels(symbol)  # سيتم استخدام الدالة الجديدة
        
        conditions = [
            ma.get('signal') == 'شراء',
            data.get('price', 0) > ma.get('ma200', 0),
            ma.get('ma9', 0) > ma.get('ma21', 0),
            any(p in levels.get('patterns', []) for p in ["Hammer", "Bullish Engulfing"]),
            data.get('RSI', 0) > 50
        ]
        
        logger.info(f"📊 تحليل {symbol}: شروط الدخول -> {conditions}")
        return all(conditions)
    except Exception as e:
        logger.error(f"🔥 خطأ في تحليل الشروط: {e}")
        return False

def build_trade_message(symbol, data, entry_price, targets):
    try:
        ma = calculate_moving_averages(data)
        msg = [
            f"📈 *إشارة تداول*: {symbol}",
            f"💰 السعر: {data.get('price', 0):.4f} | الدخول: {entry_price:.4f}",
            f"🎯 الأهداف: {', '.join(map(str, targets))}",
            f"🛑 وقف الخسارة: {targets.get('stop_loss', 0):.4f}",
            f"📊 RSI: {data.get('RSI', 0):.1f} | ADX: {data.get('ADX', 0):.1f}"
        ]
        return "\n".join(msg)
    except Exception as e:
        logger.error(f"🔥 خطأ في بناء الرسالة: {e}")
        return "⚠️ تعذر إنشاء تفاصيل الصفقة"
