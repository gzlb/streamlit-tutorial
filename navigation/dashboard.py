import plotly.graph_objects as go
import streamlit as st
import yfinance as yf
from plotly.subplots import make_subplots

from utils.fetch_top import fetch_top_currencies


def get_historical(coin: str, start_date, end_date, period=None, interval="1d"):
    coin += "-USD"
    stock = yf.Ticker(coin)

    historical = stock.history(period=period, start=start_date, end=end_date, interval=interval)
    if "Datetime" in historical.columns:
        historical.rename({"Datetime": "Date"}, axis=1, inplace=True)

    return historical


def pageII():
    st.title("Crypto Dashboard", anchor="title")
    col1, col2 = st.columns([1, 2])

    n = st.sidebar.slider("Select Top N Currencies", min_value=5, max_value=50, step=5, value=25)
    top_currencies = fetch_top_currencies(n)

    with col1:
        coin = st.selectbox("Pick a coin from the list", top_currencies)

    start_date = st.sidebar.date_input(
        "Start Date", value=pd.to_datetime("2022-01-01"), key="dstart_date"
    )
    end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("now"), key="dend_date")
    resolution = st.select_slider(
        "Resolution", options=["1d", "5d", "1mo"], value="1d", key="Nresolution"
    )

    coin_df = get_historical_dask(coin, start_date, end_date, interval=resolution)

    # Moving average - 30weeks
    coin_df["30wma"] = coin_df["Close"].rolling(window=30).mean()
    round(coin_df["Close"].var(), 3)

    # Candle and volume chart
    fig = make_subplots(
        rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1, row_heights=[100, 30]
    )
    fig.add_trace(
        go.Candlestick(
            x=coin_df.index,
            open=coin_df["Open"],
            high=coin_df["High"],
            low=coin_df["Low"],
            close=coin_df["Close"],
            name="Candlestick",
        ),
        row=1,
        col=1,
    )

    fig.update_layout(xaxis_rangeslider_visible=False)

    fig.add_trace(
        go.Scatter(
            x=coin_df.index,
            y=coin_df["30wma"],
            line=dict(color="#e0e0e0", width=2, dash="dot"),
            name="30-week MA",
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Bar(
            x=coin_df.index,
            y=coin_df["Volume"],
            marker=dict(color=coin_df["Volume"], colorscale="aggrnyl_r"),
            name="Volume",
        ),
        row=2,
        col=1,
    )

    fig["layout"]["xaxis2"]["title"] = "Date"
    fig["layout"]["yaxis"]["title"] = "Price"
    fig["layout"]["yaxis2"]["title"] = "Volume"
    st.plotly_chart(fig, use_container_width=True)

    # Show data
    if st.checkbox("Show data"):
        st.dataframe(coin_df)


def get_historical_dask(coin: str, start_date, end_date, interval="1d"):
    coin += "-USD"
    stock = yf.Ticker(coin)

    # Fetch data in chunks using Dask
    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")
    historical_dask = dd.from_pandas(pd.DataFrame(), npartitions=10)

    for chunk_start in pd.date_range(start=start_date, end=end_date, freq="1M"):
        chunk_end = chunk_start + pd.DateOffset(months=1)
        chunk_end = min(chunk_end, end_date)
        chunk_data = stock.history(start=chunk_start, end=chunk_end, interval=interval).compute()
        historical_dask = dd.concat(
            [historical_dask, dd.from_pandas(chunk_data, npartitions=1)], axis=0
        )

    return historical_dask


if __name__ == "__main__":
    pageII()
