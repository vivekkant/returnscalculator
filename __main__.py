import datetime
from calculator import transactions, cagr, pnl, cashflow, xirr

if __name__ == "__main__":

    records = [{'date': datetime.date(2020, 4, 27), 'action': 'Buy', 'stock': 'Bajaj Finserv Limited', 'quantity': 21.0, 'price': 4568.7286},
    {'date': datetime.date(2020, 5, 15), 'action': 'Buy', 'stock': 'Bajaj Finserv Limited', 'quantity': 3.0, 'price': 4720.35},
    {'date': datetime.date(2020, 6, 15), 'action': 'Buy', 'stock': 'Bajaj Finserv Limited', 'quantity': 2.0, 'price': 5195.0},
    {'date': datetime.date(2020, 7, 15), 'action': 'Buy', 'stock': 'Bajaj Finserv Limited', 'quantity': 2.0, 'price': 6415.325},
    {'date': datetime.date(2020, 8, 24), 'action': 'Sell', 'stock': 'Bajaj Finserv Limited', 'quantity': 10.0, 'price': 6420.049},
    {'date': datetime.date(2020, 9, 1), 'action': 'Sell', 'stock': 'Bajaj Finserv Limited', 'quantity': 5.0, 'price': 6640.8},
    {'date': datetime.date(2020, 9, 24), 'action': 'Buy', 'stock': 'Bajaj Finserv Limited', 'quantity': 10.0, 'price': 5420.05},
    {'date': datetime.date(2020, 12, 2), 'action': 'Buy', 'stock': 'Bajaj Finserv Limited', 'quantity': 2.0, 'price': 8739.25},
    {'date': datetime.date(2020, 12, 16), 'action': 'Buy', 'stock': 'Bajaj Finserv Limited', 'quantity': 1.0, 'price': 9325.0},
    {'date': datetime.date(2020, 12, 21), 'action': 'Buy', 'stock': 'Bajaj Finserv Limited', 'quantity': 5.0, 'price': 8870.75},
    {'date': datetime.date(2021, 1, 18), 'action': 'Buy', 'stock': 'Bajaj Finserv Limited', 'quantity': 1.0, 'price': 8362.55}]

    trans = transactions(records, 10220.05)
    trans = cagr(trans)

    print("--------------- Transaction wise CAGR ---------------")
    for tran in trans:
    	print(tran)

    print("--------------- Total P&L ---------------")
    realized, unrealized, realized_pnl, unrealized_pnl = pnl(trans)
    print("Realized Profit Amount = ", realized)
    print("Unrealized Profit Amount = ", unrealized)
    print("Realized Percent Percentage = ", realized_pnl)
    print("Unrealized Profit Percentage = ", unrealized_pnl)

    cashflow = cashflow(records, 10220.05)
    print("--------------- Cashflow ---------------")
    for tran in cashflow:
    	print(tran, cashflow[tran])
    print(cashflow)

    xirr = xirr(cashflow)
    print("--------------- XIRR ---------------")
    print("XIRR = ", xirr)


