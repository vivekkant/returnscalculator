import csv
import os
import datetime

records_cols={'date':'date', 'action':'action', 'stock':'stock', 'quantity':'quantity', 'price':'price'}
prices_cols={'stock':'stock', 'price':'price'}

def parse_records_file(filename, columns=records_cols):
    """
    This function reads a CSV file and returns a list of transaction records for processing
    The inout are as follows:
        filename - Full qualified of the input file
        columns - Optional dict field to map the CSV header columns to actual ones
    """
    with open(filename) as csvfile:
        preader = csv.DictReader(csvfile)
        records = []
        for row in preader:
            record = {}
            record['date'] = row.get(columns['date'])
            record['action'] = row.get(columns['action'])
            record['stock'] = row.get(columns['stock'])
            record['quantity'] = row.get(columns['quantity'])
            record['price'] = row.get(columns['price'])
            records.append(record)
        return records

def parse_prices_file(filename, columns=prices_cols):
    """
    This function reads a CSV file and returns a list of price records
    The inout are as follows:
        filename - Full qualified of the input file
        columns - Optional dict field to map the CSV header columns to actual ones
    """
    with open(filename) as csvfile:
        preader = csv.DictReader(csvfile)
        prices = {}
        for row in preader:
            prices[row.get(columns['stock'])] = float(row.get(columns['price']))
        return prices

def map_transactions_file(transactions, filepath):
    """
    This function take the mapped transactions at transaction level
    and maps into a CSV file.
    The inout are as follows:
        transactons - A list of transactions with each dict of following keys
            stock - The stock name or symbol (string)
            buy_date - The buy date of the transaction (datetime.date)
            buy_price - The buy price of the transaction (float)
            sell_date - The sell date of the transaction (datetime.date)
            sell_price - The sell price of the transaction (float)
            realized - If the gains are realized (boolean) 
            quantity - The quantity of the transaction (integer)
        filepath - Full qualified of the input file
    """
    csv_columns = ['stock','buy_date','buy_price','sell_date','sell_price','realized','quantity']
    with open(filepath, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in transactions:
            writer.writerow(data)


def map_cagr_transactions_file(transactions, filepath):
    """
    This function take the mapped transactions with CAGR calcualtion at transaction level
    and maps into a CSV file.
    The inout are as follows:
        transactons - A list of transactions with each dict of following keys
            stock - The stock name or symbol (string)
            buy_date - The buy date of the transaction (datetime.date)
            buy_price - The buy price of the transaction (float)
            sell_date - The sell date of the transaction (datetime.date)
            sell_price - The sell price of the transaction (float)
            realized - If the gains are realized (boolean) 
            quantity - The quantity of the transaction (integer)
            profit - Total profit (float)
            pnl - % profit or loss  in decimal value (float)
            duration - Duration in years (float)
            cagr - Transaction level CAGR in decimal percentage (float)
        filepath - Full qualified of the input file
    """
    csv_columns = ['stock','buy_date','buy_price','sell_date','sell_price','realized','quantity','profit','pnl','duration','cagr']
    with open(filepath, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in transactions:
            writer.writerow(data)

def map_pnl(pnl, filepath):
    """
    This transaction maps the pnl for each fo ths stocks
    """
    csv_columns = ['stock','realized','realized_investment','realized_pnl','unrealized','unrealized_investment','unrealized_pnl']
    with open(filepath, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        total_pnl = pnl.pop('TOTAL')
        total_pnl['stock'] = 'TOTAL'
        for stock in pnl:
            stock_pnl = pnl[stock]
            stock_pnl['stock'] = str(stock)
            writer.writerow(stock_pnl)
        writer.writerow(total_pnl)


def map_cashflows(cashflow, filepath):
    """
    This function takes the cashflow and maps into a CSV file
    """
    csv_columns = ['date','cashflow']
    with open(filepath, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for tran in cashflow:
            item = {'date':tran, 'cashflow':cashflow[tran]}
            writer.writerow(item)
    

def list_csv_files(filepath):
    filelist = []
    for parent_folder_path in os.listdir(filepath):
        parent_folder = os.path.join(filepath, parent_folder_path)
        if os.path.isdir(parent_folder):
            for csv_file_path in os.listdir(parent_folder):
                csv_file = os.path.join(parent_folder, csv_file_path)
                filelist.append(csv_file)
    return filelist




