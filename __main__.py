from parse_export import read_portfolio_file, map_transactions
from calculator import get_transactions, cagr_calculator, pnl_calculator, get_cashflow, get_xirr

filepath = "/Users/vivekkant/temp/xirr/trans.csv"
records = read_portfolio_file(filepath)

trans = get_transactions(records, 10220.05)
trans = cagr_calculator(trans)

print("--------------- Transaction wise CAGR ---------------")
for tran in trans:
	print(tran)

print("--------------- Total P&L ---------------")
realized, unrealized, realized_pnl, unrealized_pnl = pnl_calculator(trans)
print("Realized Profit Amount = ", realized)
print("Unrealized Profit Amount = ", unrealized)
print("Realized Percent Percentage = ", realized_pnl)
print("Unrealized Profit Percentage = ", unrealized_pnl)

cashflow = get_cashflow(records, 10220.05)
print("--------------- Cashflow ---------------")
for tran in cashflow:
	print(tran, cashflow[tran])
print(cashflow)

xirr = get_xirr(cashflow)
print("--------------- XIRR ---------------")
print("XIRR = ", xirr)

map_transactions(trans, "/Users/vivekkant/temp/xirr/trans2.csv")

