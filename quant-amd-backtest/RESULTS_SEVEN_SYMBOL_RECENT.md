# Frozen Portfolio V1 — Seven-Symbol Recent Transfer Test

Date: 2026-08-15

## Test design

Symbols: QQQ, SPY, IWM, NVDA, AMD, AAPL, META.

Rules were frozen before this test. No symbol-specific optimization was allowed. The test used the same rolling 60 trading days of 5-minute premarket/regular/postmarket data from Yahoo Finance, covering 2026-05-20 through 2026-08-14. This is a recent portability/regime test, not a substitute for the prior 2019-2025 QQQ validation.

The tested portfolio consists of frozen OCE-60 plus the frozen Gap-Continuation Pullback strategy. Execution assumptions remain next-bar/strategy-defined entries, 1 bp adverse slippage, conservative stop-first same-bar resolution, and one combined strategy trade per symbol per day.

## Results by symbol

| Symbol | Portfolio trades | Win rate | Avg R | Profit factor | Total R | Read |
|---|---:|---:|---:|---:|---:|---|
| QQQ | 4 | 25.00% | -0.5778R | 0.241 | -2.311R | Recent failure |
| SPY | 6 | 66.67% | +0.0360R | 1.105 | +0.216R | Encouraging but tiny sample |
| IWM | 9 | 44.44% | -0.1836R | 0.547 | -1.653R | Failure |
| NVDA | 4 | 50.00% | -0.1733R | 0.657 | -0.693R | Failure |
| AMD | 0 | N/A | N/A | N/A | 0R | No evidence / no signals |
| AAPL | 7 | 42.86% | -0.1734R | 0.552 | -1.213R | Failure |
| META | 5 | 60.00% | +0.0387R | 1.096 | +0.194R | Encouraging but tiny sample |

### Component observations

- SPY OCE: 6 trades, 66.67% wins, +0.216R total. Gap strategy produced no trades.
- META OCE: 4 trades, 75.00% wins, +1.207R; adding one losing Gap trade reduced the combined result to 60.00% wins and +0.194R.
- AAPL Gap: 2 trades, both winners, +1.162R total, but AAPL OCE was poor, leaving the combined portfolio negative.
- AMD produced no valid OCE or Gap signals in the window.
- QQQ itself was poor in this later-2026 window despite strong earlier-2026 and long-history results, reinforcing the presence of regime drift.

## Blind seven-symbol pooling

Treating every per-symbol portfolio signal as an independent raw opportunity produced:

- 35 opportunities
- 48.57% win rate
- -0.1560R average expectancy
- Profit factor 0.648
- 28 unique signal days
- 6 days with signals in multiple symbols
- Maximum 3 symbol signals on one day

Therefore, blindly expanding the frozen QQQ portfolio to all seven symbols is rejected.

## Interpretation

The recent transfer test does not support using the same frozen Portfolio V1 rules indiscriminately across QQQ, SPY, IWM, NVDA, AMD, AAPL, and META. SPY and META are the only positive combined results, but their samples are too small and profit factors too weak to promote. AAPL's Gap component is interesting but has only two observations.

The most important finding is regime sensitivity: even QQQ fell to 25% wins over four portfolio trades in the May 20-August 14 window. This supports building a regime gate before increasing live opportunity count.

## Next research gates

1. Acquire uniform multi-year intraday data for all seven symbols and run the frozen transfer test without retuning.
2. Build a regime classifier/gate that can disable Portfolio V1 during historically hostile environments.
3. Re-test SPY and META first because they were the only positive recent transfers.
4. Keep AMD disabled until the rules generate enough opportunities to evaluate.
5. Do not move any newly tested symbol to autonomous options execution based on this 60-day sample.
