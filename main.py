# main.py
import matplotlib.pyplot as plt

from utils.api_helpers import fetch_asset_data
from utils.data_processing import process_data
import pandas as pd
import streamlit as st

from navigation.landing import pageI
from navigation.dashboard import pageII
from navigation.calculator import calculator

# def calculate_market_cap(df):
#     # Calculate market cap based on price and quantity data in the DataFrame
#     df["market_cap"] = df["price"] * df["quantity"]
#     return df


def main():
    # api_url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    # start_date = "2022-08-22"
    # end_date = "2023-08-22"

    # data = fetch_asset_data(api_url, start_date, end_date)
    # processed_data = pd.DataFrame(data)
    # # processed_data = calculate_market_cap(processed_data)

    # # User input for top count
    # top_count = int(input("Enter the number of top assets to display (10, 25, or 50): "))
    # if top_count not in [5, 10, 25, 50]:
    #     print("Invalid selection. Displaying top 25 assets by default.")
    #     top_count = 25

    # # Select top assets based on market cap
    # top_assets = processed_data.groupby("asset_name").market_cap.mean().nlargest(top_count)

    # # Plotting the values over the past year for top assets
    # plt.figure(figsize=(10, 6))
    # for asset_name in top_assets.index:
    #     asset_data = processed_data[processed_data["asset_name"] == asset_name]
    #     plt.plot(asset_data["date"], asset_data["price"], label=asset_name)

    # plt.xlabel("Date")
    # plt.ylabel("Price")
    # plt.title(f"Top {top_count} Assets by Market Cap Over the Past Year")
    # plt.legend()
    # plt.xticks(rotation=45)
    # plt.tight_layout()
    # plt.show()

    # Streamlit pages
    st.set_page_config(layout="wide")
    st.sidebar.image(
        "https://res.cloudinary.com/crunchbase-production/image/upload/c_lpad,f_auto,q_auto:eco,dpr_1/z3ahdkytzwi1jxlpazje",
        width=50,
    )

    pages = {
        "🏠 Main Page": pageI,
        "📈 Crypto Dashboard": pageII,
        "💰 Calculator": calculator.calculator,
    }

    selected_page = st.sidebar.radio("Navigation", pages.keys())
    pages[selected_page]()
