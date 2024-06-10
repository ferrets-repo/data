import os
import requests
import pandas as pd
import time
import datetime
import pandas as pd
from datetime import date
import numpy as np
from scipy.optimize import fmin


def fetch_fred_data(series_id, start_date, end_date):
    api_key = 'e1ed8f4fb579f8537d1d1d263f4708b8'  # Replace with your API key
    base_url = 'https://api.stlouisfed.org/fred/'
    obs_endpoint = 'series/observations'

    obs_params = {
        'series_id': series_id,
        'api_key': api_key,
        'file_type': 'json',
        'observation_start': start_date,
        'observation_end': end_date,
        'frequency': 'd',
        'units': 'lin'
    }

    response = requests.get(base_url + obs_endpoint, params=obs_params)
   
    if response.status_code == 200:
        data = response.json().get('observations', [])
        return pd.DataFrame(data)
    else:
        print(f"Failed to fetch data for series_id {series_id}: {response.status_code}")
        return pd.DataFrame()

# List of series IDs
series_ids = ['DGS1MO', 'DGS3MO', 'DGS6MO', 'DGS1', 'DGS2', 'DGS3', 'DGS5', 'DGS7', 'DGS10', 'DGS20', 'DGS30']

# List of dates
# dates = ['2024-05-01', '2024-05-02', '2024-05-03']  # Add as many dates as needed

# Define the start date
start_date = '2024-05-23'

# Get today's date
# end_date = date.today().strftime('%Y-%m-%d')
end_date = '2024-05-23'

# Generate the date range
dates = pd.date_range(start=start_date, end=end_date).strftime('%Y-%m-%d').tolist()

# Create an empty DataFrame with dates as index and series IDs (or maturities) as columns
data_df_main = pd.DataFrame(index=dates, columns=series_ids)

# Loop over each date and each series ID to fetch data
for date in dates:
    for series_id in series_ids:
        data_df_temp = fetch_fred_data(series_id, date, date)
        if not data_df_temp.empty:
            # Find the observation value, handling the case where there may be no data
            value = data_df_temp['value'].iloc[0] if not data_df_temp['value'].empty else None
            data_df_main.loc[date, series_id] = value

# Mapping series_id to number of months for column names
maturity_mapping = {
    'DGS1MO': '1M', 'DGS3MO': '3M', 'DGS6MO': '6M',
    'DGS1': '1Y', 'DGS2': '2Y', 'DGS3': '3Y',
    'DGS5': '5Y', 'DGS7': '7Y', 'DGS10': '10Y',
    'DGS20': '20Y', 'DGS30': '30Y'
}

data_df_main.rename(columns=maturity_mapping, inplace=True)

# Save the dataframe to a CSV file
data_df_main.to_csv('fred_yield_matrix.csv', index=True)
print(data_df_main)
