# Indian Market Agent

A lightweight stock monitoring agent with a desktop widget for tracking Indian market stocks.

## Features

- Real-time stock price monitoring via Yahoo Finance
- Price spike & volume anomaly detection
- Telegram alerts with AI-generated explanations
- Desktop widget (Electron) with stock selector

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   fetcher   │────▶│    agent     │────▶│  notifier   │
│  (yfinance) │     │ (main loop)  │     │ (telegram)  │
└─────────────┘     └──────┬───────┘     └─────────────┘
                           │
                           ▼
                     ┌──────────────┐
                     │   widget     │
                     │  (electron)  │
                     └──────────────┘
```

## Tech Stack

**Backend:** Python, yfinance, python-dotenv

**Widget:** Electron, HTML/CSS/JS

**Alerts:** Telegram Bot API

## Setup

1. **Clone & install Python deps**
   ```bash
   pip install yfinance requests python-dotenv
   ```

2. **Create `.env` file** (copy from `.env.example`)
   ```
   TELEGRAM_BOT_TOKEN=your_bot_token
   TELEGRAM_CHAT_ID=your_chat_id
   ```

3. **Install widget deps**
   ```bash
   cd market-widget && npm install
   ```

## Usage

```bash
# Terminal 1: Start the agent
python agent.py

# Terminal 2: Start the widget
cd market-widget && npm start
```
