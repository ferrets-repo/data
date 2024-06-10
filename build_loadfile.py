import requests
import pandas as pd

def fetch_fred_data(series_id):
    api_key = 'e1ed8f4fb579f8537d1d1d263f4708b8'  # Replace with your API key
    base_url = 'https://api.stlouisfed.org/fred/'
    obs_endpoint = 'series/observations'

    # Assign parameters
    start_date = '2024-05-01'  # for the start date
    end_date = '2024-05-21'  # for the end date
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

# Create main dataframe with 'Maturity' and 'Yield' column names but leave it empty
data_df_main = pd.DataFrame(columns=['Maturity', 'Yield'])

# Loop over series IDs and fetch data
for series_id in series_ids:
    # Put series data into a temporary dataframe
    data_df_temp = fetch_fred_data(series_id)
    # Load row 0 data from the temp dataframe 'value' column into the next empty 'value' cell of the main dataframe
    data_df_main.loc[len(data_df_main), 'Yield'] = data_df_temp.loc[0, 'value']
    # Load 'series_id' into the next empty 'series_id' cell of the main dataframe
    data_df_main.loc[len(data_df_main)-1, 'Maturity'] = series_id
    # prevent old index being added as a column
    data_df_main = data_df_main.reset_index(drop=True)

# Search through the dataframe and replace the 'series_id' with the number of months
data_df_main['Maturity'] = data_df_main['Maturity'].map({'DGS1MO': 1, 'DGS3MO': 3, 'DGS6MO': 6, 'DGS1': 12, 'DGS2': 24, 'DGS3': 36, 'DGS5': 60, 'DGS7': 84, 'DGS10': 120, 'DGS20': 240, 'DGS30': 360 })

# Save the dataframe to a CSV file
data_df_main.to_csv('fred_table.csv', index=True)
print(data_df_main)