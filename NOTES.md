# notes and observations

random things I noticed while building this that I want 
to come back to later

---

**why does the strategy underperform SPY so badly in absolute terms?**

it's market neutral — the long and short legs roughly cancel out 
market exposure. so when SPY goes up 20% in a year, our strategy 
doesn't capture that move. it's only trying to capture the 
*relative* performance of winners vs losers, not the market 
direction. this is actually a feature not a bug if you think of 
it as an uncorrelated return stream.

---

**the 2021-2023 drawdown**

momentum strategies are known to "crash" during rapid market 
reversals. when everyone rushes to sell winners and buy beaten-down 
stocks (value rotation), momentum gets hurt badly. this happened 
in late 2021 through 2022. our drawdown chart shows exactly this.

---

**survivorship bias problem**

all 18 stocks I chose are companies that are still around and 
doing well in 2024. I didn't include any companies that went 
bankrupt or got delisted between 2019-2024. this probably makes 
the results look slightly better than they would in reality since 
failing companies tend to have bad momentum and I'm not shorting 
them.

---

**things to try next**

- expand to full S&P 500 using a proper index membership list
- add Fama-French factor exposure analysis 
- try a 6-month lookback instead of 12 and see if it changes results
- add volatility scaling — size positions by inverse volatility 
  so lower vol stocks get bigger positions
- compare against a simple SPY buy-and-hold properly adjusted 
  for the same market exposure

---

**questions I still don't fully understand**

- how do real funds handle the short side practically? borrow 
  costs seem like they'd eat a lot of the return
- is monthly rebalancing too slow? some papers use weekly
- how sensitive are results to the choice of top_n=5? 
  what if I used top 3 or top 8?

---
**significance testing (t-tests)**
ran a one-sample t-test on all four return series (momentum gross/net, mean-reversion gross/net) to check if any of them are actually distinguishable from zero, or if I'm just looking at noise.
none of them are significant at the 5% level. momentum gross has the highest t-stat (0.75, p=0.456) but that's nowhere close to significant. honestly this makes sense once I think about it — 60 monthly observations is not a lot of data to detect an effect this small. the literature on momentum uses much longer sample periods (often 20-30+ years) and much broader universes, so a 5-year window on the full S&P 500 might just not have enough statistical power to confirm an edge that's real but small.
one thing I noticed: mean-reversion has n=71 periods vs momentum's n=60. this is because mean-reversion only needs a 21-day lookback vs momentum's 252-day lookback, so it starts generating signals much earlier in the data — more of the dataset is usable. worth keeping in mind when comparing them directly.
takeaway: the gross momentum edge is directionally consistent with what the literature would predict, but I can't claim statistical significance with this sample size. that's an honest limitation, not a dead end — more years of data or a broader universe would be the natural next test
---
**out-of-sample split (pre-2023 vs 2023+)**
split the full backtest period at a fixed date (chosen before looking at results) to check if the signals are stable over time or just an artifact of one period.
momentum held up reasonably well — gross Sharpe went from 0.38 (in-sample) to 0.28 (out-sample), same sign, similar magnitude. net Sharpe was negative in both halves (-0.08 and -0.09), which matches what I found in the cost analysis — the cost problem isn't specific to one period, it's structural.
mean-reversion was the surprise. gross Sharpe was -0.32 in-sample but +0.66 out-of-sample — a complete flip. this actually explains something I didn't understand before: the full-sample gross Sharpe was close to 0.00, which I read earlier as "no edge." but this split shows that ~0.00 was actually an average of a strongly negative period and a strongly positive period canceling out, not a stable near-zero edge. that's a meaningfully different conclusion — it suggests mean-reversion here is unstable/regime-dependent rather than simply absent.
caveat: 24-36 periods per bucket is a small sample, so I wouldn't over-read either result, especially the mean-reversion flip — it could partly be noise given how few data points are in each half.