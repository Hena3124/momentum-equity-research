from data import download_prices
from backtest import run_backtest, compute_metrics
from signals import compute_momentum, compute_mean_reversion


if __name__ == "__main__":
    print("loading data...")
    prices = download_prices()

    print("running momentum backtest...")
    mom_net, mom_gross = run_backtest(prices, lookback=252, skip=21, signal_func=compute_momentum)
    mom_net_metrics, _ = compute_metrics(mom_net)
    mom_gross_metrics, _ = compute_metrics(mom_gross)

    print("running mean-reversion backtest...")
    mr_net, mr_gross = run_backtest(prices, lookback=21, skip=0, signal_func=compute_mean_reversion)
    mr_net_metrics, _ = compute_metrics(mr_net)
    mr_gross_metrics, _ = compute_metrics(mr_gross)

    # this table is the key diagnostic: comparing gross vs net tells us
    # whether a weak/negative net Sharpe is because the signal itself is
    # weak, or because transaction costs are eating a real signal alive
    print("\n{:<22} {:>10} {:>10} {:>16} {:>16}".format(
        "metric", "mom net", "mom gross", "mr net", "mr gross"))
    print("-" * 78)
    for k in mom_net_metrics:
        print("{:<22} {:>10} {:>10} {:>16} {:>16}".format(
            k, mom_net_metrics[k], mom_gross_metrics[k],
            mr_net_metrics[k], mr_gross_metrics[k]))