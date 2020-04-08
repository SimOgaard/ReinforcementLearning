def FileSortments():
    import requests
    import pandas_datareader.data as web
    import pickle
    import datetime as dt
    import bs4 as bs
    import os
    import argparse
    from datetime import date

    def mkdate(datestring):
        return dt.datetime.strptime(datestring, '%Y-%m-%d').date()

    ap = argparse.ArgumentParser()
    ap.add_argument("-sa", "--stockAmount", required=False, default=500)
    ap.add_argument("-sd", "--startDate", type=mkdate, required=False, default=date(2017, 1, 1))
    args = vars(ap.parse_args())
    stockAmount = int(args["stockAmount"])
    startDate = args["startDate"]

    table = bs.BeautifulSoup(requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies").text, "lxml").find("table", {"class":"wikitable sortable"})
    tickers = []

    for row in table.findAll("tr")[1:]:
        ticker = row.find_all('td')[0].text
        tickers.append(ticker[:-1])

    with open("/content/ReinforcementLearning/DataMarket/sp500tickers.pickle","wb") as f:
        pickle.dump(tickers,f)

    if not os.path.exists("/content/ReinforcementLearning/DataMarket/data/"):
        os.mkdir("/content/ReinforcementLearning/DataMarket/data/")

    for ticker in tickers[:stockAmount]:
        try:
            web.DataReader(ticker, "yahoo", dt.datetime(startDate.year, startDate.month, startDate.day), dt.datetime.now()).to_csv("/content/ReinforcementLearning/DataMarket/data/{}.csv".format(ticker))
        except Exception as e:
            print("Failed to read",ticker, e)

FileSortments()
