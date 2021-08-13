import unittest
from unittest.mock import patch, call
from reno_tax_helper.parser import Transactions 

class TestTransactionData(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        self.is_crypto={'type_is_crypto': True}
        self.not_crypto={'type_is_crypto': False}
        self.date='2021-06-30T23:09:08'
    @classmethod
    def tearDownClass(self):
        pass
    
    @patch('reno_tax_helper.parser.get_asset_info') 
    def test_create_transactions_fail_no_arg(self, mocked_call):
        with self.assertRaises(ValueError):
            transactions = Transactions()
        assert not mocked_call.called, 'get_asset_info should not be called'  
    
    @patch('reno_tax_helper.parser.get_asset_info') 
    def test_create_transactions_fail_empty_arg(self, mocked_call):     
        with self.assertRaises(ValueError):
            transactions = Transactions("", "")  
        assert not mocked_call.called, 'get_asset_info should not be called'  
    
    @patch('reno_tax_helper.parser.get_asset_info') 
    def test_create_transactions_fail_not_exist_currency(self, mocked_call):
        #invalid crypto, valid quote currency
        mocked_call.side_effect = [None, self.not_crypto]
        with self.assertRaises(ValueError):
            transactions = Transactions("123", "USD")  
        mocked_call.assert_called_with("123")
        
    @patch('reno_tax_helper.parser.get_asset_info') 
    def test_create_transactions_fail_not_exist_currency_quote(self, mocked_call):
        #invalid crypto, invalid quote currency
        mocked_call.side_effect = [None, None]
        with self.assertRaises(ValueError):
            transactions = Transactions("123", "123")
        mocked_call.assert_called_with("123")
        
    @patch('reno_tax_helper.parser.get_asset_info') 
    def test_create_transactions_fail_not_exist_quote(self, mocked_call):
        #valid crypto, invalid quote currency
        mocked_call.side_effect = [self.is_crypto, None]
        with self.assertRaises(ValueError):
            transactions = Transactions("RVN", "123")
        mocked_call.assert_has_calls(
            [call("RVN"), 
            call("123")]
        )

    @patch('reno_tax_helper.parser.get_coin_value') 
    @patch('reno_tax_helper.parser.get_asset_info') 
    def test_add_transaction_successful(self, mocked_call, mocked_call2):
        mocked_call.side_effect = [self.is_crypto, self.not_crypto]
        mocked_call2.return_value = 1
        transactions = Transactions("RVN","USD")
        transactions.add_transaction(self.date,20)

        assert transactions.ts_count == 1
        assert transactions.ts_list[0].amount == 20
        assert transactions.ts_list[0].quote == 20    
 
    @patch('reno_tax_helper.parser.get_coin_value') 
    @patch('reno_tax_helper.parser.get_asset_info') 
    def test_add_transaction_fail(self, mocked_call, mocked_call2):
        mocked_call.side_effect = [self.is_crypto, self.not_crypto]
        mocked_call2.return_value = 1
        transactions = Transactions("RVN","USD")
        
        with self.assertRaises(ValueError):
            transactions.add_transaction(None,20)
        
        with self.assertRaises(ValueError):
            transactions.add_transaction(self.date,0)

if __name__ == '__main__':
    unittest.main()
