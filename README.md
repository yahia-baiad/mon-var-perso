# Personal Value-at-Risk

An application that applies **Value-at-Risk** and **Conditional VaR** : The risk measures banks use daily to a personal bank account.

The idea: instead of asking "how much will I spend next month?", ask "in the worst 5% of scenarios, how low can my balance go?"

---

## Method

The model splits cash flows into two categories, because they don't behave the same way:

**Recurring flows (deterministic)** rent, subscriptions, salary. They land on fixed dates for known amounts, so they're applied as-is through a monthly calendar anchored to today's date.

**Residual flows (stochastic)** everyday discretionary spending. These are aggregated into daily totals (days with no spending counted as zero), then resampled via **bootstrap**: each simulated day randomly draws from a day actually observed in the history.

The simulation generates 10,000 balance paths over the chosen horizon, then extracts three indicators.

### The three metrics

| Metric | Definition | How to read it |
|---|---|---|
| **VaR (floor balance)** | 5th percentile of the **minimum** balance reached over the horizon | In 95% of scenarios, the balance stays above this level |
| **CVaR** | Average of the minima falling below the VaR threshold | When things go badly, how badly they go |
| **Overdraft risk** | Probability that the minimum drops below zero | Chance of going into the red |

**Key modelling point:** all three metrics are based on the **minimum balance across the whole horizon**, not the final-day balance. This isn't a cosmetic distinction measuring the final day produced a reassuring but wrong result, because that day happened to fall on a payday. Overdraft risk lives in the troughs of the monthly cycle, not at its peak.

---

## Installation

```bash
git clone https://github.com/yahia-baiad/mon-var-perso.git
cd mon-var-perso
pip install -r requirements.txt
streamlit run app.py
```

The app opens at `http://localhost:8501`.

---

## Project structure

| File | Purpose |
|---|---|
| `app.py` | Streamlit interface and metric display |
| `data.py` | Synthetic transaction generation, recurring calendar, residual history extraction |
| `simulate.py` | Monte Carlo path simulation and VaR / CVaR computation |
| `viz.py` | Plotly fan chart (median plus 25–75% and 5–95% intervals) |

---

## Data

All transactions are **fully synthetic**, generated with a fixed seed for reproducibility. No real banking data is used, stored, or transmitted.

Simulated profile: semi-monthly income of roughly $650, $750 rent on the 1st, subscriptions on the 5th, and daily discretionary spending drawn from a Gamma distribution.

---

## Known limitations

This is a modelling exercise, and the model rests on assumptions worth stating openly:

- **i.i.d. bootstrap** : Each day is drawn independently. The model ignores autocorrelation in spending (one large expense doesn't predict another) and day-of-week effects (people spend more on Saturdays). This is the main limitation.
- **30-day months** : The recurring calendar uses a modulo 30. Months with 31 days drift slightly, and February has no 30th.
- **Deterministic income** : Salary is treated as certain, which doesn't fit variable or freelance income.
- **No tail events**: The model captures neither one-off large expenses nor income interruptions.

Natural extensions would be a block bootstrap to preserve temporal structure, or segmenting residuals by day of week.

---

## Stack

Python · NumPy · pandas · Streamlit · Plotly
