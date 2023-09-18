# helpers/data_processing.py
import dask.dataframe as dd
import pandas as pd
import streamlit as st


@st.cache_data
def get_top_n_stocks(data, group_by, n):
    """
    Calculate the top n stocks based on market capitalization.

    Args:
        data (dd.DataFrame): Input data.
        group_by (str): Grouping interval (e.g., 'week', 'month', 'quarter', 'year').
        n (int): Number of top stocks to retrieve.

    Returns:
        pd.DataFrame: DataFrame containing top n stocks per specified interval.
    """
    data["market_cap"] = data["volume"] * data["close"]

    # Extract date components using Pandas
    date_components = data["date"].dt.isocalendar()

    # Map ISO week to month and quarter
    date_components["month"] = (
        date_components["year"] * 12 + date_components["week"] // 4
    )
    date_components["quarter"] = (
        date_components["year"] * 4 + date_components["week"] - 1
    ) // 13 + 1

    # Merge date components back into Dask DataFrame
    data_with_date_components = dd.concat([data, date_components], axis=1)

    # Group by specified interval and Name
    grouped = (
        data_with_date_components.groupby([group_by, "Name"])["market_cap"]
        .sum()
        .reset_index()
    )

    # Function to find top n stocks
    def top_n_stocks(group, n):
        return group.nlargest(n, "market_cap")

    # Find top n stocks per specified interval
    top_n_stocks_per_interval = (
        grouped.groupby(group_by).apply(top_n_stocks, n=n).compute()
    )

    return top_n_stocks_per_interval
