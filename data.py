import pandas as pd
import yfinance as yf
import os

# these are 20 large S&P 500 stocks across different sectors

TICKERS = [
    "AAPL", "MSFT", "GOOGL", "NVDA", "META",    # tech
    "JPM", "GS", "BAC",                         # financials
    "JNJ", "PFE",                               # healthcare
    "XOM", "CVX",                               # energy
    "HD", "MCD", "NKE",                         # consumer
    "BA", "CAT", "HON",                         # industrials
    "SPY", "QQQ"                                # benchmarks
]

START = "2019-01-01"
END   = "2024-12-31"

def download_prices():
    # checking if we already downloaded it so we don't hit the API every time
    if os.path.exists("data/prices.csv"):
        print("loading from cache...")


        return pd.read_csv("data/prices.csv", index_col=0, parse_dates=True)

    print(f"downloading {len(TICKERS)} tickers from {START} to {END}")

    raw = yf.download(TICKERS, start=START, end=END, auto_adjust=True, progress=False)
    prices = raw["Close"]

    # some stocks have occasional missing days (holidays, halts)


    # forward fill handles it, just carry the last known price forward
    prices = prices.ffill()

    os.makedirs("data", exist_ok=True)
    prices.to_csv("data/prices.csv")
    print(f"saved. shape: {prices.shape}")
    return prices


def compute_returns(prices):
    # daily return = (today's price - yesterday's price) / yesterday's price
    # pct_change() does exactly this for every stock at once


    return prices.pct_change(fill_method=None) #chnaged to silenece the warning


if __name__ == "__main__":
    prices = download_prices()

    returns = compute_returns(prices)

    print("\n prices (last 3 rows) ")
    print(prices.tail(3).round(2))

    print("\n daily returns (last 3 rows) ")
    print(returns.tail(3).round(4))

    print(f"\ntotal observations: {prices.shape[0] * prices.shape[1]:,}")