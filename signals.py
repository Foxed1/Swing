def check_entry_conditions(data):
    ma = calculate_moving_averages(data)
    levels = analyze_levels(data['symbol'])
    
    # شروط الدخول المعززة بالمتوسطات
    conditions = [
        ma['signal'] == 'شراء',
        data['price'] > ma['ma200'],  # فوق المتوسط الطويل
        ma['ma9'] > ma['ma21'],       # تقاطع ذهبي
        any(p in levels['patterns'] for p in ["Hammer", "Bullish Engulfing"]),
        data['RSI'] > 50              # زخم إيجابي
    ]
    
    return all(conditions)

def build_trade_message(symbol, data, levels, targets):
    ma = calculate_moving_averages(data)
    msg = [
        "📈 *إشارة تداول متقدمة*",
        f"• العملة: {symbol} | السعر: {data['price']:.4f}",
        f"• الدخول: {targets['entry']:.4f}",
        f"• الأهداف: {targets['take_profit']:.4f}",
        f"• وقف الخسارة: {targets['stop_loss']:.4f}",
        "",
        "📊 *التحليل الفني:*",
        f"• المتوسطات: MA9({ma['ma9']:.2f}) > MA21({ma['ma21']:.2f}) > MA50({ma['ma50']:.2f})",
        f"• الاتجاه: {ma['trend']} | إشارة: {ma['signal']}",
        f"• Pivot: {levels['pivot']:.2f} | R1: {levels['r1']:.2f}",
        f"• أنماط الشموع: {', '.join(levels['patterns'])}",
        f"• RSI: {data['RSI']:.1f} | ADX: {data['ADX']:.1f}"
    ]
    return "\n".join(msg)
