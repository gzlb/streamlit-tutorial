import dask.dataframe as dd
import pandas as pd
import streamlit as st

from utils.data_processing import get_top_n_stocks


def pageII():
    st.title("S&P 500 Ranking", anchor="title")

    num_steps = st.sidebar.slider(
        "Pick the number of currencies you want to rank based on marketcap",
        min_value=5,
        max_value=50,
        step=5,
    )

    # Page
    col1, col2 = st.columns([5, 5])

    col1.header(f" Top {num_steps} based on market cap in USD")

    check = st.radio(
        "Filter", ["weekly", "monthly", "quarterly", "annual"], horizontal=True, index=0
    )

    if check == "weekly":
        group_by_interval = "week"
    elif check == "monthly":
        group_by_interval = "month"
    elif check == "quarterly":
        group_by_interval = "quarter"
    else:
        group_by_interval = "year"

    df_initial = dd.read_csv(
        "archive/all_stocks_5yr.csv",
        usecols=["date", "close", "volume", "Name"],
        parse_dates=["date"],
    )
    df_filter = get_top_n_stocks(
        data=df_initial, group_by=group_by_interval, n=num_steps
    )

    # st.dataframe(df_filter)

    # Display the top n tickers
    top_tickers = df_filter["Name"].unique()[:num_steps]
    ticker_df = pd.DataFrame({"Name": top_tickers})
    ticker_df.index += 1  # Numbering starts from 1

    col1.dataframe(df_filter, height=300)
    col2.header("Top Tickers")
    col2.dataframe(ticker_df, height=300)

    if st.checkbox("Show complete data"):
        st.dataframe(df_initial)
