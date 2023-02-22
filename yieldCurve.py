from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import date
import matplotlib.pyplot as plt

def getData(year):
    try:
        url = f"https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value={year}"
        webTable = pd.read_html(url)
        df = webTable[0]
        df = df.drop(df.columns[[1, 2, 3, 4, 5, 6, 7, 8, 9]], axis=1) #this columns are "included" in the table, but they are invisible and carry no data
        return df
    except:
        print(f"error: failed to get yield data for {year}")


def chartRates(years, dataPoints):
    currentYear = date.today().year
    yieldTables = []
    for i in range (0,years):
        df = getData(currentYear-i)
        yieldTables.append(df)
    yieldTables.reverse()
    ratesTable = pd.concat(yieldTables, ignore_index=True)
    #print(ratesTable.to_string())

    rowNum = len(ratesTable.index) - 1
    interval = rowNum // (dataPoints-1)
    plotData = []

    while rowNum>=0:
        #print(list(ratesTable.loc[rowNum, :]))
        plotData.append(list(ratesTable.loc[rowNum, :]))
        rowNum = rowNum - interval
    dfColumns = list(ratesTable.columns)
    plotDf = pd.DataFrame(plotData, columns=dfColumns)
    #print(plotDf.to_string())
    dates = list(plotDf["Date"])
    plotDf = plotDf.drop("Date", axis=1)
    #print(plotDf.to_string())
    rows = len(plotDf.index)
    ctr = 0
    while ctr < rows:
        plt.plot(plotDf.loc[ctr, :], label= dates[ctr])
        ctr += 1
    leg = plt.legend(loc='best')
    plt.show()


if __name__ == '__main__':
    years = 2       #how many years would you like to look back
    yieldCurvesToChart = 4  #how many yield curves would you like to plot (spread evenly across the given number of years)
    chartRates(years, yieldCurvesToChart)
