# signals.py
from utils import determine_trend_strength
from ai_predictor import load_all_models
from config import SYMBOLS, MIN_AI_CONFIDENCE

ai_models = load_all_models(SYMBOLS)

def check_entry_conditions(data, symbol):
    if not data:
        return False

    # 1. فلترة السيولة
    if data.get("volume", 0) < MIN_VOLUME:
        return False

    # 2. تنبؤ الذكاء الاصطناعي
    ai_prediction = ai_models[symbol].predict([[data["EMA50"], data["RSI"]]])[0]
    ai_confidence = ai_models[symbol].predict_proba([[data["EMA50"], data["RSI"]]])[0][1]
    
    if ai_prediction == 0 or ai_confidence < MIN_AI_CONFIDENCE:
        return False

    # 3. شروط المؤشرات
    conditions = [
        data["EMA50"] > data["EMA200"],
        data["MACD.macd"] > data["MACD.signal"],
        40 <= data["RSI"] <= 70,
        data["ADX"] >= 20,
        data["summary"]["RECOMMENDATION"] in ["BUY", "STRONG_BUY"]
    ]
    return all(conditions)

def build_trade_message(symbol, data, entry_price, targets):
    message = (
        f"🚀 *إشارة ذكية - {symbol}*\n\n"
        f"• السعر: {entry_price:.4f}\n"
        f"• الأهداف: {', '.join([f'{t:.4f}' for t in targets])}\n"
        f"• الثقة: {ai_models[symbol].predict_proba([[data['EMA50'], data['RSI']]])[0][1]:.0%}\n"
        f"• RSI: {data['RSI']:.1f} | ADX: {data['ADX']:.1f}\n"
        f"• التقييم: {data['summary']['RECOMMENDATION']}"
    )
    return message
