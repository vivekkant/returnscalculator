from datetime import date
from scipy.optimize import newton
from copy import deepcopy
import numpy as np

def _transactions(records, price):
    """
        This function takes in the transaction records and returns the list of transactions
        based on the exeution of trades. It uses FIFO method to match buy and sell transactions
        This is used in calculation of realized & unrealized gains and CAGR at transaction level
        It is used by the transactions function for matching transactions of a single record.
    """

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
                
                sell_tran['quantity'] =  sell_quant - buy_quant 
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


def transactions(records, prices):
    """

    This function takes in the transaction records and returns the list of transactions
    based on the exeution of trades. It uses FIFO method to match buy and sell transactions
    This is used in calculation of realized & unrealized gains and CAGR at transaction level

    INPUT
    -----
    record : A list of dictionary with the following keys
        date - Date in datetime.date format
        action - String either "Buy" and "Sell"
        stock - The stock name or symbol
        price - The buy or sell price
        quantity - The quantity of the transactions
    price : A dict with the following keys
        key - The stock name or symbol
        value - The current value of the stock

    OUTPUT
    ------
    transactions :  A list of matched transactions with each transaction is a dict
        stock - The stock name or symbol (string)
        buy_date - The buy date of the transaction (datetime.date)
        buy_price - The buy price of the transaction (float)
        sell_date - The sell date of the transaction (datetime.date)
        sell_price - The sell price of the transaction (float)
        realized - If the gains are realized (boolean) 
        quantity - The quantity of the transaction (integer)

    """

    records_by_stock = {}
    for record in records:
        stock = record['stock']
        try:
            record_list = records_by_stock[stock]
        except KeyError:
            record_list = []
            records_by_stock[stock] = record_list
        record_list.append(deepcopy(record))

    trans = []
    for stock in records_by_stock:
        stock_records = records_by_stock[stock]
        try:
            price = prices[stock]
        except KeyError:
            price = 0.0
        _trans = _transactions(stock_records, price)
        trans.extend(_trans)

    return trans


def cagr(transactions):

    """
    This function calculates the transaction level CAGR

    INPUT
    -----
    transactions :  A list of matched transactions with each transaction is a dict
        stock - The stock name or symbol (string)
        buy_date - The buy date of the transaction (datetime.date)
        buy_price - The buy price of the transaction (float)
        sell_date - The sell date of the transaction (datetime.date)
        sell_price - The sell price of the transaction (float)
        realized - If the gains are realized (boolean) 
        quantity - The quantity of the transaction (integer)    

    OUTPUT
    ------
    transactions :  The same list of transactions are enhanced with the following keys
        profit - Total profit (float)
        pnl - % profit or loss  in decimal value (float)
        duration - Duration in years (float)
        cagr - Transaction level CAGR in decimal percentage (float)

    """
    
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

def pnl(transactions):

    """
    This function calculates the total profit & loss

    INPUT
    -----
    transactions :  A list of matched transactions with each transaction is a dict
        stock - The stock name or symbol (string)
        buy_date - The buy date of the transaction (datetime.date)
        buy_price - The buy price of the transaction (float)
        sell_date - The sell date of the transaction (datetime.date)
        sell_price - The sell price of the transaction (float)
        realized - If the gains are realized (boolean) 
        quantity - The quantity of the transaction (integer)    

    OUTPUT
    ------
    pnl : A dict containing pnl for each stock
        key : Stock name or Symbol or 'TOTAL' for total P&L
        value : A dict containing the following keys for P&L values
            realized profit :  Total realized profit
            unrealized : Total realized profit
            realized_pnl : % age realized profit on investment amound
            unrealized_pnl : % age realized profit on investment amound
    """

    pnl = {}

    for tran in transactions:

        stock = tran['stock']
        try:
            stock_pnl = pnl[stock]
        except KeyError:
            stock_pnl = {}
            stock_pnl['realized'] = 0.0
            stock_pnl['unrealized'] = 0.0
            stock_pnl['realized_investment'] = 0.0
            stock_pnl['unrealized_investment'] = 0.0
            pnl[stock] = stock_pnl

        try:
            total_pnl = pnl['TOTAL']
        except KeyError:
            total_pnl = {}
            total_pnl['realized'] = 0.0
            total_pnl['unrealized'] = 0.0
            total_pnl['realized_investment'] = 0.0
            total_pnl['unrealized_investment'] = 0.0   
            pnl['TOTAL'] = total_pnl     
        
        if tran['realized']:
            stock_pnl['realized'] += tran['profit']
            stock_pnl['realized_investment'] += tran['buy_price'] * tran['quantity']
            total_pnl['realized'] += tran['profit']
            total_pnl['realized_investment'] += tran['buy_price'] * tran['quantity']
        else:
            stock_pnl['unrealized'] += tran['profit']
            stock_pnl['unrealized_investment'] += tran['buy_price'] * tran['quantity']
            total_pnl['unrealized'] += tran['profit']
            total_pnl['unrealized_investment'] += tran['buy_price'] * tran['quantity']

    for stock in pnl:
        stock_pnl = pnl[stock]
        stock_pnl['realized_pnl'] = 0.0 if stock_pnl['realized_investment'] == 0 else stock_pnl['realized'] / stock_pnl['realized_investment']
        stock_pnl['unrealized_pnl'] = 0.0 if stock_pnl['unrealized_investment'] == 0 else stock_pnl['unrealized'] / stock_pnl['unrealized_investment']

    return pnl


def cashflow(records, prices):

    """
    This function gives a cashflow based on trasaction records

    INPUT
    -----
    record : A list of dictionary with the following keys
        date - Date in datetime.date format
        action - String either "Buy" and "Sell"
        stock - The stock name or symbol
        price - The buy or sell price
        quantity - The quantity of the transactions
    prices : A dict of the current prices of stocks 

    OUTPUT
    ------
    cashflow : A dict of cashflow records with positive records on sell and 
    negetive on buy
        key : A datetime.date for the cashflow transaction
        value : Amount of transaction

    """

    quantities = {}
    cashflow = {}

    for record in records:

        stock = record['stock']
        try:
            quantity = quantities[stock]
        except KeyError:
            quantity = 0

        try:
            cashflow_item = cashflow[record['date']]
        except KeyError:
            cashflow_item = 0

        if record["action"] == 'Buy':
            quantity += record["quantity"]
            amount = -1 * record["quantity"] * record['price']
            cashflow[record['date']] = cashflow_item + amount

        elif record["action"] == 'Sell':
            quantity -= record["quantity"]
            amount = 1 * record["quantity"] * record['price']
            cashflow[record['date']] = cashflow_item + amount

        quantities[stock] = quantity

    cashflow_today = 0
    for stock in quantities:
        cashflow_today += quantities[stock] * prices[stock]

    cashflow[date.today()] = cashflow_today

    return cashflow

def _discf(rate, pmts, dates):

    dcf=[]
    for i,cf in enumerate(pmts):
        d=dates[i]-dates[0]
        dcf.append(cf*(1+rate)**(-d.days/365.))
    return np.add.reduce(dcf)

def xirr(cashflow, guess=.10):
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





