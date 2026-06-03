import pandas as pd
import numpy as np
from data import download_prices
from signals import compute_momentum


def run_backtest(prices, lookback=252, skip=21, top_n=5, bottom_n=5):

    
    stock_cols = [c for c in prices.columns if c not in ["SPY", "QQQ"]]
    stocks = prices[stock_cols]

    # compute momentum signal
    past_return, ranks = compute_momentum(stocks, lookback, skip)

    # forward returns - what actually happens AFTER we place the trade
    # shift(-1) means "next day's return" - this is what we earn
    # this is the key look-ahead bias fix - we use tomorrow's return,
    # not today's, because we can only trade after the signal is ready
    daily_returns = stocks.pct_change(fill_method=None)
    forward_returns = daily_returns.shift(-1)

    # we rebalance monthly - every 21 trading days
    # on each rebalance day, build a long/short portfolio
    portfolio_returns = []
    dates = []

    rebal_days = range(lookback, len(stocks) - 1, 21)

    for i in rebal_days:
        date = stocks.index[i]

        # ranks on THIS day - no future data used
        todays_ranks = ranks.iloc[i]

        # skip if too many NaNs (not enough history yet)
        if todays_ranks.isna().sum() > len(stock_cols) * 0.3:
            continue

        todays_ranks = todays_ranks.dropna()

        # pick top and bottom stocks
        long_stocks  = todays_ranks.nlargest(top_n).index.tolist()
        short_stocks = todays_ranks.nsmallest(bottom_n).index.tolist()

        # get the next 21 days of returns for these stocks
        # this is what we'd earn holding this portfolio for a month
        next_period = forward_returns.iloc[i:i+21]

        long_ret  = next_period[long_stocks].mean(axis=1).mean()
        short_ret = next_period[short_stocks].mean(axis=1).mean()

        # long-short return: profit from longs, subtract losses from shorts
        # if our longs go up 3% and shorts go down 2%, we make 5%
        ls_return = long_ret - short_ret

        portfolio_returns.append(ls_return)
        dates.append(date)

    results = pd.Series(portfolio_returns, index=dates, name="monthly_return")
    return results


def compute_metrics(returns):
    

    total_return = (1 + returns).prod() - 1

    #  we have monthly returns so multiply by 12
    ann_return = returns.mean() * 12

    #    how much do returns bounce around
    ann_vol = returns.std() * np.sqrt(12)

    # sharpe ratio - return per unit of risk
    # higher is better. above 0.5 is decent, above 1.0 is good


    # using 0 as risk free rate to keep it simple
    sharpe = ann_return / ann_vol if ann_vol > 0 else 0

    # max drawdown - worst peak to trough loss
    # this tells you the worst case if you had bad timing

    cumulative = (1 + returns).cumprod()
    rolling_max = cumulative.cummax()
    drawdown = (cumulative - rolling_max) / rolling_max



    max_dd = drawdown.min()

    # hit rate - what % of months were profitable
    hit_rate = (returns > 0).mean()

    metrics = {
        "total return":       f"{total_return:.1%}",
        "annualised return":  f"{ann_return:.1%}",
        "annualised vol":     f"{ann_vol:.1%}",
        "sharpe ratio":       f"{sharpe:.2f}",
        "max drawdown":       f"{max_dd:.1%}",
        "hit rate":           f"{hit_rate:.1%}",
    }

    return metrics, cumulative


if __name__ == "__main__":
    print("loading data........")
    prices = download_prices()

    print("running backtest...")

    returns = run_backtest(prices)

    print(f"\nbacktest ran for {len(returns)} monthly periods")
    print(f"date range: {returns.index[0].date()} to {returns.index[-1].date()}")



    metrics, cumulative = compute_metrics(returns)

    print("\nstrategy performance")
    for k, v in metrics.items():

        print(f"  {k:<22} {v}")

    print("\n monthly returns (last 6) ")



    print(returns.tail(6).round(4).to_string())