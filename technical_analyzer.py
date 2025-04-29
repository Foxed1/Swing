import numpy as np
import logging

logger = logging.getLogger(__name__)

def calculate_moving_averages(data):
    """حساب المتوسطات المتحركة مع معالجة الأخطاء"""
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
            'signal': 'شراء' if golden_cross and closes[-1] > ma_values['ma200'] else 'بيع'
        }
    except Exception as e:
        logger.error(f"❌ فشل حساب المتوسطات: {e}")
        return None
