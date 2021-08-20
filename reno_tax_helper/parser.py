import datetime
from parse import *
from reno_tax_helper.coin_client import get_coin_value, get_asset_info

DATE_FORMAT_STR = "{year:04d}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:{second:02d}{}"

class Transactions:
    
    def validate_currency(self, currency):
        """
            validate that the crypto currency is available in coinmarket cap
        """
        if not currency:
           raise ValueError("Currency symbol can't be empty") 
        
        asset_info = get_asset_info(currency)
        if not asset_info:
           raise ValueError("Error getting asset info about currency ", currency) 
 
        return asset_info
   
    def validate_crypto_currency(self, crypto):
        if not crypto:
           raise ValueError("Crypto currency symbol can't be empty") 
        
        asset_info = self.validate_currency(crypto)
        if not asset_info or not asset_info['type_is_crypto']:
           raise ValueError("Crypto currency symbol is not a crypto") 
        
        return crypto

    def validate_quote_currency(self, quote):
        if not quote:
           raise ValueError("Quote currency symbol can't be empty") 
        
        asset_info = self.validate_currency(quote)
        if not asset_info or asset_info['type_is_crypto']:
           raise ValueError("Quote currency symbol is a crypto") 
        
        return quote
 
    def __init__(self, crypto_currency=None, quote_currency=None):
        self.crypto_currency = self.validate_crypto_currency(crypto_currency)
        self.quote_currency = self.validate_quote_currency(quote_currency)
        self.ts_list=[]
        self.ts_count=0

    class Transaction:
        
        def validate_date(self, date):
            if date is None:
                raise ValueError("date value can't be None")
 
            if not isinstance(date, datetime.date):
                # check if date has a valid format("2021-06-30T23:09:08")
                date_parsed = parse(DATE_FORMAT_STR, date)
                if date_parsed is None:
                    raise ValueError("date parse error")
                date = datetime.datetime(
                    date_parsed.named['year'],
                    date_parsed.named['month'],
                    date_parsed.named['day'],
                    hour=date_parsed.named['hour'],
                    minute=date_parsed.named['minute'],
                    second=date_parsed.named['second'],
                )

            if date > datetime.datetime.now():
                # check if is future date
                raise ValueError("Can't have future dated transaction") 
            
            return date
        
        def validate_amount(self,amount):
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Transaction amount needs to be greater than 0")
            return amount
        
        def __init__(self, date=None, amount=0):
            self.date=self.validate_date(date)
            self.amount=self.validate_amount(amount)
            self.quote=None   
 
    def add_transaction(self, date, amount):
        ts = self.Transaction(date,amount)
        self.ts_list.append(ts)
        self.ts_count+=1
        value = get_coin_value(self.crypto_currency, self.quote_currency, ts.date)
        if value is None:
            raise Exception("Error getting coin value")
        ts.quote = ts.amount * value

def process_file(file_path, crypto_currency, quote_currency, start_index, date_index, amount_index):
    f = open(file_path, "r")
    #create a transaction
    ts = Transactions(crypto_currency, quote_currency)
    #add each transaction and calculate quote price for each transaction
    count = 0
    
    for l in f:
        if count < start_index:
            count += 1
            continue
        
        list_l = l.split(',')
        date = list_l[date_index].strip('\"')
        amount = list_l[amount_index].strip('\"')
        try:
            ts.add_transaction(date, amount)
        except ValueError as e:
            print(e)
            continue
  
    f.close()    
    return ts
