from fredapi import Fred
from datetime import date
import pandas as pd
import json

# Set API key
#fred = Fred(api_key='4dc6fb97db665c2cf01cd3377d5f252a')

# Set observation date as today's date
#today = date.today()
#obs_date = today.strftime("%d-%m-%y")

# Get the FRED data
#data1 = fred.get_series(series_id='DGS1MO', observation_start = obs_date, observation_end = obs_date, format=json)
#data2 = fred.get_series_info(series_id='DGS1MO')
#print(data1)
#print(data2)

# Build a dataframe
d = {'Months': ["DGS1MO", "DGS3MO", "DGS1"], 'Yield': [0.03, 0.04, 0.05]}
df = pd.DataFrame(data=d)
df.to_csv('testout.csv', index=False)
print(df)
y = df['Yield']
m = df['Months']
print(y)
print(m)
