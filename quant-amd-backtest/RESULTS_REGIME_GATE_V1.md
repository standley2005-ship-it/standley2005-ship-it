# Regime Gate V1 — Frozen QQQ Portfolio Research

Date: 2026-08-15

## Purpose

Add a pre-open binary permission layer in front of the frozen OCE-60 + Gap-Continuation Pullback portfolio. The gate is based only on information available before the regular session open. It does not modify entry, stop, target, or exit rules.

## Selection protocol

- Candidate gates were selected on 2019–2022.
- 2023–2024 was used as validation.
- 2025 was sealed until one gate was frozen.
- Early 2026 and the rolling May 20–August 14, 2026 window were test-only.
- The gate was required to retain at least 15 trades in 2021 so it could not solve the problem merely by deleting the difficult regime.

## Frozen Gate V1

Allow Portfolio V1 only when all are true before the open:

- 20-day annualized realized volatility: 14% to 40%
- Absolute prior 5-day QQQ return: <= 3.5%
- Absolute distance from prior 20-day moving average: >= 0.3%
- Absolute distance from prior 50-day moving average: <= 10%
- Absolute premarket return: <= 2%

The selected gate had no effective gap-size or premarket-range restriction.

## QQQ results

### 2019–2022 training

Baseline:
- 180 trades
- 63.33% wins
- +0.0784R/trade
- PF 1.261
- +14.104R
- max R drawdown -6.839R

Gated:
- 83 trades
- 68.67% wins
- +0.1423R/trade
- PF 1.523
- +11.810R
- max R drawdown -3.055R

### 2023–2024 validation

Baseline:
- 71 trades
- 64.79% wins
- +0.1593R/trade
- PF 1.601

Gated:
- 46 trades
- 69.57% wins
- +0.2366R/trade
- PF 2.068

### Sealed 2025 test

Baseline:
- 39 trades
- 58.97% wins
- -0.0152R/trade
- PF 0.956
- -0.592R

Gated:
- 19 trades
- 68.42% wins
- +0.1005R/trade
- PF 1.353
- +1.909R

### Early 2026 test

Baseline:
- 9 trades
- 77.78% wins
- +1.369R

Gated:
- 4 trades
- 100% wins
- +2.438R

Four trades are too small to treat 100% as an expected win rate.

### May 20–August 14, 2026 recent test

Baseline:
- 4 trades
- 25% wins
- -2.310R

Gated:
- 0 trades

The frozen gate blocked all four recent QQQ signals. This is evidence of useful avoidance, not evidence of a 100% winning system.

## Combined 2019–2025

Baseline Portfolio V1:
- 290 trades
- 63.10% wins
- +0.0856R/trade
- PF 1.288
- +24.821R
- max R drawdown -6.839R
- $200 at 2% planned equity risk: about $318.38
- modeled account drawdown about -13.32%

Regime-Gated Portfolio V1:
- 148 trades
- 68.92% wins
- +0.1662R/trade
- PF 1.644
- +24.603R
- max R drawdown -4.509R
- $200 at 2% planned equity risk: about $321.99
- modeled account drawdown about -8.77%

The gate retained about 51% of historical trades while preserving almost all total R, materially raising win rate and expectancy and lowering drawdown.

## Calendar detail after gating

- 2019: 14 trades, 50.0%, -1.333R
- 2020: 23 trades, 78.26%, +8.131R
- 2021: 26 trades, 65.38%, +1.110R
- 2022: 20 trades, 75.0%, +3.901R
- 2023: 25 trades, 60.0%, +2.654R
- 2024: 21 trades, 80.95%, +8.230R
- 2025: 19 trades, 68.42%, +1.909R

2019 remains a weak regime and prevents claiming >=60% in every individual year.

## Seven-symbol recent transfer

The same frozen gate was then applied to QQQ, SPY, IWM, NVDA, AMD, AAPL, and META over May 20–August 14, 2026 with no symbol-specific tuning.

Raw pooled signals:
- 35 opportunities
- 48.57% wins
- -0.156R/trade
- PF 0.648

After frozen gate:
- 5 opportunities
- 80.0% wins
- +0.148R/trade
- PF 1.719
- +0.740R

Per-symbol gated counts were extremely small: QQQ 0, SPY 0, IWM 3, NVDA 1, AMD 0, AAPL 1, META 0. Therefore the 80% pooled result is interesting but not statistically strong.

## Interpretation

Regime Gate V1 is promising as a QQQ permission layer. It improved the sealed 2025 test, preserved the strong early-2026 subset, and blocked the later-2026 QQQ failure signals while improving long-history win rate, expectancy, PF, and drawdown.

It is too aggressive to use as a universal per-symbol gate. The next version should separate:

1. Market regime: determined from QQQ/SPY state.
2. Symbol strategy eligibility: whether a specific underlying is allowed in that market regime.
3. Strategy signal: frozen OCE/GAP or another independently validated engine.
4. Options contract gate: affordability, spread, IV, delta, DTE, liquidity, and expected payoff.

Do not interpret these underlying R results as historical option-contract P&L or a guaranteed future win rate.
