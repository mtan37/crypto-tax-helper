import unittest
from unittest.mock import patch, call, Mock
import reno_tax_helper.manager as m
class TestCalculation(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        self.ts = Mock()
        self.ts.ts_list=[]
        
        amount = 1
        quote = 2
        while amount < 7:
            t = Mock()
            t.amount = amount
            t.quote = quote
            self.ts.ts_list.append(t)   
            amount += 1 
            quote +=2   
 
    @classmethod
    def tearDownClass(self):
        pass

    def test_calculate_total_quote(self):
        assert m.calculateTotalQuoteAmount(self.ts) == 42

    def test_calculate_total_amount(self):
        assert m.calculateTotalAmount(self.ts) == 21
