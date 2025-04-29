import logging
import numpy as np
from technical_analyzer import calculate_moving_averages

# إعدادات التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def analyze_levels(symbol, price_data=None):
    """
    دالة محسنة لتحليل مستويات الدعم/المقاومة
    مع معالجة الحالات الطارئة بقيم افتراضية
    """
    try:
        # يمكن استبدال هذا الجزء بتحليل حقيقي من API
        return {
            "levels": {
                "support": [price_data * 0.98, price_data * 0.95] if price_data else [],
                "resistance": [price_data * 1.02, price_data * 1.05] if price_data else []
            },
            "patterns": ["Hammer", "Bullish Engulfing"]  # أنماط افتراضية
        }
    except Exception as e:
        logger.error(f"❌ فشل تحليل المستويات لـ {symbol}: {e}")
        return {
            "levels": {"support": [], "resistance": []},
            "patterns": []
        }

def check_entry_conditions(data, symbol):
    """
    دالة محسنة للتحقق من شروط الدخول مع معالجة جميع الأخطاء المحتملة
    """
    if not data or not isinstance(data, dict):
        logger.warning(f"⚠️ بيانات غير صالحة لـ {symbol}")
        return False

    try:
        ma = calculate_moving_averages(data)
        if not ma:
            return False

        levels = analyze_levels(symbol, data.get('price'))
        
        # شروط الدخول مع قيم افتراضية آمنة
        conditions = [
            str(ma.get('signal', '')).strip().lower() == 'شراء',
            float(data.get('price', 0)) > float(ma.get('ma200', 1)),
            float(ma.get('ma9', 0)) > float(ma.get('ma21', 0)),
            any(p in levels.get('patterns', []) for p in ["Hammer", "Bullish Engulfing"]),
            float(data.get('RSI', 0)) > 50,
            float(data.get('ADX', 0)) > 25  # شرط إضافي لقوة الاتجاه
        ]
        
        logger.debug(f"🔍 {symbol} - شروط الدخول: {conditions}")
        return all(conditions)
        
    except Exception as e:
        logger.error(f"🔥 خطأ حرج في تحليل الشروط لـ {symbol}: {str(e)}", exc_info=True)
        return False

def build_trade_message(symbol, data, entry_price, targets):
    """
    دالة محسنة لبناء رسالة التداول مع معالجة جميع الأخطاء
    """
    try:
        ma = calculate_moving_averages(data) or {}
        levels = analyze_levels(symbol, data.get('price'))
        
        msg_lines = [
            f"📈 *إشارة تداول متقدمة* - {symbol}",
            f"⚡ السعر الحالي: {data.get('price', 'N/A'):.4f}",
            f"🎯 نقاط الدخول: {entry_price:.4f}",
            f"✅ أهداف الربح: {', '.join([f'{tp:.4f}' for tp in targets.get('take_profit', [])})",
            f"🛑 وقف الخسارة: {targets.get('stop_loss', 'N/A'):.4f}",
            "---",
            f"📊 المؤشرات الفنية:",
            f"• RSI: {data.get('RSI', 'N/A'):.1f}",
            f"• ADX: {data.get('ADX', 'N/A'):.1f}",
            f"• MA9/MA21: {ma.get('ma9', 'N/A'):.2f}/{ma.get('ma21', 'N/A'):.2f}",
            f"• الأنماط: {', '.join(levels.get('patterns', ['لا يوجد']))}"
        ]
        
        return "\n".join(msg_lines)
        
    except Exception as e:
        logger.error(f"🔥 فشل بناء الرسالة: {str(e)}")
        return f"📌 إشارة تداول لـ {symbol} عند {entry_price:.4f} (تفاصيل غير متاحة)"
