import numpy as np
import pandas as pd

def generate_synthetic_transactions(start_date="2024-01-01",n_months=12, seed=42):
    rng = np.random.default_rng(seed)
    end_date = pd.Timestamp(start_date) + pd.DateOffset(months=n_months)
    dates = pd.date_range(start=start_date, end=end_date, freq="D", inclusive="left")
    rows = []

    for date in dates:
        if date.day in (15,30):
            rows.append({"date": date, "amount": rng.normal(650,40),"type": "income"})
        if date.day == 1:
            rows.append({"date": date, "amount": -750, "type": "rent"})
        if date.day == 5:
            rows.append({"date": date, "amount": -35.99, "type": "subscriptions"})
        daily_spend = rng.gamma(shape=2, scale=8)
        if daily_spend > 1:
            rows.append({"date": date, "amount": -round(daily_spend, 2), "type": "discretionary"})

    return pd.DataFrame(rows)


recurring_calendar = {
    1: -750,     # loyer
    5: -35.99,   # abonnements
    15: 650,     # paie
    30: 650,     # paie
}

RECURRING_TYPES = {"rent", "subscriptions", "income"}

def get_residual_history(df):
    res = df.loc[~df["type"].isin(RECURRING_TYPES)]
    daily = res.groupby("date")["amount"].sum()
    full_index = pd.date_range(df["date"].min(), df["date"].max(), freq="D")
    return daily.reindex(full_index, fill_value=0.0)

