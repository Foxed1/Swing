import time
import schedule
from datetime import datetime
from config import SYMBOLS, ROUND_TIME_MINUTES, FOLLOW_UP_MINUTES
from analyzer import analyze_symbol
from signals import check_entry_conditions, build_trade_message
from telegram_bot import send_message
from trades_manager import save_trade, load_trades, remove_trade, save_all_trades, clean_old_trades
from keep_alive import keep_alive

def run_analysis():
    # تنظيف الصفقات القديمة قبل التحليل
    trades = load_trades()
    trades = clean_old_trades(trades)
    save_all_trades(trades)

    open_symbols = [t["symbol"] for t in trades]
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
        # المتابعة البسيطة للصفقات المفتوحة
        pass

def print_alive_message():
    print(f"✅ Bot is alive at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

keep_alive()

# جدول التحليلات والجولات
schedule.every(ROUND_TIME_MINUTES).minutes.do(run_analysis)
schedule.every(FOLLOW_UP_MINUTES).minutes.do(follow_up_trades)

# طباعة نشاط دوري كل 5 دقائق
schedule.every(5).minutes.do(print_alive_message)

print("✅ البوت بدأ العمل الآن!")

while True:
    schedule.run_pending()
    time.sleep(1)
