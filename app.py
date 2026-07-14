import streamlit as st
from data import generate_synthetic_transactions, recurring_calendar, get_residual_history
from simulate import simulate_balance_paths, compute_var_cvar
from viz import plot_fan_chart

st.title("📊 Mon VaR personnel")

@st.cache_data
def load_residual_history():
    df = generate_synthetic_transactions()
    return get_residual_history(df)

residual_history = load_residual_history()

current_balance = st.number_input("Solde actuel ($)", value=1500.0)
horizon = st.slider("Horizon (jours)", 30, 120, 60)
confidence = st.select_slider("Niveau de confiance", options=[0.90, 0.95, 0.99], value=0.95)

if st.button("Lancer la simulation"):
    paths = simulate_balance_paths(residual_history, recurring_calendar, current_balance, horizon)
    var, cvar, prob_neg = compute_var_cvar(paths, confidence)

    col1, col2, col3 = st.columns(3)
    col1.metric("VaR (solde plancher)", f"{var:.0f} $")
    col2.metric("CVaR (pire 5% en moyenne)", f"{cvar:.0f} $")
    col3.metric("Risque de solde négatif", f"{prob_neg:.1%}")

    st.plotly_chart(plot_fan_chart(paths), use_container_width=True)
