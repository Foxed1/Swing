import logging
from technical_analyzer import calculate_moving_averages

# إعدادات التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def analyze_levels(symbol, price_data=None):
    """
    تحليل مستويات الدعم/المقاومة (إصدار آمن)
    """
    try:
        return {
            "levels": {
                "support": [price_data * 0.98, price_data * 0.95] if price_data else [],
                "resistance": [price_data * 1.02, price_data * 1.05] if price_data else []
            },
            "patterns": ["Hammer", "Bullish Engulfing"]
        }
    except Exception as e:
        logger.error(f"فشل تحليل المستويات: {e}")
        return {"levels": {"support": [], "resistance": []}, "patterns": []}

def check_entry_conditions(data, symbol):
    """
    التحقق من شروط الدخول مع معالجة الأخطاء
    """
    if not data:
        logger.warning(f"لا يوجد بيانات لـ {symbol}")
        return False

    try:
        ma = calculate_moving_averages(data) or {}
        levels = analyze_levels(symbol, data.get('price'))
        
        conditions = [
            str(ma.get('signal', '')).lower() == 'شراء',
            float(data.get('price', 0)) > float(ma.get('ma200', 1)),
            float(ma.get('ma9', 0)) > float(ma.get('ma21', 0)),
            any(p in levels.get('patterns', []) for p in ["Hammer", "Bullish Engulfing"]),
            float(data.get('RSI', 0)) > 50
        ]
        return all(conditions)
    except Exception as e:
        logger.error(f"خطأ في شروط الدخول: {e}")
        return False

def build_trade_message(symbol, data, entry_price, targets):
    """
    بناء رسالة التداول (إصدار معدل بدون أخطاء تركيبية)
    """
    try:
        take_profit_str = ", ".join([f"{tp:.4f}" for tp in targets.get('take_profit', [])])
        stop_loss_str = f"{targets.get('stop_loss', 0):.4f}"
        
        ma = calculate_moving_averages(data) or {}
        levels = analyze_levels(symbol, data.get('price')) or {}
        
        message_lines = [
            f"📈 إشارة تداول: {symbol}",
            f"💰 السعر: {data.get('price', 0):.4f}",
            f"🎯 الأهداف: {take_profit_str}",
            f"🛑 وقف الخسارة: {stop_loss_str}",
            f"📊 RSI: {data.get('RSI', 0):.1f}",
            f"📈 MA9/MA21: {ma.get('ma9', 0):.2f}/{ma.get('ma21', 0):.2f}",
            f"🔄 الأنماط: {', '.join(levels.get('patterns', []))}"
        ]
        return "\n".join(message_lines)
    except Exception as e:
        logger.error(f"فشل بناء الرسالة: {e}")
        return f"📌 إشارة شراء لـ {symbol} عند {entry_price:.4f}"
