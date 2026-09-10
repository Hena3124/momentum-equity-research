import numpy as np
from scipy import stats
from data import download_prices
from backtest import run_backtest
from signals import compute_momentum, compute_mean_reversion


def test_significance(returns, label=""):
    # one-sample t-test: is the mean monthly return distinguishable
    # from zero, or could this be noise given how few observations
    # we have? (60 monthly periods isn't a lot of data)

    n = len(returns)
    mean = returns.mean()
    std = returns.std(ddof=1)
    se = std / np.sqrt(n)
    t_stat = mean / se

    # two-tailed p-value using the t-distribution (not normal),
    # since n is small enough that the distinction matters
    p_value = 2 * (1 - stats.t.cdf(abs(t_stat), df=n - 1))

    print(f"\n{label}")
    print(f"  n periods:        {n}")
    print(f"  mean return:      {mean:.4%}")
    print(f"  std dev:          {std:.4%}")
    print(f"  t-statistic:      {t_stat:.2f}")
    print(f"  p-value:          {p_value:.3f}")

    if p_value < 0.05:
        print(f"  -> statistically significant at 5% level")
    else:
        print(f"  -> NOT statistically significant at 5% level")

    return t_stat, p_value


if __name__ == "__main__":
    print("loading data...")
    prices = download_prices()

    print("running momentum backtest...")
    mom_net, mom_gross = run_backtest(prices, lookback=252, skip=21, signal_func=compute_momentum)

    print("running mean-reversion backtest...")
    mr_net, mr_gross = run_backtest(prices, lookback=21, skip=0, signal_func=compute_mean_reversion)

    print("\n" + "=" * 50)
    print("SIGNIFICANCE TESTS")
    print("=" * 50)

    test_significance(mom_gross, "momentum (gross)")
    test_significance(mom_net, "momentum (net)")
    test_significance(mr_gross, "mean-reversion (gross)")
    test_significance(mr_net, "mean-reversion (net)")