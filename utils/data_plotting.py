import plotly.graph_objects as go
import streamlit as st


@st.cache_data
def plot_top_stocks(top_stocks_data, interval):
    fig = go.Figure()

    for stock_name, stock_data in top_stocks_data.groupby("Name"):
        fig.add_trace(
            go.Scatter(
                x=stock_data[interval],
                y=stock_data["market_cap"],
                mode="lines",
                name=stock_name,
            )
        )

    interval_label = interval.capitalize()
    fig.update_layout(
        height=600,
        showlegend=True,
        title_text=f"Top Stocks by Market Cap ({interval_label})",
        xaxis=dict(title=interval_label),
        yaxis=dict(title="Market Cap"),
    )

    return fig
