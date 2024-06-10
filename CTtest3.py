import os
import requests
import pandas as pd
import time
import datetime
import pandas as pd
from datetime import date
from fredapi import Fred

fred_key = 'e1ed8f4fb579f8537d1d1d263f4708b8'
ids = ['DGS1MO', 'DGS3MO', 'DGS6MO', 'DGS1', 'DGS2', 'DGS3', 'DGS5', 'DGS7', 'DGS10', 'DGS20', 'DGS30']
freq = 'd'
fred = Fred(api_key=fred_key)

# Initialize an empty DataFrame with the appropriate date index
combined_df = pd.DataFrame()

# Mapping series_id to number of months for column names
maturity_mapping = {
    'DGS1MO': '1M', 'DGS3MO': '3M', 'DGS6MO': '6M',
    'DGS1': '1Y', 'DGS2': '2Y', 'DGS3': '3Y',
    'DGS5': '5Y', 'DGS7': '7Y', 'DGS10': '10Y',
    'DGS20': '20Y', 'DGS30': '30Y'
}

for series_id in ids:
    # Get the series data from FRED
    series_data = fred.get_series(series_id)
   
    # Convert the series to a DataFrame
    df = series_data.to_frame(name=series_id)
   
    # Rename the column to match the maturity mapping
    df.rename(columns={series_id: maturity_mapping[series_id]}, inplace=True)
   
    # Join the series data with the combined DataFrame
    combined_df = combined_df.join(df, how='outer')

# Drop data rows where NaN value exists
clean_df = combined_df.dropna()
print(clean_df)
