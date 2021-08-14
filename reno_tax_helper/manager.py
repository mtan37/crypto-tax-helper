def calculateTotalQuoteAmount(ts=None):
    """
        calculate the total quote price of a list of transactions
    """
    total = 0
    for t in ts.ts_list:    
        total += t.quote
    return total

def calculateTotalAmount(ts=None):
    """
        calculate the total amount of crypt coin of a list of transactions
    """
    total = 0
    for t in ts.ts_list:    
        total += t.amount
    
    return total

def outputAssetSheet(ts=None):
    pass 
