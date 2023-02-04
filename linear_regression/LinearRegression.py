from datetime import datetime
from sklearn import linear_model
from sklearn.metrics import r2_score
import pandas as pd
import matplotlib.pyplot as plt

def GenerateYs(Xs, m, b):
    result = []
    for x in Xs:
        y = m*x + b
        result.append(y)

    return result


oil = pd.read_csv("oilPrices-1.csv", index_col="Date", parse_dates=True)
rub = pd.read_csv("usdPrices-1.csv", index_col="Date", parse_dates=True)

trainStartDate = datetime(2014,9,1)
trainEndDate = datetime(2016,7,1)

testStartDate = datetime(2016,7,1)
testEndDate = datetime(2018,8,1)

join = oil.join(rub, rsuffix="UsdRub", how="inner")
joinTrain = join[(join.index>trainStartDate) & (join.index<trainEndDate)]
joinTest = join[(join.index>testStartDate) & (join.index<testEndDate)]

Xtrain = joinTrain["Price"].values       #price of oil in USD
Ytrain = joinTrain["PriceUsdRub"].values #price of USD in rubles

Xtest = joinTest["Price"].values       #price of oil in USD
Ytest = joinTest["PriceUsdRub"].values #price of USD in rubles

linReg = linear_model.LinearRegression()

Xtrain = Xtrain.reshape(len(Xtrain), 1)
Ytrain = Ytrain.reshape(len(Ytrain), 1)

Xtest = Xtest.reshape(len(Xtest), 1)
Ytest = Ytest.reshape(len(Ytest), 1)

linReg.fit(Xtrain, Ytrain)
YpredictedSk = linReg.predict(Xtest)

r2easy = r2_score(Ytest, YpredictedSk)
print("Our calculated coffs m:{} and b:{} and our r2 is {}".format(linReg.coef_,linReg.intercept_, r2easy))

Ycalculated = GenerateYs(Xtest, linReg.coef_[0][0], linReg.intercept_[0])
plt.plot(Xtest, Ycalculated, "k-", label=f'y={float(linReg.coef_):.2f} x+{float(linReg.intercept_):.2f}, '
                                          f'r2={float(r2easy):.2f}')  # calculated based on trained data
plt.legend()
plt.scatter(Xtest, Ytest, c="darkred")  # real observed data
plt.title("Oil Price to USD/RUB FX")
plt.xlabel("Price of Oil in USD")
plt.ylabel("Price of Dollar in Rubles")
plt.show()