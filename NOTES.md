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