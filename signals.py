import logging
from technical_analyzer import calculate_moving_averages

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_entry_conditions(data, symbol):
    ma = calculate_moving_averages(data)
    levels = analyze_levels(symbol)
    
    conditions = [
        ma['signal'] == 'شراء',
        data['price'] > ma['ma200'],
        ma['ma9'] > ma['ma21'],
        any(p in levels['patterns'] for p in ["Hammer", "Bullish Engulfing"]),
        data['RSI'] > 50
    ]
    
    logger.info(f"📊 تحليل {symbol}: شروط الدخول -> {conditions}")
    return all(conditions)

def build_trade_message(symbol, data, entry_price, targets):
    ma = calculate_moving_averages(data)
    msg = [
        f"📈 *إشارة تداول*: {symbol}",
        f"💰 السعر: {data['price']:.4f} | الدخول: {entry_price:.4f}",
        f"🎯 الأهداف: {', '.join([str(t) for t in targets])}",
        f"🛑 وقف الخسارة: {targets['stop_loss']:.4f}",
        f"📊 RSI: {data['RSI']:.1f} | ADX: {data['ADX']:.1f}"
    ]
    return "\n".join(msg)
