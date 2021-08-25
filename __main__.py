import datetime
from calculator import transactions, cagr, pnl, cashflow, xirr
from fileio import list_csv_files
from trendanalyzer import get_portfolio_summary,parse_portfolio_file, map_portfolio_summary

if __name__ == "__main__":

    """
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
    {'date': datetime.date(2021, 1, 18), 'action': 'Buy', 'stock': 'Bajaj Finserv Limited', 'quantity': 1.0, 'price': 8362.55},
    {'date': datetime.date(2020, 2, 20), 'action': 'Buy', 'stock': 'Avenue Supermarkets Limited', 'quantity': 3.0, 'price': 2472.0000},
    {'date': datetime.date(2020, 3, 16), 'action': 'Buy', 'stock': 'Avenue Supermarkets Limited', 'quantity': 4.0, 'price': 2012.0000},
    {'date': datetime.date(2020, 5, 14), 'action': 'Sell', 'stock': 'Avenue Supermarkets Limited', 'quantity': 4.0, 'price': 2345.9000}]

    prices = {'Bajaj Finserv Limited': 10200.50, 'Avenue Supermarkets Limited': 3151.95}

    trans = transactions(records, prices)

    print("--------------- Matched transactions ---------------")
    for tran in trans:
        print(tran)


    trans = cagr(trans)

    print("--------------- Transaction wise CAGR ---------------")
    for tran in trans:
    	print(tran)


    print("--------------- Total P&L ---------------")
    pnl= pnl(trans)
    print(pnl)

   
    cashflow = cashflow(records, prices)
    print("--------------- Cashflow ---------------")
    for tran in cashflow:
    	print(tran, cashflow[tran])
    print(cashflow)


    xirr = xirr(cashflow)
    print("--------------- XIRR ---------------")
    print("XIRR = ", xirr)
    """

    filepath = '/Users/vivekkant/Dropbox/Account/Portfolio/VK/portfolio-out'
    summaryfile = '/Users/vivekkant/temp/portfolio'
    
    filelist = list_csv_files(filepath)
    for csvfile in filelist:
        print(get_portfolio_summary(csvfile))

    print('Creating a summary file...')
    map_portfolio_summary(filelist, summaryfile)
        




