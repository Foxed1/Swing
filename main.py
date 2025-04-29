import time
import schedule
import logging
import os
from config import *
from analyzer import analyze_symbol
from signals import check_entry_conditions, build_trade_message
from telegram_bot import send_message
from trades_manager import save_trade, load_trades, remove_trade
from keep_alive import keep_alive

# إعدادات التسجيل
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/bot_logs.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def run_analysis():
    logger.info("🔍 بدء جولة تحليل جديدة...")
    open_trades = {t["symbol"]: t for t in load_trades()}
    
    for symbol in SYMBOLS:
        try:
            if symbol in open_trades:
                logger.debug(f"⏩ تخطي {symbol} (صفقة مفتوحة بالفعل)")
                continue
                
            data = analyze_symbol(symbol)
            if not data:
                logger.warning(f"⚠️ لا يوجد بيانات لـ {symbol}")
                continue
                
            if check_entry_conditions(data, symbol):
                entry_price = data["price"]
                targets = {
                    "take_profit": [entry_price * 1.02, entry_price * 1.04],
                    "stop_loss": entry_price * 0.98
                }
                save_trade(
                    symbol=symbol,
                    entry_price=entry_price,
                    targets=targets,
                    stop_loss=targets["stop_loss"],
                    indicators=data
                )
                message = build_trade_message(symbol, data, entry_price, targets)
                send_message(message)
                logger.info(f"✅ إشارة دخول لـ {symbol}")
                
        except Exception as e:
            logger.error(f"🔥 خطأ في تحليل {symbol}: {e}", exc_info=True)
        time.sleep(1)

def follow_up_trades():
    logger.info("🔄 متابعة الصفقات المفتوحة...")
    for trade in load_trades():
        try:
            data = analyze_symbol(trade["symbol"])
            if not data:
                logger.warning(f"⚠️ لا يوجد بيانات لـ {trade['symbol']}")
                continue
                
            current_price = data["price"]
            symbol = trade["symbol"]
            
            if current_price >= trade["targets"]["take_profit"][1]:
                send_message(f"🎯 {symbol} - إغلاق كامل عند {current_price:.4f}")
                remove_trade(symbol)
                logger.info(f"🔄 {symbol} - إغلاق (وصول للهدف الثاني)")
            elif current_price >= trade["targets"]["take_profit"][0] and not trade.get("partial_taken"):
                send_message(f"✅ {symbol} - جني 50% أرباح عند {current_price:.4f}")
                trade["partial_taken"] = True
                save_trade(**trade)
                logger.info(f"🔄 {symbol} - جني 50% أرباح")
            elif current_price <= trade["stop_loss"]:
                send_message(f"❌ {symbol} - إيقاف خسارة عند {current_price:.4f}")
                remove_trade(symbol)
                logger.info(f"🔄 {symbol} - إغلاق (إيقاف خسارة)")
                
        except Exception as e:
            logger.error(f"🔥 خطأ في متابعة {trade['symbol']}: {e}", exc_info=True)
        time.sleep(1)

if __name__ == "__main__":
    keep_alive()
    logger.info("🟢 بدء تشغيل البوت بنجاح!")
    
    # التشغيل الأولي
    run_analysis()
    follow_up_trades()
    
    # الجدولة
    schedule.every(ROUND_TIME_MINUTES).minutes.do(run_analysis)
    schedule.every(FOLLOW_UP_MINUTES).minutes.do(follow_up_trades)
    
    while True:
        schedule.run_pending()
        time.sleep(1)
