import feedparser

def fetch_news(stock_name):
    url = f"https://news.google.com/rss/search?q={stock_name}+stock+india"
    feed = feedparser.parse(url)
    return [entry.title for entry in feed.entries[:3]]