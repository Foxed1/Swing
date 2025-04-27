# utils.py

def determine_trend_strength(adx_value):
    if adx_value > 25:
        return "قوي"
    elif 20 <= adx_value <= 25:
        return "متوسط"
    else:
        return "ضعيف"
