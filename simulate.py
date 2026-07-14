import numpy as np

def simulate_balance_paths(residual_history, recurring_calendar, current_balance,
                             horizon_days=60, n_simulations=10000, seed=1):
    rng = np.random.default_rng(seed)
    residual_values = residual_history.values

    residual_draws = rng.choice(residual_values, size=(n_simulations, horizon_days), replace=True)
    recurring_vector = np.array([recurring_calendar.get((d % 30) + 1, 0) for d in range(horizon_days)])

    daily_flows = residual_draws + recurring_vector
    return current_balance + np.cumsum(daily_flows, axis=1)


def compute_var_cvar(balance_paths, confidence=0.95):
    final_balances = balance_paths[:, -1]
    var_threshold = np.percentile(final_balances, (1 - confidence) * 100)
    cvar = final_balances[final_balances <= var_threshold].mean()
    prob_negative = (balance_paths.min(axis=1) < 0).mean()
    return var_threshold, cvar, prob_negative
