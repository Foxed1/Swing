import numpy as np
import logging

logger = logging.getLogger(__name__)

def calculate_moving_averages(data):
    if not data or 'close' not in data:
        logger.error("❌ بيانات غير صالحة لحساب المتوسطات")
        return {
            'ma9': 0,
            'ma21': 0,
            'ma50': 0,
            'ma200': 0,
            'trend': 'غير محدد',
            'signal': 'انتظار'
        }
    
    try:
        closes = np.array(data['close'])
        ma_values = {
            'ma9': np.mean(closes[-9:]),
            'ma21': np.mean(closes[-21:]),
            'ma50': np.mean(closes[-50:]),
            'ma200': np.mean(closes[-200:])
        }
        
        golden_cross = ma_values['ma9'] > ma_values['ma21'] > ma_values['ma50']
        death_cross = ma_values['ma9'] < ma_values['ma21'] < ma_values['ma50']
        
        return {
            **ma_values,
            'trend': 'صاعد' if golden_cross else 'هابط' if death_cross else 'جانبي',
            'signal': 'شراء' if golden_cross and data['price'] > ma_values['ma200'] else 'بيع'
        }
    except Exception as e:
        logger.error(f"❌ فشل حساب المتوسطات: {e}")
        return {
            'ma9': 0,
            'ma21': 0,
            'ma50': 0,
            'ma200': 0,
            'trend': 'خطأ',
            'signal': 'انتظار'
        }
