import feedparser
from urllib.parse import quote

def fetch_news(stock_name):
    # URL-encode the stock name to handle spaces and special characters
    encoded_name = quote(stock_name)
    url = f"https://news.google.com/rss/search?q={encoded_name}+stock+india"
    feed = feedparser.parse(url)
    return [entry.title for entry in feed.entries[:3]]