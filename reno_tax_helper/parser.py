from datetime import datetime, timezone
from parse import *

DATE_FORMAT_STR = "{year:04d}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:{second:02d}"

"""
Only support RVN and USDT
"""
class Transaction:
    
    def __init__(self, date: datetime=None, amount: int=0):
        self.date=self.validate_date(date)
        # amount in crypto currency
        self.amount=self.validate_amount(amount)
        self.fiat_amount=None

    def validate_date(self, date):
        if date is None:
            raise ValueError("date value can't be None")

        if not isinstance(date, datetime):
            # check if date has a valid format("2021-06-30T23:09:08")
            date_parsed = parse(DATE_FORMAT_STR, date)
            if date_parsed is None:
                raise ValueError("date parse error")
            date = datetime(
                date_parsed.named['year'],
                date_parsed.named['month'],
                date_parsed.named['day'],
                hour=date_parsed.named['hour'],
                minute=date_parsed.named['minute'],
                second=date_parsed.named['second'],
                tzinfo=timezone.utc
            )

        if date > datetime.now(tz=timezone.utc):
            # check if is future date
            raise ValueError("Can't have future dated transaction") 
        
        return date
    
    def validate_amount(self, amount):
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Transaction amount needs to be greater than 0")
        return amount 

def process_file(file_path, start_row_index, date_index, amount_index):
    f = open(file_path, "r")
    #create a transaction
    ts = []
    #add each transaction and calculate quote price for each transaction
    count = 0
    start_date = None
    end_date = None
    
    for l in f:
        if count < start_row_index:
            count += 1
            continue
        
        list_l = l.split(',')
        date = list_l[date_index].strip('\"')
        amount = list_l[amount_index].strip('\"')
        try:
            transaction  = Transaction(date, amount)
            ts.append(transaction)
            if start_date is None or start_date > transaction.date:
                start_date = transaction.date
            if end_date is None or end_date < transaction.date:
                end_date = transaction.date
        except ValueError as e:
            print(e)
            continue
  
    f.close()    
    return ts, start_date, end_date
