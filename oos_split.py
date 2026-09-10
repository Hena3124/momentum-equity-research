import pandas as pd
from data import download_prices
from backtest import run_backtest, compute_metrics
from signals import compute_momentum, compute_mean_reversion

# splitting point chosen up front, before looking at either sub-period's
# results - this is a fair time-based split, not something tuned after
# seeing which split makes the numbers look better
SPLIT_DATE = "2023-01-01"


def split_metrics(net, gross, split_date, label):
    net_in    = net[net.index < split_date]
    net_out   = net[net.index >= split_date]
    gross_in  = gross[gross.index < split_date]
    gross_out = gross[gross.index >= split_date]

    net_in_m, _    = compute_metrics(net_in)
    net_out_m, _   = compute_metrics(net_out)
    gross_in_m, _  = compute_metrics(gross_in)
    gross_out_m, _ = compute_metrics(gross_out)

    print(f"\n{label}")
    print(f"  in-sample:  {len(net_in)} periods  ({net_in.index[0].date()} to {net_in.index[-1].date()})")
    print(f"  out-sample: {len(net_out)} periods  ({net_out.index[0].date()} to {net_out.index[-1].date()})")
    print("\n  {:<22} {:>12} {:>12} {:>14} {:>14}".format(
        "metric", "net in", "net out", "gross in", "gross out"))
    print("  " + "-" * 74)
    for k in net_in_m:
        print("  {:<22} {:>12} {:>12} {:>14} {:>14}".format(
            k, net_in_m[k], net_out_m[k], gross_in_m[k], gross_out_m[k]))


if __name__ == "__main__":
    print("loading data...")
    prices = download_prices()

    print("running momentum backtest...")
    mom_net, mom_gross = run_backtest(prices, lookback=252, skip=21, signal_func=compute_momentum)
    split_metrics(mom_net, mom_gross, SPLIT_DATE,
                   "MOMENTUM: pre-2023 vs 2023+ (fixed split, not tuned)")

    print("running mean-reversion backtest...")
    mr_net, mr_gross = run_backtest(prices, lookback=21, skip=0, signal_func=compute_mean_reversion)
    split_metrics(mr_net, mr_gross, SPLIT_DATE,
                   "MEAN-REVERSION: pre-2023 vs 2023+ (fixed split, not tuned)")