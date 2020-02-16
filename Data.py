from datetime import timedelta, date

def FileSortments(startDate):
    import requests
    import pandas_datareader.data as web
    import os
    import pickle
    import datetime as dt
    import bs4 as bs

    if not os.path.exists("csv"):
        os.makedirs("csv")

    table = bs.BeautifulSoup(requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies").text, "lxml").find("table", {"class":"wikitable sortable"})
    tickers = []

    for row in table.findAll("tr")[1:]:
        ticker = row.find_all('td')[0].text
        tickers.append(ticker[:-1])

    with open("Market_environment/datasets/sp500tickers.pickle","wb") as f:
        pickle.dump(tickers,f)

    for ticker in tickers:
        try:
            web.DataReader(ticker, "yahoo", dt.datetime(startDate.year, startDate.month, startDate.day), dt.datetime.now()).to_csv("Market_environment/datasets/data/{}.csv".format(ticker))
        except Exception as e:
            print("Failed to read",ticker, e)

def DateRange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

startDate = date(2017, 1, 1)
endDate = date(2020, 2, 1)

FileSortments(startDate)