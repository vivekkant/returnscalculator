import csv
import datetime

cols={'date':'date', 'action':'action', 'stock':'stock', 'quantity':'quantity', 'price':'price'}

def map_records_file(filename, columns=cols):
    """
    This function reads a CSV file and returns a list of transaction records for processing
    The inout are as follows:
        filename - Full qualified of the input file
        columns - Optional dict field to map the CSV header columns to actual ones
    """
    with open(filepath) as csvfile:
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
