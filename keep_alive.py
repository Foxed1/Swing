# keep_alive.py

from flask import Flask
from threading import Thread
import requests
import time

app = Flask('')

@app.route('/')
def home():
    return "I'm alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    # تشغيل السيرفر
    t = Thread(target=run)
    t.start()

    # تفعيل Self-Ping كل 5 دقائق
    def ping_self():
        while True:
            try:
                url = "https://swing-f0ee.onrender.com/"
                requests.get(url)
                print("✅ Self-ping sent to keep alive.")
            except Exception as e:
                print(f"❌ Error in self-ping: {e}")
            time.sleep(300)  # كل 5 دقائق (300 ثانية)

    ping_thread = Thread(target=ping_self)
    ping_thread.start()
