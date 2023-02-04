import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import openpyxl
import RealLogRegressions.WOE as woe

# from logRegression.logRegressionL2.helperFiles.WOE import data_vars


dropColsHC = [
# 'funded_amnt',
# 'funded_amnt_inv',
# 'installment',
# 'total_pymnt',
# 'out_prncp_inv',
# 'total_pymnt_inv',
# 'total_rec_prncp',
# 'total_rec_int',
# 'last_pymnt_amnt',
# 'collection_recovery_fee',
# 'total_acc',"delinq_2yrs"
]

df = pd.read_csv("Data/150K.csv", skipinitialspace=True)
df = df.drop(dropColsHC, axis=1)
correlation = df.corr()
finalIV, IV = woe.data_vars(df, df["default_ind"])
IV.to_excel("IVOutput.xlsx")

# print(correlation.head())
# correlation.to_excel("Correlation.xlsx")

sb.heatmap(correlation)
plt.show()

