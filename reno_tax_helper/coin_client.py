import requests
import json
import os

COIN_API_KEY=os.getenv('COIN_API_KEY',"")
COIN_BASE_URL='https://rest.coinapi.io'
COIN_EXCHANGE_RATE_URL_FORMAT='/v1/exchangerate/{crypto:}/{quote_currency:}?time={year:04d}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:{second:02d}'
COIN_ASSET_SYMBOL_URL_FORMAT='/v1/assets/{crypto}'

class InvalidResponseError(Exception):
    pass

def call(url, key):
    HEADERS = {
        'X-CoinAPI-Key': key,
    }
    response = requests.get(url, headers=HEADERS)
    data = json.loads(response.text)
    return data

def get_coin_value(crypto, quote_currency, time):
    """
    get the value of a coin at certain tiem
    """
    url = COIN_BASE_URL + \
        COIN_EXCHANGE_RATE_URL_FORMAT.format(
            crypto=crypto,
            quote_currency=quote_currency,
            year=time.year,
            month=time.month,
            day=time.day,
            hour=time.hour,
            minute=time.minute,
            second=30,
        )#Current the api call does not consider seconds, and rounds down the minute when second==0
    print(url)
    response = call(url, COIN_API_KEY)
    
    try:
        error = response['error']
        print(error)
        return None 
    except KeyError:
        error = None
   
    if response['asset_id_base'] != crypto or response['asset_id_quote'] != quote_currency:
        raise InvalidResponseError("Invalid response")
    
    rate = response['rate']
    return rate

def get_asset_info(crypto):
    """
    get the info of a currency in dict format
    return None if the currency doesn't exist
    """
    url = COIN_BASE_URL + \
        COIN_ASSET_SYMBOL_URL_FORMAT.format(
            crypto=crypto,
        )
    response = call(url, COIN_API_KEY)

    try:
        error = response[0]['error']
        print(error)
        return None 
    except KeyError:
        error = None

    if response:
        return response[0]
   
    return None
