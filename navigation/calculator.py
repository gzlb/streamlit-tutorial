import streamlit as st
from utils.fetch_top import fetch_top_currencies

def calculator():
    st.title('🪙 Cryptocurrency Converter Calculator')
    col1, col2 = st.columns(2)

    top_currencies = fetch_top_currencies(50)
    with col1:
        box01 = st.selectbox('From', top_currencies, key='coin1')
    with col2:
        box02 = st.selectbox('To', top_currencies, key='coin2')
    
    columns = st.columns((2, 1, 2))
    quantity = columns[0].number_input('Quantity')

    # Your conversion calculations here

    columns = st.columns((1, 1))
    quantity = columns[0].metric('', convert)

    # Remaining code
