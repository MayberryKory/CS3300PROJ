import requests
import json
import base64
import os

# Get these 3 values from registering your developer account/application with https://developer.kroger.com/
client_id = "shopnest-c3f6a3ac62a8ec4c7a93f6c9aa42d1658272743587919993717"
client_secret = "4yBG7MpD4bYi1imSjMkZQo-I9xsyTSStSlySV4Df"
redirect_uri = ""

# Authentication requires base64 encoded id:secret, which is precalculated here
encoded_client_token = base64.b64encode(f"{client_id}:{client_secret}".encode('ascii')).decode('ascii')

class Product:
    """ Represents a single grocery product """

    def __init__(self, id, upc, brand, description, image, size, price):
        self.id = id
        self.upc = upc
        self.brand = brand
        self.description = description
        self.image = image
        self.size = size
        self.price = price

    def __str__(self):
        verbose = False
        description = f"({self.brand}) {self.description}"
        if self.size:
            description += f" - {self.size}: ${self.price}"
        if verbose:
            description += f"\nProduct ID: {self.id}"
            description += f"\nUPC: {self.upc}"
            description += f"\nImage: {self.image}"
        return description
    
    def __repr__(self):
        return self.__str__()
        

    @classmethod
    def from_json(cls, obj):
        id = obj.get("productId")
        upc = obj.get("upc")
        brand = obj.get("brand")
        description = obj.get("description")
        image = _get_image_from_images(obj.get("images"))
        size = _get_product_size(obj.get("items"))
        price = _get_product_price(obj.get("items"))

        return Product(id, upc, brand, description, image, size, price)

def _get_image_from_images(images, perspective='front', size='medium'):
    front_image = next((image for image in images if image.get("perspective") == perspective), None)
    if front_image:
        sizes = front_image.get("sizes", [])
        front_image = next((s.get("url") for s in sizes if s.get("size") == size), None)
    return front_image

def _get_product_size(items):
    # Not sure when this could be more than one, but its an array so we'll take the first
    if len(items) > 0:
        return items[0].get("size")
    else:
        return None

def _get_product_price(items):
    # Not sure when this could be more than one, but its an array so we'll take the first
    if len(items) > 0:
        return items[0].get("price", {}).get('regular')
    else:
        return None

class Location:
    """ Represents a single kroger location """

    def __init__(self, id, name, address):
        self.id = id
        self.name = name
        self.address = address

    def __str__(self):
        description = f"{self.name} ({self.id})"
        description += f" - {self.address}"
        return description

    def __repr__(self):
        return self.__str__()

    @classmethod
    def from_json(cls, obj):
        id = obj.get("locationId")
        name = obj.get("name")
        address = _get_address(obj.get("address"))
        
        return Location(id, name, address)


def _get_address(address):
    line1 = address.get("addressLine1")
    city = address.get("city")
    state = address.get("state")
    zipcode = address.get("zipCode")

    return f"{line1}, {city}, {state}, {zipcode}"

param_map = {
    'brand': 'filter.brand',
    'chain': 'filter.chain',
    'fulfillment': 'filter.fulfillment',
    'limit': 'filter.limit',
    'location_id': 'filter.locationId',
    'product_id': 'filter.product_id',
    'term': 'filter.term',
    'within_miles': 'filter.radiusInMiles',
    'zipcode': 'filter.zipCode.near',
}

def get_mapped_params(params):
    """ Maps a dictionary of parameters (ignore self) to the api's expected key value """
    return { param_map[key] : value for key, value in params.items() if key != 'self'}


API_URL = 'https://api-ce.kroger.com/v1'

def get_client_access_token(encoded_client_token):
    url = API_URL + '/connect/oauth2/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {encoded_client_token}',
    }
    payload = {
        'grant_type':"client_credentials",
        'scope':['product.compact'],
    }
    response = requests.post(url, headers=headers, data=payload)
    return json.loads(response.text).get('access_token')

class KrogerClient:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.encoded_client_token = base64.b64encode(f"{client_id}:{client_secret}".encode('ascii')).decode('ascii')
        self.token = self.get_client_access_token(self.encoded_client_token)

    @classmethod
    def get_client_access_token(cls, encoded_client_token):
        url = API_URL + '/connect/oauth2/token'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Basic {encoded_client_token}',
        }
        payload = {
            'grant_type': "client_credentials",
            'scope': ['product.compact'],
        }
        response = requests.post(url, headers=headers, data=payload)
        return json.loads(response.text).get('access_token')

    def _make_get_request(self, endpoint, params):
        url = API_URL + endpoint
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}',
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
        # Check the status code to ensure a successful response.
            data = response.json()  # Use .json() to parse the JSON response content
            return data
        else:
            print(f"Request failed with status code {response.status_code}")
            return None

    def search_products(self, term=None, location_id=None, product_id=None, brand=None, fulfillment='csp', limit=5):
        params = get_mapped_params(locals())
        endpoint = '/products'
        endpoint = endpoint + '/{product_id}/'
    
        results = self._make_get_request(endpoint, params=params)
        print(results)
        if results is not None:
            data = results.get('data')
            return [Product.from_json(product) for product in data]
        else:
        # Handle the case where the request failed
            raise Exception("Failed to retrieve data from the API")


    def get_locations(self, zipcode, within_miles=10, limit=5, chain='King Soopers'):
        params = get_mapped_params(locals())
        endpoint = '/locations'

        results = self._make_get_request(endpoint, params=params)
        data = results.get('data')
        return [Location.from_json(location) for location in data]
