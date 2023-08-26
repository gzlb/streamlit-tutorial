import streamlit as st
import yfinance as yf
from datetime import date, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils import crypto_utils

def pageII():
    st.title('Crypto Dashboard', anchor="title")

    # Sidebar
    tickers = ('BTC', 'ETH', 'SOL', 'ADA', 'DOT', 'MATIC', 'EGLD', 'DOGE', 'XRP', 'BNB')
    coin = st.sidebar.selectbox('Pick a coin from the list', tickers)

    # Page
    col1, col2 = st.columns([1, 5])
    coin_image = f'img/{coin.lower()}.png'
    col1.header(f'{coin}/USD')
    col2.image(coin_image, width=60)

    # Metrics
    col1, col2, col3 = st.columns([2, 2, 2])
    info = crypto_utils.get_market(coin)
    price_difference_24h = (info['price'] - info['priceHigh24h']) / info['price'] * 100
    col1.metric('Price', f'{info["price"]:,}', f'{round(price_difference_24h, 2)}%')
    col2.metric('24h High', f'{info["priceHigh24h"]:,}')
    col3.metric('24h Low', f'{info["priceLow24h"]:,}')

    st.metric('24h Volume', f'{info["volumeUsd24h"]:,}')

    # Check periods

    # ... (rest of the code)

    # Candle and volume chart
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1, row_heights=[100, 30])
    fig.add_trace(
        go.Candlestick(x=coin_df['Date'],
                       open=coin_df['Open'], high=coin_df['High'],
                       low=coin_df['Low'], close=coin_df['Close'],
                       name='Candlestick',
                       ), row=1, col=1
    )

    fig.update_layout(xaxis_rangeslider_visible=False)

    fig.add_trace(
        go.Scatter(
            x=coin_df['Date'],
            y=coin_df['30wma'],
            line=dict(color='#e0e0e0', width=2, dash='dot'),
            name="30-week MA"
        ), row=1, col=1
    )

    # Bar chart
    fig.add_trace(
        go.Bar(
            x=coin_df['Date'],
            y=coin_df['Volume'],
            marker=dict(color=coin_df['Volume'], colorscale='aggrnyl_r'),
            name='Volume'
        ), row=2, col=1
    )
    fig['layout']['xaxis2']['title'] = 'Date'
    fig['layout']['yaxis']['title'] = 'Price'
    fig['layout']['yaxis2']['title'] = 'Volume'
    st.plotly_chart(fig, use_container_width=True)

    # Show data
    if st.checkbox('Show data'):
        st.dataframe(coin_df)

# Run the Streamlit app
if __name__ == "__main__":
    pageII()
