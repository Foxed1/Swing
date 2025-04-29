def save_trade(symbol, entry_price, targets, stop_loss, indicators, **kwargs):
    trades = load_trades()
    trade_data = {
        "symbol": symbol,
        "entry_price": entry_price,
        "targets": targets,
        "stop_loss": stop_loss,
        "indicators": indicators,
        **kwargs  # يدعم حقولاً مخصصة مثل partial_taken
    }
    trades.append(trade_data)
    with open(TRADES_FILE, 'w') as f:
        json.dump(trades, f, indent=4)
    logger.info(f"💾 تم تحديث صفقة {symbol}")
