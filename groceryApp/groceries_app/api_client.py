import requests

class KrogerAPIClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.kroger.com/v1'

    def fetch_product_data(self, product_id, location_id):
        url = f"{self.base_url}/products/{product_id}?filter.locationId={location_id}"
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.api_key}',
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return None
