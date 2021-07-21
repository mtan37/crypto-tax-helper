import unittest
from reno_tax_helper.coin_client import get_coin_value, InvalidResponseError
from unittest.mock import patch
from datetime import datetime
class TestApiCall(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        self.r1={'asset_id_base': 'RVN', 'asset_id_quote': 'USD', 'rate': 0.0502182830088944} 
        pass
    
    @classmethod
    def tearDownClass(self):
        pass
    
    def test_get_coin_value_success(self):
        with patch('reno_tax_helper.coin_client.call') as mocked_call:
            mocked_call.return_value = self.r1
            
            self.assertEqual(
                get_coin_value('RVN', 'USD', datetime(2021,2,1,hour=23, minute=30)),
                0.0502182830088944
            )
    
    def test_get_coin_value_fail_mismatch_crypto(self):
        with patch('reno_tax_helper.coin_client.call') as mocked_call:
            mocked_call.return_value = self.r1
            
            with self.assertRaises(InvalidResponseError):
                get_coin_value('AAA', 'USD', datetime(2021,2,1,hour=23, minute=30))
        
    def test_get_coin_value_fail_mismatch_quote(self):
        with patch('reno_tax_helper.coin_client.call') as mocked_call:
            mocked_call.return_value = self.r1
            
            with self.assertRaises(InvalidResponseError):
                get_coin_value('RVN', 'AAA', datetime(2021,2,1,hour=23, minute=30))
        
