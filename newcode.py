import os
import requests
import pandas as pd
import time
import datetime
import pandas as pd
from datetime import date
import numpy as np
from scipy.optimize import fmin

def fetch_fred_data(series_id):
    api_key = 'e1ed8f4fb579f8537d1d1d263f4708b8'  # Replace with your API key
    base_url = 'https://api.stlouisfed.org/fred/'
    obs_endpoint = 'series/observations'

    # Assign parameters
    start_date = '2024-05-01'  # for the start date
    # end_date = date.today().strftime('%Y-%m-%d')  # for the end date
    # end_date = date.today()  # for the end date
    end_date = '2024-05-01'  # for the end date
    ts_frequency = 'd'  # for the frequency... d=daily, w=weekly, m=monthly, q=quarterly
    ts_units = 'lin'  # to get the unit of the data

    obs_params = {
        'series_id': series_id,
        'api_key': api_key,
        'file_type': 'json',
        'observation_start': start_date,
        'observation_end': end_date,
        'frequency': ts_frequency,
        'units': ts_units
    }

    # Make request to FRED API
    response = requests.get(base_url + obs_endpoint, params=obs_params)
    data = response.json()['observations']
    df = pd.DataFrame(data)

    return df

# List of series IDs
series_ids = ['DGS1MO', 'DGS3MO', 'DGS6MO', 'DGS1', 'DGS2', 'DGS3', 'DGS5', 'DGS7', 'DGS10', 'DGS20', 'DGS30']

# Loop over series IDs and fetch data
for series_id in series_ids:
    data_df = fetch_fred_data(series_id)
    print(data_df)
    data_df.to_csv('fred_' + series_id.lower() + '.csv', index=False)