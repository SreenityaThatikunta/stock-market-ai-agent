# Indian Market Agent

A lightweight stock monitoring agent with a desktop widget for tracking Indian market stocks.

## What it does

1. **Monitors stock prices** via Yahoo Finance (configurable interval)
2. **Detects anomalies** - price spikes and unusual volume
3. **Sends alerts** via Telegram when thresholds are breached
4. **Desktop widget** shows live stock status

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   fetcher   │────▶│    agent     │────▶│  notifier   │
│  (yfinance) │     │ (main loop)  │     │ (telegram)  │
└─────────────┘     └──────┬───────┘     └─────────────┘
                          │
                          ▼
                   ┌──────────────┐
                   │    widget    │
                   │  (tkinter)   │
                   └──────────────┘
```

**Files:**
- `agent.py` - Main monitoring loop
- `fetcher.py` - Stock data from Yahoo Finance
- `signals.py` - Price change & volume spike detection
- `reasoning.py` - Generates alert explanations
- `notifier.py` - Console + Telegram alerts
- `widget.py` - Desktop widget UI
- `widget_styles.py` - Widget styling config
- `config.py` - All settings (gitignored)

## Setup

1. **Install dependencies**
   ```bash
   pip install yfinance requests pillow
   ```

2. **Create config.py**
   ```python
   TELEGRAM_BOT_TOKEN = "your_bot_token"
   TELEGRAM_CHAT_ID = "your_chat_id"

   STOCK_SYMBOL = "INFY.NS"      # Yahoo Finance symbol
   STOCK_NAME = "INFOSYS"

   PRICE_CHANGE_THRESHOLD = 1.5  # percent
   VOLUME_SPIKE_FACTOR = 2.0
   CHECK_INTERVAL_SECONDS = 30

   USE_TELEGRAM = True
   ```

3. **Run the agent**
   ```bash
   python agent.py
   ```

4. **Run the widget** (separate terminal)
   ```bash
   python widget.py
   ```

## Configuration

| Setting | Description |
|---------|-------------|
| `STOCK_SYMBOL` | Yahoo Finance symbol (e.g., `RELIANCE.NS`, `TCS.NS`) |
| `PRICE_CHANGE_THRESHOLD` | % change to trigger alert |
| `VOLUME_SPIKE_FACTOR` | Volume multiplier to trigger alert |
| `CHECK_INTERVAL_SECONDS` | How often to check |

## Telegram Setup

1. Create a bot via [@BotFather](https://t.me/botfather)
2. Get your chat ID from [@userinfobot](https://t.me/userinfobot)
3. Add token and chat ID to `config.py`
