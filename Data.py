from datetime import timedelta, date

def FileSortments(startDate):
    import requests
    import pandas_datareader.data as web
    import pickle
    import datetime as dt
    import bs4 as bs

    table = bs.BeautifulSoup(requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies").text, "lxml").find("table", {"class":"wikitable sortable"})
    tickers = []

    for row in table.findAll("tr")[1:]:
        ticker = row.find_all('td')[0].text
        tickers.append(ticker[:-1])

    with open("/content/Market-environment/Market_environment/datasets/sp500tickers.pickle","wb") as f:
        pickle.dump(tickers,f)

    for ticker in tickers:
        try:
            web.DataReader(ticker, "yahoo", dt.datetime(startDate.year, startDate.month, startDate.day), dt.datetime.now()).to_csv("/content/Market-environment/Market_environment/datasets/data/{}.csv".format(ticker))
        except Exception as e:
            print("Failed to read",ticker, e)

startDate = date(2017, 1, 1)
endDate = date(2020, 1, 1)

FileSortments(startDate)
