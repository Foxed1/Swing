# analyzer.py

from tradingview_ta import TA_Handler, Interval
from config import TIMEFRAME

def analyze_symbol(symbol):
    handler = TA_Handler(
        symbol=symbol,
        screener="crypto",
        exchange="BINANCE",
        interval=Interval.INTERVAL_4_HOURS
    )
    try:
        analysis = handler.get_analysis()
        indicators = analysis.indicators
        summary = analysis.summary
        return {
            "price": indicators.get("close"),
            "EMA50": indicators.get("EMA50"),
            "EMA200": indicators.get("EMA200"),
            "MACD.macd": indicators.get("MACD.macd"),
            "MACD.signal": indicators.get("MACD.signal"),
            "RSI": indicators.get("RSI"),
            "ADX": indicators.get("ADX"),
            "summary": summary
        }
    except Exception as e:
        print(f"Error analyzing {symbol}: {e}")
        return None
