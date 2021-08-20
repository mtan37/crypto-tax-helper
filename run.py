import sys
import argparse
import os 
from reno_tax_helper.parser import process_file
from reno_tax_helper.manager import calculateTotalQuoteAmount, calculateTotalAmount

def main():
    # Check version
    if sys.version_info[0] < 3:
        raise Exception("Pleas use Python 3")

    if os.getenv('COIN_API_KEY',"") == "":
        raise Exception("Pleas set COIN_API_KEY")

    # Process command argument
    parser = argparse.ArgumentParser()
    parser.add_argument('csv_path', type=str,
                        help='File path to transactions csv file')
    parser.add_argument('crypto_symbol', type=str,
                        help='Symbol of the crypo involved in the transaction')
    parser.add_argument('quote_symbol', type=str,
                        help='Symbol of the currency you want to translate to')
    parser.add_argument('amount_column_index', type=int,
                        help='Index of the csv column that indicate the amount of crypto in a single transaction')
    parser.add_argument('date_column_index', type=int,
                        help='Index of the csv column that indicate the date of the transaction')
    parser.add_argument('--header', action='store_true',
                        help='Indicate whether the csv file contains a header')

    args = parser.parse_args()
   
    ts = process_file(args.csv_path, args.crypto_symbol, args.quote_symbol, args.header, args.date_column_index, args.amount_column_index)
    quote_amount = calculateTotalQuoteAmount(ts)
    crypto_amount = calculateTotalAmount(ts)
    
    print("Total quote amount in ", args.quote_symbol, ": ", quote_amount)
    print("Total crypto amount in ", args.crypto_symbol, ": ", crypto_amount)
    
if __name__ == "__main__":
    main()
