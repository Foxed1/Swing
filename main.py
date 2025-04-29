# main.py

import time
import schedule
from config import SYMBOLS, ROUND_TIME_MINUTES, FOLLOW_UP_MINUTES
from analyzer import analyze_symbol
from signals import check_entry_conditions, build_trade_message
from telegram_bot import send_message
from trades_manager import save_trade, load_trades, remove_trade
from keep_alive import keep_alive

def run_analysis():
    open_symbols = [t["symbol"] for t in load_trades()]
    for symbol in SYMBOLS:
        if symbol in open_symbols:
            print(f"⏩ تم تخطي {symbol} لأن فيه صفقة مفتوحة بالفعل.")
            continue
        print(f"Analyzing {symbol}...")
        data = analyze_symbol(symbol)
        if check_entry_conditions(data):
            price = data["price"]
            target_price = round(price * 1.05, 4)
            stop_price = round(price * 0.97, 4)
            save_trade(symbol, price, target_price, stop_price)
            message = build_trade_message(symbol, data, price, target_price, stop_price)
            send_message(message)
        time.sleep(1)

def follow_up_trades():
    trades = load_trades()
    for trade in trades:
        symbol = trade["symbol"]
        data = analyze_symbol(symbol)
        if not data:
            continue
        price = data["price"]
        if price >= trade["target_price"]:
            send_message(f"✅ الصفقة على {symbol} وصلت للهدف!")
            remove_trade(symbol)
        elif price <= trade["stop_price"]:
            send_message(f"❌ الصفقة على {symbol} ضربت الستوب!")
            remove_trade(symbol)
        time.sleep(1)

keep_alive()

schedule.every(ROUND_TIME_MINUTES).minutes.do(run_analysis)
schedule.every(FOLLOW_UP_MINUTES).minutes.do(follow_up_trades)

if __name__ == "__main__":
    print("✅ البوت Swing_Bot_v2 Final_v2 يعمل الآن...")
    run_analysis()
    while True:
        schedule.run_pending()
        time.sleep(1)
