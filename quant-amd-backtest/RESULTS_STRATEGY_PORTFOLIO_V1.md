# Strategy Portfolio V1 — QQQ Intraday Research Snapshot

Date recorded: 2026-08-15

## Scope and caveats

This is an underlying QQQ intraday directional-signal backtest, not an options-contract backtest. Historical results do not guarantee future win rates. The early-2026 checkpoint uses data through March 20, 2026; a separate OCE-only extension through March 26 was examined earlier, so 2026 is no longer a pristine holdout for future strategy development.

Common execution assumptions include next-bar entries, 1 bp adverse slippage, conservative stop-first resolution when both stop and target can be reached within the same five-minute candle, and at most one portfolio trade per day.

## Research gate

Each candidate family was sampled with 1,200 seeded parameter variants. A candidate had to survive:

- 2019–2022 training: at least 35 trades, win rate >=57%, positive expectancy >0.03R, PF >=1.12, plus positive subperiod behavior in both 2019–2020 and 2021–2022.
- 2023–2025 validation: at least 20 trades, win rate >=60%, expectancy >0.035R, PF >=1.15.
- Positive expectancy in at least two of 2023, 2024, and 2025 when enough trades existed.
- Only after passing pre-2026 gates was the frozen strategy checked on early 2026.

## Families tested

Rejected under the pre-2026 robustness gate:

- Overnight gap reversal
- Opening-range breakout + retest
- Simple trend pullback
- VWAP opening-shock reversion
- Opening-range failed-break reversal
- Premarket breakout + retest

Historically qualified:

### Gap-Continuation Pullback

Frozen configuration:

- Gap magnitude: 0.5% to 2.0%
- Prior trend filter enabled
- First 45 minutes must confirm at least 0.3% continuation in the gap direction
- EMA confirmation enabled
- Pullback touch tolerance: 0.3 ATR
- Entries no later than 11:00 ET
- Target: 0.6R
- Max underlying structural stop distance: 1.2%
- 1 bp adverse slippage

2019–2022 training:

- Trades: 60
- Win rate: 71.67%
- Average expectancy: +0.1173R
- Profit factor: 1.409
- Total: +7.037R

2023–2025 validation:

- Trades: 35
- Win rate: 71.43%
- Average expectancy: +0.1241R
- Profit factor: 1.447
- Total: +4.345R

Calendar detail:

- 2023: 12 trades, 58.33% wins, -1.235R, PF 0.763
- 2024: 10 trades, 90.00% wins, +4.007R, PF 4.914
- 2025: 13 trades, 69.23% wins, +1.573R, PF 1.451

Early-2026 checkpoint through March 20:

- Trades: 2
- Wins: 1
- Win rate: 50.0%
- Total: -0.459R

This is historically qualified but 2026 remains unconfirmed because the 2026 sample contains only two trades.

## OCE-60 baseline, 2019–2025

- Trades: 258
- Win rate: 61.63%
- Average expectancy: +0.07235R
- Profit factor: 1.2376
- Total: +18.667R
- Worst cumulative trade-sequence drawdown: -9.002R

## Portfolio V1: OCE-60 + Gap-Continuation Pullback

Portfolio rules:

- At most one trade per day.
- If the two engines disagree on direction, skip the day.
- If they agree, take the earliest valid setup.
- If only one engine fires, that engine may supply the trade.

2019–2025 portfolio result:

- Trades: 290
- Win rate: 63.10%
- Average expectancy: +0.08559R
- Profit factor: 1.2875
- Total: +24.821R
- Worst cumulative trade-sequence drawdown: -6.839R
- Incremental trades versus OCE alone: +32
- Opportunity increase versus OCE alone: about +12.4%
- Agreement days: 63
- Gap-only days: 32
- OCE-only days: 195
- Conflict days skipped: 0

$200 account simulation at 2% planned risk per trade:

- Ending balance: $318.38
- Maximum modeled account drawdown: -13.32%

For comparison, OCE-60 alone previously produced about $282.39 with roughly -16.96% modeled maximum account drawdown at the same 2% risk assumption.

### Portfolio calendar years

- 2019: 45 trades, 64.44% wins, +4.089R, PF 1.352
- 2020: 46 trades, 63.04% wins, +6.137R, PF 1.483
- 2021: 48 trades, 54.17% wins, -4.376R, PF 0.769
- 2022: 41 trades, 73.17% wins, +8.254R, PF 1.771
- 2023: 37 trades, 59.46% wins, +3.634R, PF 1.345
- 2024: 34 trades, 70.59% wins, +7.675R, PF 1.926
- 2025: 39 trades, 58.97% wins, -0.592R, PF 0.956

The portfolio improves the aggregate result but does not eliminate regime weakness: 2021 and 2025 remain losing years, and 2023/2025 calendar win rates remain below 60% even though the full-period win rate is above 60%.

## Early-2026 portfolio checkpoint through March 20

OCE-60 alone:

- 7 trades
- 85.71% wins
- +1.829R
- PF 2.772

Gap-Continuation Pullback alone:

- 2 trades
- 50.0% wins
- -0.459R

Combined Portfolio V1:

- 9 trades
- 77.78% wins
- Average expectancy: +0.1522R
- Profit factor: 1.669
- Total: +1.369R
- $200 at 2% planned risk: approximately $205.38
- Modeled max drawdown: approximately -2.06%
- 2 incremental early-2026 opportunities versus OCE alone
- No strategy-direction conflicts in the sample

## Interpretation

Portfolio V1 achieved the research objective in the historical underlying-signal test: it increased trade opportunities while keeping the aggregate win rate above 60%. It also improved historical expectancy, profit factor, total R, and modeled drawdown versus OCE-60 alone.

It is not certified for autonomous Robinhood options trading. The next required gates are:

1. Expand opportunity horizontally across additional liquid underlyings using frozen logic rather than weakening QQQ filters.
2. Measure cross-instrument stability and signal correlation.
3. Run actual historical option-contract selection and fills, including bid/ask, IV, DTE, delta, theta, liquidity, and affordability for a ~$200 account.
4. Shadow trade before live autonomous execution.
