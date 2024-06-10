# fred api
#api_key = fred_key
api_key = 'e1ed8f4fb579f8537d1d1d263f4708b8' # where you input your Api key

# Define the FRED API endpoint
base_url = 'https://fred.stlouisfed.org/series/'

'''
Get observation data from the FRED API
'''

# Assign endpoint
obs_endpoint = 'series/observations'

# Assign parameters
series_id = ['DGS1MO'] # for the series_id 'DGS3MO', 'DGS6MO', 'DGS1', 'DGS2', 'DGS3', 'DGS5', 'DGS7', 'DGS10', 'DGS20', 'DGS30'
start_date = '2010-01-01' # for the start date
end_date = datetime.today().strftime('%Y-%m-%d')   # for the end date
ts_frequency = 'q'    # for the frequency
ts_units = 'pca'       # to get the unit of the data

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

print(df)
#to save to csv file or any other file
df.to_csv('fred.csv', index=False)

pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.max_rows', None)     # Show all rows

# Read CSV files into DataFrames
df1 = pd.read_csv('fred.csv')

# get the shape of the data
print("Shape of df2:", df2.shape)

# to know the columns of each data frame
print("Columns of DataFrame 1:")
print(df1.columns)
