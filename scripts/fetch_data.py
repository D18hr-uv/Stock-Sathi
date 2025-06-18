import yfinance as yf
import pandas as pd

def fetch_stock_data(symbol: str, interval: str, period: str) -> pd.DataFrame:
    """
    Fetches historical stock data using yfinance.
    """
    ticker = yf.Ticker(symbol)
    df = ticker.history(interval=interval, period=period)
    df.reset_index(inplace=True)
    return df

def save_to_csv(df: pd.DataFrame, path: str):
    df.to_csv(path, index=False)

# Example usage
if __name__ == "__main__":
    symbol = "AAPL"
    interval = "1m"
    period = "1d"
    data = fetch_stock_data(symbol, interval, period)
    save_to_csv(data, "../data/stock_data.csv")
