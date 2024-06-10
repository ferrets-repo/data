import pandas as pd
import numpy as np

df = pd.read_csv('fred_series.csv', index_col=0)

# Print a specific row based on index
# print(df.iloc[[0]])

# Iterate row by row in a dataframe
# for index, row in df.iterrows():
#     print(row)

# Transpose the dataframe: Row -> Column
dft = df.T

for column in dft:
    df_temp = dft[column].copy()
    df_temp.columns = ["Maturity", "Yield"]
    print(df_temp)