from tradingview_ta import TA_Handler, Interval
from config import TIMEFRAME
import logging

logger = logging.getLogger(__name__)

def analyze_symbol(symbol):
    try:
        handler = TA_Handler(
            symbol=symbol,
            screener="crypto",
            exchange="BINANCE",
            interval=Interval.INTERVAL_4_HOURS
        )
        analysis = handler.get_analysis()
        indicators = analysis.indicators
        
        if not indicators or 'close' not in indicators:
            logger.warning(f"⚠️ بيانات غير كاملة لـ {symbol}")
            return None
            
        return {
            "price": indicators.get("close"),
            "close": indicators.get("close"),  # مطلوب لـ technical_analyzer
            "EMA50": indicators.get("EMA50"),
            "EMA200": indicators.get("EMA200"),
            "RSI": indicators.get("RSI", 50),  # قيمة افتراضية إذا لم توجد
            "ADX": indicators.get("ADX", 25),
            "summary": analysis.summary
        }
    except Exception as e:
        logger.error(f"❌ فشل تحليل {symbol}: {str(e)}")
        return None
