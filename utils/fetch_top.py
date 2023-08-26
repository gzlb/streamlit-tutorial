import requests

def fetch_top_currencies(n):
    # Replace with your CoinMarketCap API endpoint and key
    API_KEY = "YOUR_COINMARKETCAP_API_KEY"
    API_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

    params = {
        'CMC_PRO_API_KEY': API_KEY,
        'start': 1,
        'limit': n,
        'convert': 'USD',
        'sort': 'market_cap',
        'sort_dir': 'desc'
    }

    response = requests.get(API_URL, params=params)
    data = response.json()

    top_currencies = []
    for entry in data['data']:
        symbol = entry['symbol']
        top_currencies.append(symbol)

    return top_currencies
