# -*- coding: utf-8 -*-

# إعدادات Telegram
TELEGRAM_TOKEN = "7856358847:AAE3t_G9S5UXO1_I88uo1d88jMW7NRhQMx4"
CHAT_ID = "-1002667517368"

# قائمة العملات
SYMBOLS = [
    "BTCUSDT", "ETHUSDT", "SOLUSDT", "AVAXUSDT", "INJUSDT", 
    "LINKUSDT", "NEARUSDT", "ARBUSDT", "ADAUSDT", "ATOMUSDT",
    "DOTUSDT", "OPUSDT", "SUIUSDT", "APTUSDT", "MATICUSDT",
    "TIAUSDT", "PYTHUSDT", "PEPEUSDT", "DOGEUSDT", "SHIBUSDT",
    "RUNEUSDT", "FETUSDT", "RNDRUSDT", "JASMYUSDT", "1000SATSUSDT",
    "STXUSDT", "BLURUSDT", "DYDXUSDT", "GALAUSDT", "LTCUSDT",
    "TRXUSDT", "AAVEUSDT", "ARDRUSDT", "PAXGUSDT", "SEIUSDT",
    "COTIUSDT", "LDOUSDT", "CFXUSDT", "WIFUSDT", "BICOUSDT",
    "IDUSDT", "CVCUSDT", "AGIXUSDT", "NKNUSDT", "OCEANUSDT",
    "HIGHUSDT", "MAGICUSDT", "HOOKUSDT", "VELODROMEUSDT"
]

# إعدادات الوقت
TIMEFRAME = "4h"  # الإطار الزمني للتحليل (1h, 4h, 1d)
ROUND_TIME_MINUTES = 240  # فترة المسح (بالدقائق)
FOLLOW_UP_MINUTES = 30   # متابعة الصفقات كل 30 دقيقة

# إعدادات إدارة المخاطرة
RISK_PERCENT = 1.5  # نسبة المخاطرة من رأس المال لكل صفقة (1.5%)
MIN_VOLUME = 2000000  # الحد الأدنى لحجم التداول (2 مليون دولار)

# إعدادات المتوسطات المتحركة
MA_SETTINGS = {
    'fast_ma': 9,      # للمدى القصير (تحديد الدخول)
    'medium_ma': 21,   # للمدى المتوسط (تأكيد الاتجاه)
    'slow_ma': 50,     # دعم/مقاومة ديناميكي
    'trend_ma': 200    # تحديد الاتجاه العام
}

# إعدادات Pivot
PIVOT_DAYS = 3  # عدد الأيام لحساب مستويات Pivot

# إعدادات الذكاء الاصطناعي (معطلة حالياً)
AI_ENABLED = False  # تفعيل/تعطيل نماذج الذكاء الاصطناعي

# إعدادات API (اختيارية)
BINANCE_API_KEY = ""  # اتركه فارغاً إذا لا تريد استخدام API مباشر
BINANCE_API_SECRET = ""

# إعدادات التحليل الفني المتقدم
TECHNICAL_SETTINGS = {
    'rsi_overbought': 70,
    'rsi_oversold': 30,
    'adx_threshold': 25,  # الحد الأدنى لقوة الاتجاه
    'volume_spike': 1.5   # مضاعفة حجم التداول عن المتوسط
}

# إعدادات الرسوم البيانية (للتطوير المستقبلي)
CHART_SETTINGS = {
    'enable': False,
    'style': 'candlestick',
    'indicators': ['MA', 'MACD', 'Volume']
}
