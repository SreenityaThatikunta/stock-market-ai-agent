import yfinance as yf

def fetch_stock_data(symbol, interval="5m", period="1d"):
    stock = yf.Ticker(symbol)
    df = stock.history(period=period, interval=interval)
    return df