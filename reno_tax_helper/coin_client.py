import requests
import json

COIN_API_KEY=os.env('COIN_API_KEY',"")
COIN_BASE_URL='https://rest.coinapi.io'
COIN_EXCAHNGE_RATE_URL_FORMAT='/v1/exchangerate/{crypto:}/{quote_currency:}?time={year:d}-{month:d}-{day:d}T00:00:00.0000000Z'

def call(url, key):
    HEADERS = {
        'X-CoinAPI-Key': key,
    }
    
    try:
        response = requests.get(url, headers=headers)
        data = json.loads(response.text)
        print(data)

def get_coin_value(crypto, quote_currency, date):
    # TODO format the URL with parameters
        
