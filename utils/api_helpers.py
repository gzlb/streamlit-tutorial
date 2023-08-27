import requests
from datetime import datetime
import coinmarketcapapi


def fetch_asset_data(api_url, start_date, end_date):
    API_KEY = "00d5b114-9687-4884-b922-ba32d3f753fe"

    cmc_client = coinmarketcapapi.CoinMarketCapAPI(API_KEY)
    response = cmc_client.tools_priceconversion(amount=1, symbol="ETH", convert="USD")
    response.data
    print(response.data)
