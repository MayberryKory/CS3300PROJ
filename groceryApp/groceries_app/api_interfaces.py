import requests
from rest_framework.response import Response
from .serializer import GrocerySerializer

def get_kroger_products(api_token, brand, term, location_id):
    url = f'https://api-ce.kroger.com/v1/products?filter.brand={brand}&filter.term={term}&filter.locationId={location_id}'
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {api_token}'
    }

    params = {
        "filter.brand": brand,
        "filter.term": term,
        "filter.locationId": location_id
    }
    
    response = requests.get(url, headers=headers, params=params)
    print(response.content)
   

    if response.status_code == 200:
        kroger_data = response.json()

        # Serialize Kroger data to GroceryItem objects
        serializer = GrocerySerializer(data=kroger_data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
    else:
        error_message = f"Failed to fetch data. Status code: {response.status_code}"
        return Response({'error_message': error_message}, status=response.status_code)
    
def get_client_access(api_token):
    url = f'https://api-ce.kroger.com/v1/connect/oauth2/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {api_token}',
    }
    payload = {
        'grant_type':"client_credentials",
        'scope':['product.compact'],
    }
    response = requests.post(url, headers=headers, data=payload)
    print("CLIENT TOKEN RESPONSE:" + str(response.content))

