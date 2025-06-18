def check_price_alert(df, threshold=5):
    """
    Compares latest and opening price to determine if alert should be triggered.
    """
    if df.empty:
        return None
    open_price = df['Open'].iloc[0]
    latest_price = df['Close'].iloc[-1]
    change = ((latest_price - open_price) / open_price) * 100

    if abs(change) >= threshold:
        return f"⚠️ ALERT: Price changed by {change:.2f}%"
    return f"✅ Stable: Change is {change:.2f}%"
