# main.py
import time
import schedule
from config import *
from analyzer import analyze_symbol
from signals import check_entry_conditions, build_trade_message
from telegram_bot import send_message
from trades_manager import save_trade, load_trades, remove_trade
from keep_alive import keep_alive

def run_analysis():
    open_trades = {t["symbol"]: t for t in load_trades()}
    
    for symbol in SYMBOLS:
        if symbol in open_trades:
            continue
            
        data = analyze_symbol(symbol)
        if not data:
            continue
            
        if check_entry_conditions(data, symbol):
            entry_price = data["price"]
            targets = [
                round(entry_price * 1.02, 4),  # هدف 1: +2%
                round(entry_price * 1.04, 4)   # هدف 2: +4%
            ]
            stop_loss = round(entry_price * 0.98, 4)  # وقف -2%
            
            save_trade(symbol, entry_price, targets, stop_loss)
            message = build_trade_message(symbol, data, entry_price, targets)
            send_message(message)
        time.sleep(1)

def follow_up_trades():
    for trade in load_trades():
        data = analyze_symbol(trade["symbol"])
        if not data:
            continue
            
        current_price = data["price"]
        symbol = trade["symbol"]
        
        # جني الأرباح على مراحل
        if current_price >= trade["targets"][1]:
            send_message(f"🎯 {symbol} - إغلاق كامل عند {current_price:.4f}")
            remove_trade(symbol)
        elif current_price >= trade["targets"][0] and not trade.get("partial_taken"):
            send_message(f"✅ {symbol} - جني 50% أرباح عند {current_price:.4f}")
            trade["partial_taken"] = True
            save_trade(symbol, trade["entry_price"], trade["targets"], trade["stop_loss"])
        elif current_price <= trade["stop_loss"]:
            send_message(f"❌ {symbol} - إيقاف خسارة عند {current_price:.4f}")
            remove_trade(symbol)
        time.sleep(1)

if __name__ == "__main__":
    keep_alive()
    print("🟢 البوت يعمل بنموذج ذكي لكل عملة!")
    
    # تشغيل مباشر بدون تأخير أولي
    run_analysis()
    follow_up_trades()
    
    schedule.every(ROUND_TIME_MINUTES).minutes.do(run_analysis)
    schedule.every(FOLLOW_UP_MINUTES).minutes.do(follow_up_trades)
    
    while True:
        schedule.run_pending()
        time.sleep(1)
