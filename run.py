import sys
import argparse
from reno_tax_helper.manager import TransactionManager

def main():
    # Check version
    if sys.version_info[0] < 3:
        raise Exception("Pleas use Python 3")

    # Process command argument
    parser = argparse.ArgumentParser()
    parser.add_argument('csv_path', type=str,
                        help='File path to transactions csv file')
    parser.add_argument('amount_column_index', type=int,
                        help='Index of the csv column that indicate the amount of crypto in a single transaction')
    parser.add_argument('date_column_index', type=int,
                        help='Index of the csv column that indicate the date of the transaction')
    parser.add_argument('--header', action='store_true',
                        help='Indicate whether the csv file contains a header')

    args = parser.parse_args()
    
    manager = TransactionManager(args.csv_path, args.header, args.date_column_index, args.amount_column_index)
    crypto_amount = manager.getTotalAmount()
    quote_amount = manager.getTotalFiatAmount()

    print(f"total crypto amount is {crypto_amount}")
    print(f"total fiat currency amount is {quote_amount}")
    """
    for transaction in manager.transaction_list:
        print(f"transaction date: {transaction.date}")
        print(f"transaction amount: {transaction.amount}")
        print(f"transaction fiat amount: {transaction.fiat_amount}")
        print(" ")
    """
    
if __name__ == "__main__":
    main()
