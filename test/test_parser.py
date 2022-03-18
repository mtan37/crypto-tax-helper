from reno_tax_helper.parser import process_file

# content of test_class_demo.py
class TestParser:
    def test_parse_file(self):
        test_file_path='test/resource/test_parser.csv'
        transactions, start_date, end_date = process_file(test_file_path, 1, 1, 5)
        
        assert len(transactions) == 4
        assert transactions[0].amount == 6
        assert transactions[1].amount == 8
        assert transactions[2].amount == 9
        assert transactions[3].amount == 5

        assert start_date.year == 2021
        assert start_date.month == 6
        assert start_date.day == 15
        assert start_date.hour == 12
        assert start_date.minute == 31
        assert start_date.second == 45

        assert end_date.year == 2021
        assert end_date.month == 6
        assert end_date.day == 30
        assert end_date.hour == 23
        assert end_date.minute == 9
        assert end_date.second == 8
