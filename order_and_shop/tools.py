import os
import requests
import jwt
import time
from dotenv import load_dotenv

load_dotenv()

API_URL = 'https://example.com/api/send_order'
API_KEY = os.getenv('API_KEY')
MAX_RETRIES = 3


def generate_jwt():
    return jwt.encode({'some': 'payload'}, API_KEY, algorithm='HS256')


def send_order_to_external_api(order_id, shop_id):
    jwt_token = generate_jwt()
    headers = {'Authorization': f'Bearer {jwt_token}'}
    data = {'orderid': order_id, 'shpid': shop_id}

    for attempt in range(MAX_RETRIES):
        try:
            response = requests.post(API_URL, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            if attempt < MAX_RETRIES - 1:
                time.sleep(2 ** attempt)
            else:
                raise e
