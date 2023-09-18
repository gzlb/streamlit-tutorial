import dask.dataframe as dd
import pandas as pd
import streamlit as st

from utils.data_plotting import plot_top_stocks
from utils.data_processing import get_top_n_stocks


def pageIII():
    st.title("S&P 500 Plots")

    num_steps = st.sidebar.slider(
        "Pick the number of currencies you want to plot based on marketcap",
        min_value=5,
        max_value=50,
        step=5,
    )

    # Page
    col1, col2 = st.columns([5, 5])

    col1.header(f" Top {num_steps} based on market cap in USD")

    check = st.selectbox(
        "Filter by Interval",
        ["Week", "Month", "Quarter", "Year"],
        index=0,
    )
    group_by_interval = check.lower()

    df_initial = dd.read_csv(
        "archive/all_stocks_5yr.csv",
        usecols=["date", "close", "volume", "Name"],
        parse_dates=["date"],
    )
    df_filter = get_top_n_stocks(
        data=df_initial, group_by=group_by_interval, n=num_steps
    )

    # Reset the index before grouping
    df_filter = df_filter.reset_index(drop=True)

    # Display filtered data

    # Plot top stocks
    top_stocks_data = (
        df_filter.groupby(group_by_interval)
        .apply(lambda x: x.head(num_steps))
        .reset_index(drop=True)
    )  # Reset index
    fig = plot_top_stocks(top_stocks_data, interval=group_by_interval)
    st.plotly_chart(fig)

    st.dataframe(df_filter)
