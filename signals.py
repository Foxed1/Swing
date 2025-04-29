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
    if not data:
        logger.warning(f"⚠️ لا يوجد بيانات لـ {symbol}")
        return False
        
    try:
        ma = calculate_moving_averages(data)
        if not ma:
            return False
            
        levels = analyze_levels(symbol)
        
        conditions = [
            ma.get('signal', 'انتظار') == 'شراء',
            float(data.get('price', 0)) > float(ma.get('ma200', 0)),
            float(ma.get('ma9', 0)) > float(ma.get('ma21', 0)),
            any(p in levels.get('patterns', []) for p in ["Hammer", "Bullish Engulfing"]),
            float(data.get('RSI', 0)) > 50
        ]
        
        logger.info(f"📊 تحليل {symbol}: الشروط -> {conditions}")
        return all(conditions)
    except Exception as e:
        logger.error(f"🔥 خطأ في شروط الدخول: {e}")
        return False
