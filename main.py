import time
import schedule
import threading
from datetime import datetime
from config import SYMBOLS
from analyzer import analyze_symbol
from signals import check_entry_conditions, build_trade_message
from telegram_bot import send_message
from trades_manager import save_trade, load_trades, remove_trade, clean_old_trades
from keep_alive import keep_alive

def run_analysis():
    print(f"🚀 بدء جولة تحليل العملات في {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    trades = load_trades()
    trades = clean_old_trades(trades)
    open_symbols = [t["symbol"] for t in trades]

    for symbol in SYMBOLS:
        if symbol in open_symbols:
            print(f"⏩ تم تخطي {symbol} لأن فيه صفقة مفتوحة بالفعل.")
            continue

        print(f"🔎 Analyzing {symbol}...")
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
    print(f"🔄 متابعة الصفقات المفتوحة في {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    trades = load_trades()
    for trade in trades:
        symbol = trade['symbol']
        entry_price = trade['entry_price']
        target_price = trade['target_price']
        stop_price = trade['stop_price']

        # نجيب السعر الحالي
        data = analyze_symbol(symbol)
        current_price = data["price"]

        if current_price >= target_price:
            print(f"✅ تم تحقيق الهدف في صفقة {symbol}! السعر الحالي: {current_price}")
            send_message(f"✅ صفقة {symbol} وصلت الهدف! السعر الحالي: {current_price}")
            remove_trade(symbol)
        elif current_price <= stop_price:
            print(f"❌ تم ضرب وقف الخسارة في صفقة {symbol}. السعر الحالي: {current_price}")
            send_message(f"❌ صفقة {symbol} ضربت الستوب! السعر الحالي: {current_price}")
            remove_trade(symbol)
        else:
            print(f"⏳ صفقة {symbol} مازالت مفتوحة. السعر الحالي: {current_price}")

def print_alive_message():
    print(f"✅ البوت لا يزال يعمل... ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

def start_scheduler():
    scheduler_thread = threading.Thread(target=run_schedule)
    scheduler_thread.daemon = True
    scheduler_thread.start()

# بدء سيرفر الويب
keep_alive()

# جدولة المهام
schedule.every(4).hours.do(run_analysis)            # كل 4 ساعات تحليل عملات
schedule.every(2).hours.do(follow_up_trades)         # كل ساعتين متابعة الصفقات
schedule.every(5).minutes.do(print_alive_message)    # كل 5 دقائق Alive

# بدء الجدولة
start_scheduler()

print("✅ البوت بدأ العمل الآن!")

# لوب رئيسي بسيط للحفاظ على حياة البرنامج
while True:
    time.sleep(10)
