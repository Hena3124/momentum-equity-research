import pandas as pd
import yfinance as yf
import os

# pulling the real S&P 500 list instead of hand-picking stocks
# this was the biggest limitation from before - 20 stocks isn't enough
# breadth for the signal to mean much

def get_sp500_tickers():
    cache_path = "data/sp500_tickers.csv"

    if os.path.exists(cache_path):
        return pd.read_csv(cache_path)["Symbol"].tolist()

    print("fetching S&P 500 list from wikipedia...")
    tables = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    sp500 = tables[0]

    # yfinance wants BRK-B not BRK.B
    tickers = sp500["Symbol"].str.replace(".", "-", regex=False).tolist()

    os.makedirs("data", exist_ok=True)
    pd.DataFrame({"Symbol": tickers}).to_csv(cache_path, index=False)
    print(f"found {len(tickers)} tickers, cached")
    return tickers


BENCHMARKS = ["SPY", "QQQ"]

START = "2019-01-01"
END   = "2024-12-31"

def download_prices():
    # checking if we already downloaded it so we don't hit the API every time
    if os.path.exists("data/prices.csv"):
        print("loading from cache...")


        return pd.read_csv("data/prices.csv", index_col=0, parse_dates=True)

    tickers = get_sp500_tickers() + BENCHMARKS
    print(f"downloading {len(tickers)} tickers from {START} to {END}")

    # yfinance chokes if you throw 500 tickers at it in one call sometimes,
    # so pulling it in batches of 100 and sticking them back together
    chunks = [tickers[i:i + 100] for i in range(0, len(tickers), 100)]
    all_prices = []

    for i, chunk in enumerate(chunks):
        print(f"  batch {i+1}/{len(chunks)}...")
        raw = yf.download(chunk, start=START, end=END, auto_adjust=True, progress=False)
        all_prices.append(raw["Close"])

    prices = pd.concat(all_prices, axis=1)

    # drop tickers that came back totally empty (bad symbol, delisted, etc.)
    prices = prices.dropna(axis=1, how="all")

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