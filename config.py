import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Telegram credentials (from .env)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# Zerodha credentials (from .env, optional)
# ZERODHA_API_KEY = os.getenv("ZERODHA_API_KEY", "")
# ZERODHA_ACCESS_TOKEN = os.getenv("ZERODHA_ACCESS_TOKEN", "")

# Stock configuration
STOCK_SYMBOL = "INFY.NS"      # Yahoo Finance symbol (default)
STOCK_NAME = "INFOSYS"        # Default stock name

# Detection thresholds
PRICE_CHANGE_THRESHOLD = 1.5   # percent
VOLUME_SPIKE_FACTOR = 2.0

# Agent settings
CHECK_INTERVAL_SECONDS = 5       # Widget updates (keep low for responsiveness)
ALERT_COOLDOWN_SECONDS = 300     # Minimum time between Telegram alerts (5 minutes)

# Telegram (optional)
USE_TELEGRAM = True
