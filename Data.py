from datetime import timedelta, date

def FileSortments(startDate):
    import requests
    import pandas_datareader.data as web
    import pickle
    import datetime as dt
    import bs4 as bs
    import os
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--stockAmount", required=False, default=500)
    args = vars(ap.parse_args())
    stockAmount = int(args["stockAmount"])

    table = bs.BeautifulSoup(requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies").text, "lxml").find("table", {"class":"wikitable sortable"})
    tickers = []

    for row in table.findAll("tr")[1:]:
        ticker = row.find_all('td')[0].text
        tickers.append(ticker[:-1])

    with open("/content/Market-environment/Market_environment/datasets/sp500tickers.pickle","wb") as f:
        pickle.dump(tickers,f)

    os.mkdir("/content/Market-environment/Market_environment/datasets/data/")

    for ticker in tickers[:stockAmount]:
        try:
            web.DataReader(ticker, "yahoo", dt.datetime(startDate.year, startDate.month, startDate.day), dt.datetime.now()).to_csv("/content/Market-environment/Market_environment/datasets/data/{}.csv".format(ticker))
        except Exception as e:
            print("Failed to read",ticker, e)

startDate = date(2017, 1, 1)

FileSortments(startDate)
