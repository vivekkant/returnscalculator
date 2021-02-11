from parse_export import read_portfolio_file, map_transactions
from calculator import xirr_calculator

filepath = "/Users/vivekkant/temp/xirr/trans.csv"
records = read_portfolio_file(filepath)
trans = xirr_calculator(records, 10220.05)
map_transactions(trans, "/Users/vivekkant/temp/xirr/trans2.csv")

