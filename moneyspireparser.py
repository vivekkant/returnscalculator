import csv
import datetime

def read_records_file(filepath):
    with open(filepath) as csvfile:
        preader = csv.DictReader(csvfile)
        records = []
        for row in preader:
            if row.get("Investment"):
                clean_record = parse_record(row)
                if clean_record is not None:
                    records.append(clean_record)
        return records

def parse_record(record):
    clean_record = {}
    date_str = record["Date"]
    date_obj = datetime.datetime.strptime(date_str, '%d/%m/%Y')
    clean_record["date"] = date_obj.date()

    clean_record["action"] = record["Action"]

    investment = record["Investment"]
    stock = investment.split(':')[0].strip()
    clean_record["stock"] = stock

    quantity_str = investment.split(':')[1].split("@")[0].strip()
    quantity = float(quantity_str)
    clean_record["quantity"] = quantity

    price_str = investment.split(':')[1].split("@")[1].strip()
    price = float(price_str)
    clean_record["price"] = price

    return clean_record

def map_record(records, filepath):
    csv_columns = ['date','action','stock','quantity','price']
    with open(filepath, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in trans:
            writer.writerow(data)
