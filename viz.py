import numpy as np
import plotly.graph_objects as go

def plot_fan_chart(balance_paths):
    days = np.arange(balance_paths.shape[1])
    p5, p25, p50, p75, p95 = (np.percentile(balance_paths, q, axis=0) for q in (5, 25, 50, 75, 95))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=days, y=p95, line=dict(width=0), showlegend=False))
    fig.add_trace(go.Scatter(x=days, y=p5, fill="tonexty", fillcolor="rgba(99,110,250,0.15)",
                              line=dict(width=0), name="Intervalle 5–95 %"))
    fig.add_trace(go.Scatter(x=days, y=p75, line=dict(width=0), showlegend=False))
    fig.add_trace(go.Scatter(x=days, y=p25, fill="tonexty", fillcolor="rgba(99,110,250,0.3)",
                              line=dict(width=0), name="Intervalle 25–75 %"))
    fig.add_trace(go.Scatter(x=days, y=p50, line=dict(color="rgb(99,110,250)", width=2), name="Médiane"))
    fig.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="Zéro")
    fig.update_layout(title="Projection de solde", xaxis_title="Jours", yaxis_title="Solde ($)")
    return fig
