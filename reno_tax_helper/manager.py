from datetime import datetime, timezone
from reno_tax_helper.parser import process_file
from reno_tax_helper.client import get_typical_prices
"""
Store a list of ravencoin in one usd at a certain date
Value is calculated using the typical price over a day
"""
class PriceList:
    def __init__(self, start_date: datetime=None, end_date : datetime=None):
        self.start_date=self.validate_date(start_date, "start date")
        self.end_date=self.validate_date(end_date, "end date")
        self.prices = get_typical_prices(self.start_date, self.end_date) # amount of rvn in usd at various dates
 
    def validate_date(self, date: datetime, variable_name: str) -> datetime:
        if date == None:
            raise ValueError(f"{variable_name} can't be empty")
        if not isinstance(date, datetime):
            raise ValueError(f"Need to have a valid {variable_name}")
        return date

    def get_price(self, date: datetime):
        # only take the date info from the input. Always use utc timezone
        tmp_date = datetime(date.year, date.month, date.day, tzinfo=timezone.utc)
        return self.prices[int(tmp_date.timestamp()) * 1000]

class TransactionManager:

    def __init__(self, file_path: str, start_row_index: int, date_index: int, amount_index: int):
        self.transaction_list, start_date, end_date = process_file(file_path, start_row_index, date_index, amount_index)
        self.price_list = PriceList(start_date, end_date)
        # TODO populate the fiat amount for transaction list

    def outputAssetSheet(ts=None):
        pass 
