import numpy as np
from datetime import date


def simulate_balance_paths(residual_history, recurring_calendar, current_balance,
                           horizon_days=60, n_simulations=10000, seed=None):
    rng = np.random.default_rng(seed)
    residual_values = np.asarray(residual_history.values)

    residual_draws = rng.choice(residual_values, size=(n_simulations, horizon_days), replace=True)

    
    start_day = date.today().day
    recurring_vector = np.array([
        recurring_calendar.get(((start_day - 1 + d) % 30) + 1, 0)
        for d in range(horizon_days)
    ])

    daily_flows = residual_draws + recurring_vector
    return current_balance + np.cumsum(daily_flows, axis=1)


def compute_var_cvar(balance_paths, confidence=0.95):
    
    min_balances = balance_paths.min(axis=1)
    var_threshold = np.percentile(min_balances, (1 - confidence) * 100)
    cvar = min_balances[min_balances <= var_threshold].mean()
    prob_negative = (min_balances < 0).mean()
    return var_threshold, cvar, prob_negative
