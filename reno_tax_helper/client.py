"""
Client that calls binance api to get market data
"""
from binance.spot import Spot
from datetime import datetime, timezone

def get_typical_prices(start_date: datetime, end_date: datetime):
    client = Spot()
    tz = timezone.utc
    # adjust the time to 12:00am of the start date
    start_date = datetime(
        year=start_date.year,
        month=start_date.month,
        day=start_date.day,
        tzinfo=tz)
    start_date_epoch = int(start_date.timestamp()) * 1000

    # get the difference in days between start and end date
    diff_days = (end_date - start_date).days

    # Get klines of RVNUSDT at 1d interval
    results = client.klines(symbol="RVNUSDT", interval="1d", startTime=start_date_epoch, limit=diff_days + 1)
    if int(results[0][0]) != start_date_epoch:
        raise ValueError(f"can't find data for start date of {start_date}") 
    prices = {}
    for result in results:
        high = float(result[2])
        low = float(result[3])
        close = float(result[4])
        typical_price = (high + low + close)/3

        open_time = datetime.fromtimestamp(result[0]/1000, tz) # this should be in 12:00am for the particular date
        prices[open_time] = typical_price

    return prices