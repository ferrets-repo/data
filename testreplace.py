import pandas as pd

# Create main dataframe with 'maturity' and 'value' column names but leave it empty
data_df_main = pd.read_csv('fred_table.csv')
print (data_df_main)

# data_df_main['maturity'].replace({'DSG1MO': 1, 'DSG3MO': 3, 'DSG6MO': 6}, inplace=True)
data_df_main['maturity'] = data_df_main['maturity'].map({'DGS1MO': 1, 'DGS3MO': 3, 'DGS6MO': 6, 'DGS1': 12, 'DGS2': 24, 'DGS3': 36, 'DGS5': 60, 'DGS7': 84, 'DGS10': 120, 'DGS20': 240, 'DGS30': 360 })
# data_df_main['maturity'] = data_df_main['maturity'].astype('int')
data_df_main['maturity'] = pd.to_numeric(data_df_main['maturity'], errors='coerce')
print (data_df_main)
