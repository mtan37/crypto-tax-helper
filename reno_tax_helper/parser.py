import datetime
import parse
from coin_client import get_coin_value, get_asset_info

DATE_FORMAT_STR = "{year:04d}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:{second:02d}"

class Transactions:
    
    def validate_currency(self, currency):
        """
            validate that the currency is available in coinmarket cap
        """
        if not currency:
           raise ValueError("Currency symbol can't be empty") 
        
        if not get_asset_info:
           raise ValueError("Currency symbol doesn't exist") 
 
        return currency
    
    def __init__(self, currency=None):
        self.currency=self.validate_currency(currency)
        self.ts_list=[]
        self.ts_count=0

    class Transaction:
        
        def validate_date(self, date):
            if date is None:
                raise ValueError("date value can't be None")
            
            if not isinstance(date, datetime.date):
                # check if date has a valid format("2021-06-30T23:09:08")
                date_parsed = parse(DATE_FORMAT_STR,date)
                date = datetime.datetime(
                    date_parsed.named['year'],
                    date_parsed.named['month'],
                    date_parsed.named['day'],
                    hour=date_parsed.named['hour'],
                    minute=date_parsed.named['minute'],
                    second=date_parsed.named['second'],
                )

            if date > datetime.datetime.now:
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
        ts = Transaction(date,amount)
        self.ts_list.append(ts)
        self.ts_count+=1
