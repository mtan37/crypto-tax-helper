import requests
import json
import os
import datetime

COIN_API_KEY=os.getenv('COIN_API_KEY',"")
COIN_BASE_URL='https://rest.coinapi.io'
COIN_EXCHANGE_RATE_URL_FORMAT='/v1/exchangerate/{crypto:}/{quote_currency:}?time={year:04d}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:{second:02d}'

def call(url, key):
    HEADERS = {
        'X-CoinAPI-Key': key,
    }
    response = requests.get(url, headers=HEADERS)
    data = json.loads(response.text)
    print(data)
    return data

def get_coin_value(crypto, quote_currency, date):
    url = COIN_BASE_URL + \
        COIN_EXCHANGE_RATE_URL_FORMAT.format(
            crypto=crypto,
            quote_currency=quote_currency,
            year=date.year,
            month=date.month,
            day=date.day,
            hour=date.hour,
            minute=date.minute,
            second=date.second,
        )
    return call(url,COIN_API_KEY)

get_coin_value('RVN', 'USD', datetime.datetime(2021, 7, 19)) 
