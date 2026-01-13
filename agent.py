import time
import os
from datetime import datetime
import json
from config import (
    STOCK_SYMBOL,
    STOCK_NAME,
    PRICE_CHANGE_THRESHOLD,
    VOLUME_SPIKE_FACTOR,
    CHECK_INTERVAL_SECONDS
)

from fetcher import fetch_stock_data
from signals import detect_price_change, detect_volume_spike
from news_fetcher import fetch_news
from reasoning import explain_event
from notifier import notify


def run_agent():
    print("📊 Indian Market AI Agent started")
    print(f"Monitoring: {STOCK_NAME} ({STOCK_SYMBOL})")
    print("-" * 50)

    while True:
        try:
            df = fetch_stock_data(STOCK_SYMBOL)

            if df.empty:
                print("⚠️ No data received")
                time.sleep(CHECK_INTERVAL_SECONDS)
                continue

            current_price = df["Close"].iloc[-1]

            price_signal, pct = detect_price_change(
                df, PRICE_CHANGE_THRESHOLD
            )
            volume_signal = detect_volume_spike(
                df, VOLUME_SPIKE_FACTOR
            )

            # ✅ HEARTBEAT (always prints)
            print(
                f"⏱️ Checked | Price: ₹{current_price:.2f} | "
                f"Δ: {pct:.2f}% | "
                f"Volume spike: {volume_signal}"
            )

            # 🚨 ALERT CONDITION
            if price_signal or volume_signal:
                news = fetch_news(STOCK_NAME)
                explanation = explain_event(
                    STOCK_NAME,
                    pct,
                    volume_signal,
                    news
                )

                message = (
                    f"🚨 {STOCK_NAME} ALERT\n"
                    f"📉 Price Change: {pct:.2f}%\n"
                    f"📊 Volume Spike: {volume_signal}\n"
                    f"🧠 {explanation}"
                )

                notify(message)

                write_widget_data(
                    STOCK_NAME,
                    current_price,
                    explanation
                )
            else:
                # No alert - show current stock status
                write_widget_data(
                    STOCK_NAME,
                    current_price,
                    f"All steady! Δ {pct:+.2f}%"
                )

            time.sleep(CHECK_INTERVAL_SECONDS)

        except Exception as e:
            print("❌ Error:", e)
            time.sleep(60)

# Use absolute path based on script location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WIDGET_FILE = os.path.join(SCRIPT_DIR, "widget_data.json")

def write_widget_data(stock, price, message):
    data = {
        "stock": stock,
        "price": round(price, 2),
        "message": message,
        "time": datetime.now().strftime("%H:%M:%S")
    }
    with open(WIDGET_FILE, "w") as f:
        json.dump(data, f)

if __name__ == "__main__":
    run_agent()