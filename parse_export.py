import csv
import datetime

def read_portfolio_file(filepath):
	with open(filepath) as csvfile:
		preader = csv.DictReader(csvfile)
		records = []
		for row in preader:
			if row.get("Investment"):
				records.append(parse_record(row))
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

def map_transactions(trans, filepath):
	csv_columns = ['stock','buy_date','buy_price','quantity','sell_date','sell_price','realized','profit','pnl','duration','cagr']
	with open(filepath, 'w') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
		writer.writeheader()
		for data in trans:
		    writer.writerow(data)
	

