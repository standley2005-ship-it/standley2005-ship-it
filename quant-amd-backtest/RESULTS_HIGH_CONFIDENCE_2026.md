# High-Confidence Opening Consensus Ensemble — Research Snapshot

Date recorded: 2026-08-15

## Important scope

This is an underlying QQQ intraday signal backtest, not yet an option-contract P&L backtest. The 2026 intraday public source used here extends through March 26, 2026, so the 2026 figures below cover January 26 through March 26 rather than the full calendar year.

Execution assumptions include 1 bp adverse slippage and conservative stop-first resolution when stop and target can both be touched inside the same 5-minute candle.

## Ensemble construction

Two separately selected opening-consensus configurations are frozen. Both vote on independent pre-entry information such as opening drive, session VWAP, EMA structure, overnight gap, premarket direction, and prior daily trend.

The union ensemble takes at most one trade per day when either configuration fires. If both configurations fire in opposite directions, the day is skipped. If both fire in the same direction, the trade is marked as an agreement trade.

Both configurations use an opening-range structural stop, a 0.75R target, and an intraday time exit. No 2026 parameter tuning is performed by the ensemble evaluation script.

## 2019–2025 historical union result

- Trades: 258
- Win rate: 61.6279%
- Average expectancy: +0.07235R per trade
- Profit factor: 1.2376
- Total R: +18.6669R
- Worst cumulative trade-sequence drawdown: -9.0019R
- $200 account simulation at 2% planned risk per trade: $282.39 ending balance
- Simulated max account drawdown at 2% risk: -16.96%

Calendar-year union results:

- 2019: 43 trades, 62.79% win, +2.962R, PF 1.255
- 2020: 41 trades, 63.41% win, +6.042R, PF 1.545
- 2021: 45 trades, 51.11% win, -5.994R, PF 0.683
- 2022: 25 trades, 76.00% win, +7.250R, PF 2.298
- 2023: 36 trades, 58.33% win, +3.053R, PF 1.290
- 2024: 33 trades, 69.70% win, +7.101R, PF 1.856
- 2025: 35 trades, 57.14% win, -1.748R, PF 0.860

## Early-2026 result through March 20

- Trades: 7
- Wins: 6
- Win rate: 85.71%
- Average expectancy: +0.26125R per trade
- Profit factor: 2.772
- Total R: +1.82876R
- $200 account at 2% planned risk: approximately $207.33

Trade dates and directional signals:

- 2026-01-26: long, +0.194R
- 2026-01-27: long, +0.060R
- 2026-02-04: short, +0.737R
- 2026-02-23: short, +0.733R
- 2026-03-11: long, -1.032R
- 2026-03-18: short, +0.725R
- 2026-03-20: short, +0.413R

## Fresh March 23–26 extension

After the ensemble was frozen, a separate one-minute QQQ file extending through March 26 was resampled to the same 5-minute specification. March 23–26 were not part of the earlier holdout.

It generated one additional trade:

- 2026-03-24: short, -1.027R

Combining the original 7 early-2026 trades with this fresh extension gives:

- Trades: 8
- Wins: 6
- Losses: 2
- Win rate: 75.0%
- Total R: approximately +0.802R
- Average expectancy: approximately +0.100R per trade
- Profit factor: approximately 1.39
- $200 account simulation at 2% planned risk: approximately $203.07

## Interpretation

The ensemble clears a 60% win rate over the 258-trade 2019–2025 history and remains above 60% over the limited early-2026 sample. It is not certified for live options trading because (1) 2026 has only eight observed signals in the available dataset, (2) 2021 and 2025 were negative calendar years, (3) the research process has now inspected early-2026 performance while developing the ensemble, so 2026 should no longer be treated as a pristine holdout, and (4) actual Robinhood option-contract performance remains untested.

The next required stage is contract-level testing using historical option quotes, including bid/ask spreads, IV, theta, DTE, affordability, and realistic fills for a $200 account.