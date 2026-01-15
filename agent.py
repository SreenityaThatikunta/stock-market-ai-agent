import time
import os
from datetime import datetime
import json
from config import (
    STOCK_SYMBOL,
    STOCK_NAME,
    PRICE_CHANGE_THRESHOLD,
    VOLUME_SPIKE_FACTOR,
    CHECK_INTERVAL_SECONDS,
    ALERT_COOLDOWN_SECONDS
)

from fetcher import fetch_stock_data
from signals import detect_price_change, detect_volume_spike
from news_fetcher import fetch_news
from reasoning import explain_event
from notifier import notify
from pathlib import Path

# Shared data directory
DATA_DIR = Path.home() / ".market-widget"
DATA_DIR.mkdir(exist_ok=True)

WIDGET_FILE = DATA_DIR / "widget_data.json"
SELECTED_STOCK_FILE = DATA_DIR / "selected_stock.json"


def get_selected_stock():
    """Read the user's stock selection from JSON file."""
    if os.path.exists(SELECTED_STOCK_FILE):
        try:
            with open(SELECTED_STOCK_FILE) as f:
                data = json.load(f)
                name = data.get("name")
                symbol = data.get("symbol")
                if name and symbol:
                    return name, symbol
        except Exception as e:
            print(f"[DEBUG] Error reading selected stock: {e}")

    # Fall back to config defaults
    return STOCK_NAME, STOCK_SYMBOL


def write_widget_data(stock, price, message):
    data = {
        "stock": stock,
        "price": round(price, 2),
        "message": message,
        "time": datetime.now().strftime("%H:%M:%S")
    }
    with open(WIDGET_FILE, "w") as f:
        json.dump(data, f)


def run_agent():
    print("📊 Indian Market AI Agent started")
    print("-" * 50)

    current_stock_name = None
    current_stock_symbol = None
    last_alert_time = 0  # Track last Telegram alert time

    while True:
        try:
            # Check for stock selection changes
            stock_name, stock_symbol = get_selected_stock()

            # Detect stock change
            if stock_name != current_stock_name:
                if current_stock_name is not None:
                    print(f"🔄 Switching to: {stock_name} ({stock_symbol})")
                else:
                    print(f"📈 Monitoring: {stock_name} ({stock_symbol})")
                current_stock_name = stock_name
                current_stock_symbol = stock_symbol

            df = fetch_stock_data(current_stock_symbol)

            if df.empty:
                print("⚠️ No data received")
                write_widget_data(
                    current_stock_name,
                    0,
                    "Waiting for market data..."
                )
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
                news = fetch_news(current_stock_name)
                explanation = explain_event(
                    current_stock_name,
                    pct,
                    volume_signal,
                    news
                )

                # Always update widget immediately
                write_widget_data(
                    current_stock_name,
                    current_price,
                    explanation
                )

                # Only send Telegram if cooldown has passed
                now = time.time()
                if now - last_alert_time >= ALERT_COOLDOWN_SECONDS:
                    message = (
                        f"🚨 {current_stock_name} ALERT\n"
                        f"📉 Price Change: {pct:.2f}%\n"
                        f"📊 Volume Spike: {volume_signal}\n"
                        f"🧠 {explanation}"
                    )
                    notify(message)
                    last_alert_time = now
                else:
                    remaining = int(ALERT_COOLDOWN_SECONDS - (now - last_alert_time))
                    print(f"⏳ Alert suppressed (cooldown: {remaining}s remaining)")
            else:
                # No alert - show current stock status
                write_widget_data(
                    current_stock_name,
                    current_price,
                    f"All steady! Δ {pct:+.2f}%"
                )

            time.sleep(CHECK_INTERVAL_SECONDS)

        except Exception as e:
            print("❌ Error:", e)
            time.sleep(60)


if __name__ == "__main__":
    run_agent()
