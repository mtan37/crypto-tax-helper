class Transactions:
    def __init__(self, currency=None):
        self.currency=validate_currency(currency)
        self.ts_list=[]
        self.ts_count=0

    def validate_currency(self, currency):
        """
            validate that the currency is available in coinmarket cap
        """
        #TODO use coinmarket api
        return currency

    class Transaction:
        def __init__(self, date=None, amount=0):
            self.date=validate_date(date)
            self.amount=validate_amount(amount)
        def validate_date(self, date):
            if date is None:
                raise ValueError("date value can't be None")
            
            # TODO check if can't parse date
            # TODO check if is future date

            return date
        def validate_amount(self,amount):
            #TODO validate that the amount is a decimal greater than zero 
            return amount
    def add_transaction(self, date, amount):
        ts = Transaction(date,amount)
        self.ts_list.append(ts)
        self.ts_count+=1
