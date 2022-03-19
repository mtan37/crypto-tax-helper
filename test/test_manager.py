from reno_tax_helper.manager import PriceList, TransactionManager
from unittest.mock import patch
from datetime import datetime, timezone

# content of test_class_demo.py
class TestManager:

    @patch("reno_tax_helper.manager.get_typical_prices")
    def test_get_prices(self, get_typical_prices):
        start_date = datetime(2001, 1, 3, tzinfo=timezone.utc)
        end_date = datetime(2001, 1, 5, tzinfo=timezone.utc)
        time1 = int(datetime(2001, 1, 3, tzinfo=timezone.utc).timestamp()) * 1000
        time2 = int(datetime(2001, 1, 4, tzinfo=timezone.utc).timestamp()) * 1000
        time3 = int(datetime(2001, 1, 5, tzinfo=timezone.utc).timestamp()) * 1000
        get_typical_prices.return_value = {
            time1: 3,
            time2: 4,
            time3: 1,
        }
        price_list = PriceList(start_date, end_date)

        test_time1 = datetime(2001, 1, 3, 1, 2, 22, tzinfo=timezone.utc)
        test_time2 = datetime(2001, 1, 4, 1, 2, 22, tzinfo=timezone.utc)
        test_time3 = datetime(2001, 1, 5, 1, 2, 22, tzinfo=timezone.utc)
        assert price_list.get_price(test_time1) == 3
        assert price_list.get_price(test_time2) == 4
        assert price_list.get_price(test_time3) == 1

    @patch("reno_tax_helper.manager.get_typical_prices")
    def test_populate_fiat_amount(self, get_typical_prices):
        time1 = int(datetime(2021, 6, 29, tzinfo=timezone.utc).timestamp()) * 1000
        time2 = int(datetime(2021, 6, 30, tzinfo=timezone.utc).timestamp()) * 1000
        get_typical_prices.return_value = {
            time1: 2,
            time2: 3,
        }

        test_file_path='test/resource/test_parser.csv'
        manager = TransactionManager(test_file_path, 1, 1, 5)
        assert manager.transaction_list[0].fiat_amount == 18
