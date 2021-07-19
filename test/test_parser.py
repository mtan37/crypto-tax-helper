import unittest
from renotaxhelper import parser

class TestTransactionData(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        pass
    
    @classmethod
    def tearDownClass(self):
        pass
    
    def test_create_transactions_fail_empty(self):
        with self.assertRaises(ValueError):
            transactions = parser.Transactions()  
        
        with self.assertRaises(ValueError):
            transactions = parser.Transactions("")  
    
    def test_create_transactions_fail_not_exist_symbol(self):
        pass#TODO


if __name__ == '__main__':
    unittest.main()
