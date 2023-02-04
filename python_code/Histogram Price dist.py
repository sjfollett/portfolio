from datetime import datetime
import pandas as pd
import pandas_datareader as web
import numpy as np
import matplotlib.pyplot as plt


fromDate = "09-01-2020"
toDate = datetime.today()
ticker = "SPY"

df = web.DataReader(ticker, "stooq", fromDate, toDate)
df.to_csv(f"{ticker}Data{datetime.date(toDate)}.csv")

df = pd.read_csv(f"{ticker}Data{datetime.date(toDate)}.csv", index_col="Date")
# df["Dollar Volume"] = df["Volume"]*df['Close']
# df["Volume in K shares"] = df["Volume"]/1000
# df["Return to Date"] = ((df["Close"]-df["Close"][0])/df["Close"][0])*100
df['Daily Change %'] = (df["Close"].pct_change())*100
df = df.drop(["High", "Low"], axis=1)
# df = df.sort_values(by="Daily Change %")
# df = df.sort_values(by="Daily Change %", ascending = False)
# print(df.head(20))
# print(df.tail(20))

# dfOnePercent = df[ (df["Daily Change"] > .10) | (df["Daily Change"] < -.10)]
# print(dfOnePercent.tail(120))
dfAverage = df["Close"].mean(axis=0)
dfDailyMover = df["Daily Change %"].mean(axis=0)
dfStdDev = df["Close"].std(axis=0)
dfDailyStd = df["Daily Change %"].std(axis=0)
# print( "Our Average Price:",dfAverage)
# print("Average Daily Change % (drift):", dfDailyMover)
# print("Price standard deviation:", dfStdDev)
# print("Percent change standard deviation (volatility):", dfDailyStd)


dfOne = df[["Close"]]

# dfOne.plot()
# plt.title("PLTR stock price")
# plt.xlabel("Date")
# plt.ylabel("Price")
# plt.show()

dfOne['pct'] = df["Close"].pct_change()
# print(df)

#
# dfOne['pct'].plot()
# plt.plot(dfOne.index, dfOne['pct'], color="c")
# ax = plt.axes()
# ax.set_facecolor("k")
# plt.grid(which="major", axis="both", color="lightslategrey", linestyle = "-", linewidth=".5")
# plt.title("PLTR Daily Percent Change")
# plt.xlabel("Date")
# plt.ylabel("% Change")
# plt.show()

histMean = dfOne['pct'].mean()  # drift
hisStd = dfOne['pct'].std()    # volatility

# print(hisStd, histMean)
# print(df)
todayPrice = df["Close"][0]
# print(todayPrice)

timePoints = 42
scenarios = 10000
# starting point 5000 scenarios

simulatedCurves = []
lastDayPrices = []
for scenarios in range(0, scenarios):
    simulatedprices = [todayPrice]
    monteCarloMoves = np.random.normal(histMean, hisStd, timePoints)
    # print(monteCarloMoves)
    for move in monteCarloMoves:
        previousDayPrice = simulatedprices[-1]
        nextDayPrice = previousDayPrice*(1+move)
        simulatedprices.append(nextDayPrice)
        if move == monteCarloMoves[-1]:
            lastDayPrices.append(nextDayPrice)
        else:
            continue
    simulatedCurves.append(simulatedprices)
    days = list(range(0, timePoints + 1))
    # plt.plot(days, simulatedprices)

percentile = np.percentile(simulatedCurves, 50, axis=0)
percentile2 = np.percentile(simulatedCurves, 5, axis=0)
percentile3 = np.percentile(simulatedCurves, 95, axis=0)
# plt.plot(days, percentile, "b--", label="50% confidence interval")
# plt.plot(days, percentile2, "r--", label="5% confidence interval")
# plt.plot(days, percentile3, "g--", label="95% confidence interval")
plt.hist(lastDayPrices, 50, facecolor='b', alpha=.5)

# testStart = "2021-01-01"
# testEnd = "2021-04-08"
# dfTest = web.DataReader(ticker, "yahoo", testStart, testEnd)#42 trading days
# # print(dfTest)
# dfTestPrices = dfTest["Close"].values
# plt.plot(days, dfTestPrices)
ax = plt.axes()
ax.set_facecolor("k")
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels)
plt.grid(which="major", axis="both", color="lightslategrey", linestyle="-", linewidth=".5")
plt.title(f"{ticker} 60 Day outlook price distribution (10,000 Scenarios)")
plt.xlabel("Last Day Simulated Price")
plt.ylabel("# of occurrences")
plt.show()
