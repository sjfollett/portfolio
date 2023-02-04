import numpy as np
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, roc_curve, roc_auc_score
from sklearn.metrics import classification_report
import sklearn.metrics


def printOutTheCoefficients(params, coeffecients, intercept):
    tParams = params[np.newaxis].T
    tCoeffs = coeffecients.T
    total = np.concatenate([tParams, tCoeffs], axis=1)
    totalDF = pd.DataFrame(data=total)
    totalDF.to_excel("modelOutput.xlsx")
    print(totalDF)


columnWIV = ["recoveries",
             "creditScore",
             "total_rec_late_fee",
             "term",
             "annual_inc",
             "revol_util",
             "creditPurpose",
             "dti",
             "inq_last_6mths",
             "default_ind"]

df = pd.read_csv("Data/150K.csv", skipinitialspace=True, usecols=columnWIV)
# print(df.head())
# df.to_csv("checkSelectedData.csv")

df["revol_util"] = df["revol_util"].fillna(100)  # conservative value
# print(df.head())

purpose = pd.get_dummies(df["creditPurpose"])
# print(purpose.head())
df.drop("creditPurpose", axis=1, inplace=True)
dfReady = pd.concat([df, purpose], axis=1)
# print(dfReady.head())

# Mnx + Mn2X2 + ..... + b

dfResults = dfReady["default_ind"]
dfInputs = dfReady.drop("default_ind", axis=1)

inputsTrain, inputsTest, resultTrain, resultTest = train_test_split(dfInputs, dfResults, test_size=0.3, random_state=1)
# 70/30 or 75/25 size. tests 30 percent of population against 70

# LogReg = LogisticRegression(solver="liblinear", max_iter=200000)
LogReg = LogisticRegression(max_iter=200000)
LogReg.fit(inputsTrain, resultTrain)

# print("Coefs(Mns):", LogReg.coef_)
# print("Intercept(b)", LogReg.intercept_)

printOutTheCoefficients(dfInputs.columns.values, LogReg.coef_, LogReg.intercept_)

resultsPred = LogReg.predict(inputsTest)

print(confusion_matrix(resultTest, resultsPred))
print(classification_report(resultTest, resultsPred))
