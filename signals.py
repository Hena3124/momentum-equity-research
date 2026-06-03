import pandas as pd
import numpy as np


def compute_momentum(prices, lookback=252, skip=21):
    # lookback = 252 trading days = roughly 12 months
    # skip = 21 trading days = roughly 1 month
    

    # return from 12 months ago to 1 month ago
    past_return = prices.shift(skip) / prices.shift(lookback) - 1

 



    ranks = past_return.rank(axis=1, pct=True)

    return past_return, ranks


def get_long_short(ranks, top_n=5, bottom_n=5):
    # each day, pick the top 5 stocks (long) and bottom 5 (short)
    # Since in a real fund the short side means thata you borrow and sell them
    # here we're just tracking what the signal would say here

    long_stocks  = ranks.apply(lambda row: row.nlargest(top_n).index.tolist(), axis=1)
    short_stocks = ranks.apply(lambda row: row.nsmallest(bottom_n).index.tolist(), axis=1)

    return long_stocks, short_stocks


if __name__ == "__main__":
    from data import download_prices

    prices = download_prices()

    past_return, ranks = compute_momentum(prices)

    # drop SPY and QQQ from the signal

    stock_columns = [c for c in prices.columns if c not in ["SPY", "QQQ"]]
    stock_ranks = ranks[stock_columns]

    long_stocks, short_stocks = get_long_short(stock_ranks)

    # show what the signal looks like on the most recent day
    latest = prices.index[-1]
    print(f"\n momentum signal as of {latest.date()}")


    
    print(f"\ntop 5 (long):  {long_stocks.iloc[-1]}")


    print(f"bottom 5 (short): {short_stocks.iloc[-1]}")

    print("\n12-month returns for all stocks (most recent)")


    latest_returns = past_return[stock_columns].iloc[-1].sort_values(ascending=False)
    print(latest_returns.round(3).to_string())