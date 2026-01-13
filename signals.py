def detect_price_change(df, threshold):
    if len(df) < 6:
        return False, 0.0

    prev = df["Close"].iloc[-6]
    curr = df["Close"].iloc[-1]

    pct_change = (curr - prev) / prev * 100
    return abs(pct_change) >= threshold, pct_change


def detect_volume_spike(df, factor):
    if len(df) < 10:
        return False

    avg_volume = df["Volume"].iloc[:-1].mean()
    current_volume = df["Volume"].iloc[-1]

    return current_volume > factor * avg_volume