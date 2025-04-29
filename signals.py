# signals.py

from utils import determine_trend_strength

def check_entry_conditions(data):
    if not data:
        return False

    if data["EMA50"] and data["EMA200"]:
        if data["EMA50"] < data["EMA200"]:
            return False

    if data["MACD.macd"] and data["MACD.signal"]:
        if data["MACD.macd"] < data["MACD.signal"]:
            return False

    if data["RSI"] is not None and not (40 <= data["RSI"] <= 65):
        return False

    if data["ADX"] is not None and data["ADX"] < 20:
        return False

    if data["summary"]["RECOMMENDATION"] not in ["BUY", "STRONG_BUY"]:
        return False

    return True

def build_trade_message(symbol, data, entry_price, target_price, stop_price):
    trend_strength = determine_trend_strength(data["ADX"])
    message = f"🚀 *فرصة شراء* على {symbol}\n\n"
    message += f"*سعر الدخول:* {entry_price}\n"
    message += f"*الهدف المتوقع:* {target_price}\n"
    message += f"*وقف الخسارة:* {stop_price}\n\n"
    message += f"*RSI:* {round(data['RSI'],2)}\n"
    message += f"*ADX:* {round(data['ADX'],2)} ({trend_strength})\n"
    message += f"*تقييم TradingView:* {data['summary']['RECOMMENDATION']}\n"
    return message
