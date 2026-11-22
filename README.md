# momentum-equity-research

![cumulative returns](visualizations/cumulative_returns.png)

**Does 12-month momentum still earn a premium on large-cap US stocks once you charge realistic trading costs, and how does it compare with short-term mean reversion on the same data?**

Short answer: momentum shows a small positive gross edge that is consistent over time but not statistically significant over 5 years. Mean reversion shows no edge overall, but that "no edge" is two opposite regimes cancelling out.

## Data and period

- **Universe:** S&P 500 constituents (~500 tickers, scraped from Wikipedia), plus SPY/QQQ as benchmarks
- **Prices:** daily adjusted closes from yfinance, Jan 2019 – Dec 2024
- **Backtest windows:** momentum 2020–2024 (60 monthly rebalances; the first year is used up by the 12-month lookback), mean reversion 2019–2024 (71 rebalances)

## Method, in plain English

1. **Every month** (every 21 trading days), rank all stocks by a signal.
   - **Momentum:** return from 12 months ago to 1 month ago. Skipping the last month is the standard "12-1" specification (Jegadeesh & Titman, 1993).
   - **Mean reversion:** last month's return, inverted, so the biggest recent losers rank highest (Jegadeesh, 1990).
2. **Go long the top 5 and short the bottom 5**, equal-weighted.
3. **Hold for the next 21 trading days**, then rebalance.
4. **Charge 10 bps round-trip per rebalance**, assuming full turnover on both legs. This is conservative, because some names stay in the basket.
5. **Test whether it's real:** one-sample t-test on each return series, plus a time split at Jan 2023 to check stability.

## Results

Gross of costs, monthly long/short returns:

| metric | momentum | mean reversion |
|---|---|---|
| Sharpe ratio | 0.34 | 0.00 |
| hit rate (profitable months) | 58.3% | 56.3% |
| t-statistic | 0.75 | 0.01 |
| p-value | 0.46 | 0.99 |
| periods | 60 | 71 |

> **Net-of-cost results are being recomputed.** I found a bug in how monthly returns were aggregated: daily returns were averaged instead of compounded over each 21-day holding period. That bug understated return and volatility levels and mis-scaled the 10 bps cost charge. Sharpe, hit rate and the t-tests above are essentially unaffected by that scaling. Return, volatility, drawdown, all net figures and the charts will be updated after the re-run.

**Stability (split at Jan 2023, chosen before looking at either half):**

| | 2020–2022 gross Sharpe | 2023–2024 gross Sharpe |
|---|---|---|
| momentum | 0.38 | 0.28 |
| mean reversion | −0.32 | +0.66 |

**What this says:**
- Momentum's gross edge points the right way and holds in both halves, but 60 monthly observations isn't enough statistical power to confirm an edge this small (p = 0.46).
- Mean reversion's flat full-sample result hides a full regime flip. That suggests instability rather than an absent effect, though with roughly 24–36 periods per half it's suggestive, not conclusive.

## Look-ahead bias controls

| Control | Where | Why it matters |
|---|---|---|
| Signal on day T uses only prices up to T | `signals.py`: `prices.shift(skip) / prices.shift(lookback)` | The ranking can't peek at prices that wouldn't have existed yet when the trade was placed |
| Returns are earned from T+1, never on day T | `backtest.py`: `forward_returns = daily_returns.shift(-1)` | Using the same day's return both to form the signal and to score it is the classic look-ahead bug, and it inflates results |
| Holding periods don't overlap | 21-day rebalance, 21-day hold | Each month's return is measured on fresh data, so no observation is counted twice |
| Signal parameters come from the literature, not tuning | 12-1 momentum, 1-month reversal | Searching over lookbacks until something works is look-ahead by another name (data snooping) |
| Out-of-sample split date fixed in advance | `oos_split.py`: `SPLIT_DATE = "2023-01-01"` | Picking the split after seeing results would let hindsight choose the "good" period |
| Costs and significance tests reported alongside gross returns | `compare_signals.py`, `significance_test.py` | Keeps a gross number that looks good from being read as a tradable result |

**Known gaps** (not yet controlled):
- **Survivorship bias:** the universe is *today's* S&P 500 list, so stocks removed from the index during 2019–2024 are missing. This is itself a form of look-ahead, because it uses knowledge of which companies survived. The fix is point-in-time constituent lists.
- **Forward-filled prices:** halted or suspended stocks carry a stale price, which shows up as zero return instead of being excluded.

## Limitations

- Only 5 years of data, so there's low power to detect small effects
- Flat 10 bps cost model, not based on actual per-stock spread or liquidity data
- No separate borrow cost on the short leg

## Next steps

- Point-in-time index membership to remove survivorship bias
- Volatility-scaled position sizing
- Longer lookback or lower rebalance frequency to cut turnover and costs
- Fama-French factor exposure analysis
- Longer history for more statistical power

## More charts

![monthly returns](visualizations/monthly_returns.png)
![drawdown](visualizations/drawdown.png)

## How to run

```bash
git clone https://github.com/Hena3124/momentum-equity-research
cd momentum-equity-research
pip3 install -r requirements.txt
python3 data.py              # download/cache S&P 500 prices
python3 backtest.py          # momentum backtest (net + gross)
python3 compare_signals.py   # momentum vs mean reversion
python3 significance_test.py # t-tests
python3 oos_split.py         # pre-2023 vs 2023+ stability
python3 charts.py            # regenerate charts
```

**Stack:** Python · pandas · NumPy · SciPy · yfinance · matplotlib · requests

<details>
<summary>What tripped me up</summary>

- **Look-ahead bias:** I fixed it by shifting returns forward one day so the portfolio only earns returns after the signal is computable.
- **Wikipedia 403s:** `pd.read_html()` alone was blocked without a User-Agent, so I fetch with `requests` first.
- **yfinance on 500 tickers:** batched the downloads into groups of 100.

</details>
