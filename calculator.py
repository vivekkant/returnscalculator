from datetime import date
from scipy.optimize import newton
import numpy as np

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
			tran['realized'] = True
			
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
			tran['sell_date'] = date.today()
			tran['sell_price'] = price
			tran['quantity'] = buy_tran['quantity']
			tran['realized'] = False


		trans.append(tran)

	return trans

def cagr_calculator(transactions):
	
	for tran in transactions:
		profit = tran['quantity'] * (tran['sell_price'] - tran['buy_price'])
		pnl = profit / (tran['quantity'] * tran['buy_price'])
		duration = ((tran['sell_date'] - tran['buy_date']).days)/365
		cagr = ((tran['sell_price'] / tran['buy_price']) ** (1 / duration)) - 1

		tran['profit'] = profit
		tran['pnl'] = pnl
		tran['duration'] = duration
		tran['cagr'] = cagr

	return transactions

def pnl_calculator(transactions):

	realized = 0
	unrealized = 0
	realized_investment = 0
	unrealized_investment = 0

	for tran in transactions:
		
		if tran['realized']:
			realized += tran['profit']
			realized_investment += tran['buy_price'] * tran['quantity']
		else:
			unrealized += tran['profit']
			unrealized_investment += tran['buy_price'] * tran['quantity']

	realized_pnl = realized / realized_investment
	unrealized_pnl = unrealized / unrealized_investment

	return realized, unrealized, realized_pnl, unrealized_pnl

def get_cashflow(records, price):

	quantity = 0
	cashflow = {}

	for record in records:

		if record["action"] == 'Buy':
			quantity += record["quantity"]
			cashflow[record['date']] = -1 * record["quantity"] * record['price']

		elif record["action"] == 'Sell':
			quantity -= record["quantity"]
			cashflow[record['date']] = 1 * record["quantity"] * record['price']

	cashflow[date.today()] = quantity * price

	return cashflow

def _discf(rate, pmts, dates):

    dcf=[]
    for i,cf in enumerate(pmts):
        d=dates[i]-dates[0]
        dcf.append(cf*(1+rate)**(-d.days/365.))
    return np.add.reduce(dcf)

def get_xirr(cashflow, guess=.10):
    '''
    IRR function that accepts irregularly spaced cash flows

    Parameters
    ----------
    values: array_like
          Contains the cash flows including the initial investment
    dates: array_like
          Contains the dates of payments as in the form (year, month, day)

    Returns: Float
          Internal Rate of Return

    Notes
    ----------
    In general the xirr is the solution to

    .. math:: \sum_{t=0}^M{\frac{v_t}{(1+xirr)^{(date_t-date_0)/365}}} = 0

    '''

    dates = list(cashflow.keys())
    pmts = cashflow.values()


    f = lambda x: _discf(x, pmts, dates)

    return newton(f, guess)





