import csv
import os
import datetime

def parse_portfolio_file(filename):
    """
    This function will parse a portfolio output file
    """
    with open(filename) as csvfile:

        preader = csv.DictReader(csvfile)
        cost = 0.0
        value = 0.0
        cost_str = None
        value_str = None

        for row in preader:
            record = {}
            record['Symbol'] = row.get('Symbol')
            if row.get('Symbol') is None or row.get('Symbol') is '':
                cost_str = row.get('Cost basis')
                value_str = row.get('Total')

        if cost_str is not None and cost_str is not '' and value_str is not None and value_str is not '':
           cost = float(cost_str)
           value = float(value_str)

        return cost, value

def get_portfolio_summary(csvfile):
    """
    This function takes a CSV file, parses the file to return a dict of
    summary values.
    """
    
    summary = {}
    
    filename = os.path.basename(csvfile)
    summary["filename"] = filename

    foldername = os.path.basename(os.path.dirname(csvfile))
    date = datetime.datetime.strptime(foldername, "%Y-%m-%d").date()
    summary["date"] = date

    cost, value = parse_portfolio_file(csvfile)
    summary["cost"] = cost
    summary["value"] = value

    return summary


def map_portfolio_summary(filelist, summary_folder):
    """
    This function take the list of porfolio files and
    and maps into a CSV file.
    The inout are as follows:
        filelist - A list of portfolio files.
        summary_folder - Full qualified path of folder where summary files will
        be created.
    """

    portfolio_updates = {}

    for csvfile in filelist:
        summary = get_portfolio_summary(csvfile)
        filename = summary['filename']
        try:
            file_summary = portfolio_updates[filename]
        except KeyError:
            file_summary = []
        file_summary.append(summary)
        portfolio_updates[filename] = file_summary

    for filename in portfolio_updates:
        
        print('Writing file....', filename)
        file_summary = portfolio_updates[filename]
        summaryfile = os.path.join(summary_folder, filename)

        csv_columns = ['filename','date','cost','value']
        with open(summaryfile, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in file_summary:
                writer.writerow(data)            







