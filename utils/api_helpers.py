import requests


def fetch_asset_data(api_url, start_date, end_date):
    params = {
        "start_date": start_date,
        "end_date": end_date,
        # Other API parameters if needed
    }
    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API request failed with status code: {response.status_code}")
