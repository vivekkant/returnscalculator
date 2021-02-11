import datetime

def get_transactions(records, price):
	records = sorted(records, key = lambda i: i['date'], reverse=True)
	buy = []
	sell = []
	trans = []
	for record in records:
		action = record["action"]
		if action == 'Buy':
			buy.append(record)
		elif action == 'Sell':
			sell.append(record)

	while len(buy) > 0:
		
		buy_tran = buy.pop()
		
		tran = {}
		tran['stock'] = buy_tran['stock']
		tran['buy_date'] = buy_tran['date']
		tran['buy_price'] = buy_tran['price']

		if len(sell) > 0:	
			sell_tran = sell.pop()

			buy_quant = buy_tran['quantity']
			sell_quant = sell_tran['quantity']

			tran['sell_date'] = sell_tran['date']
			tran['sell_price'] = sell_tran['price']
			
			if buy_quant > sell_quant:
				
				tran['quantity'] = sell_quant


				buy_tran['quantity'] = buy_quant - sell_quant
				buy.append(buy_tran)

			elif sell_quant > buy_quant:

				tran['quantity'] = buy_quant	
				
				sell_tran['quantity'] =  sell_quant	- buy_quant	
				sell.append(buy_tran)
			
			else:

				tran['quantity'] = buy_quant
			
		else:
			tran['sell_date'] = datetime.date.today()
			tran['sell_price'] = price
			tran['quantity'] = buy_tran['quantity']


		trans.append(tran)
		print(tran)

	return trans

def xirr_calculator(records, price):
	trans = get_transactions(records, price)
	return trans



