from fredapi import Fred
from datetime import date

fred = Fred(api_key='4dc6fb97db665c2cf01cd3377d5f252a')
today = date.today()
obs_date = today.strftime("%d-%m-%y")
data1 = fred.get_series('DGS1MO', observation_start = obs_date, observation_end=obs_date)
data2 = fred.get_series('DGS6MO', observation_start = obs_date, observation_end=obs_date)
print(data1)
print(data2)