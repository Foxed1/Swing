# ai_predictor.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from binance.client import Client
import joblib
import os

MODELS_DIR = "ai_models"
os.makedirs(MODELS_DIR, exist_ok=True)

def compute_rsi(prices, window=14):
    deltas = np.diff(prices)
    up = np.where(deltas > 0, deltas, 0)
    down = np.where(deltas < 0, -deltas, 0)
    avg_gain = pd.Series(up).rolling(window).mean()
    avg_loss = pd.Series(down).rolling(window).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def train_model_for_symbol(symbol):
    client = Client()
    klines = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_4HOUR, "200 days ago UTC")
    data = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    
    data['close'] = pd.to_numeric(data['close'])
    data['volume'] = pd.to_numeric(data['volume'])
    
    # حساب المؤشرات
    data['ema_50'] = data['close'].ewm(span=50).mean()
    data['rsi'] = compute_rsi(data['close'].values)
    data['target'] = (data['close'].shift(-4) > data['close']).astype(int)
    
    data.dropna(inplace=True)
    model = RandomForestClassifier(n_estimators=150, random_state=42)
    model.fit(data[['ema_50', 'rsi']], data['target'])
    
    joblib.dump(model, f"{MODELS_DIR}/model_{symbol}.pkl")

def load_all_models(symbols):
    models = {}
    for symbol in symbols:
        model_path = f"{MODELS_DIR}/model_{symbol}.pkl"
        if os.path.exists(model_path):
            models[symbol] = joblib.load(model_path)
        else:
            print(f"⚠️ نموذج {symbol} غير موجود، جاري التدريب...")
            train_model_for_symbol(symbol)
            models[symbol] = joblib.load(model_path)
    return models
