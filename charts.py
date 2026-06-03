import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

os.makedirs("visualizations", exist_ok=True)


def plot_cumulative_returns(strategy_returns, benchmark_returns=None):
    # converting monthly returns to cumulative growth of $1 so if you started with $1, this shows what it grew to
    cumulative = (1 + strategy_returns).cumprod()

    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(cumulative.index, cumulative.values,
            color="#1f77b4", linewidth=2, label="momentum strategy")

    if benchmark_returns is not None:
        # aligning benchmark to same dates as strategy
        bm_aligned = benchmark_returns.reindex(strategy_returns.index, method="nearest")
        bm_cumulative = (1 + bm_aligned).cumprod()
        ax.plot(bm_cumulative.index, bm_cumulative.values,
                color="#aaaaaa", linewidth=1.5,
                linestyle="--", label="SPY benchmark")

    ax.set_title("momentum strategy vs SPY (2020-2024)",
                 fontsize=14, fontweight="bold", pad=15)
    
    ax.set_ylabel("growth of $1")
    ax.set_xlabel("date")
    ax.legend()
    ax.grid(alpha=0.3)

    # formating x axis so dates are readable
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    fig.tight_layout()

    path = "visualizations/cumulative_returns.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"saved: {path}")
    return path


def plot_monthly_returns_bar(strategy_returns):
    # bar chart of each monthly return
    # easy to see which months were good vs bad
    fig, ax = plt.subplots(figsize=(12, 4))

    colors = ["#2ca02c" if r > 0 else "#d62728"
              for r in strategy_returns.values]

    ax.bar(strategy_returns.index, strategy_returns.values,
           color=colors, width=20, alpha=0.8)

    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_title("monthly returns", fontsize=14,
                 fontweight="bold", pad=15)
    ax.set_ylabel("return")
    ax.set_xlabel("date")
    ax.grid(axis="y", alpha=0.3)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    plt.xticks(rotation=45)
    fig.tight_layout()

    path = "visualizations/monthly_returns.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"saved: {path}")
    return path


def plot_drawdown(strategy_returns):
    # drawdown = how far below the peak are we at each point
    # this tells you the worst case if you had bad timing entering the strategy
    cumulative  = (1 + strategy_returns).cumprod()
    peak        = cumulative.cummax()
    drawdown    = (cumulative - peak) / peak

    fig, ax = plt.subplots(figsize=(12, 4))

    ax.fill_between(drawdown.index, drawdown.values, 0,
                    color="#d62728", alpha=0.4, label="drawdown")
    ax.plot(drawdown.index, drawdown.values,
            color="#d62728", linewidth=1)

    ax.set_title("strategy drawdown", fontsize=14,
                 fontweight="bold", pad=15)
    ax.set_ylabel("drawdown from peak")
    ax.set_xlabel("date")
    ax.grid(alpha=0.3)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    fig.tight_layout()

    path = "visualizations/drawdown.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"saved: {path}")
    return path


if __name__ == "__main__":
    from data import download_prices
    from backtest import run_backtest, compute_metrics

    print("loading data and running backtest...")
    prices  = download_prices()
    returns = run_backtest(prices)

    # get SPY returns for benchmark comparison
    spy_prices  = prices["SPY"]
    spy_daily   = spy_prices.pct_change(fill_method=None)
    # resample SPY daily returns to monthly to match strategy
    spy_monthly = (1 + spy_daily).resample("ME").prod() - 1

    print("generating charts...")
    plot_cumulative_returns(returns, benchmark_returns=spy_monthly)
    plot_monthly_returns_bar(returns)
    plot_drawdown(returns)

    metrics, _ = compute_metrics(returns)
    print("\nperformance summary:")
    for k, v in metrics.items():
        print(f"  {k:<22} {v}")

    print("\ndone - charts saved to visualizations/")