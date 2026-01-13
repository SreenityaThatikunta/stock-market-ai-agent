def explain_event(stock, pct_change, volume_spike, news):
    explanation = f"{stock} moved {pct_change:.2f}% in a short period."

    if volume_spike:
        explanation += " Trading volume was unusually high."

    if news:
        explanation += f" Possible reason: {news[0]}."
    else:
        explanation += " No major related news detected."

    explanation += " This may indicate institutional activity or market reaction."

    return explanation