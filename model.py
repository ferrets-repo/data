import matplotlib
# import inline
import pandas as pd
from fredapi import Fred
import datetime as dt

from pandas._testing import at

# set up Fred key else queries do not work
fred = Fred(api_key='4dc6fb97db665c2cf01cd3377d5f252a')
# Search for the ticker by description
ticker_description = 'Market Yield on U.S. Treasury Securities at 1-Month Constant Maturity, Quoted on an Investment Basis'
ticker_info = fred.search(ticker_description)

if ticker_info is None:
    print("Did not find ticker by searching the text '{0}'. Pleave revise your search.".format(ticker_description))
else:
    # ticker_id = ticker_info['DGS1MO'].values[0]
    ticker_start = ticker_info['observation_start'].values[0]
    ticker_end = ticker_info['observation_end'].values[0]
    # print("Ticker id = {0}, start_date = {1}, end_date = {2}".format(ticker_id, ticker_start, ticker_end))
    try:
        # query the ticker information from FRED using start and end dates
        s = fred.get_series('DGS1MO', observation_start=ticker_start, observation_end=ticker_end)
        print(s.tail())
        # Save daily close file since inception
        s.to_csv("output/DGS1MO.csv")
        # Save quarterly file. Use 'QS' frequency for beginning of month data
        pd.Series(s, pd.date_range('2019-03-14', dt.datetime.now(), freq='QS')).to_csv("output/DGS1MO_quarterly.csv")
    except:
        print("Problem downloading series")

from matplotlib import pyplot as plt
# import seaborn as sns
import numpy as np

# %matplotlib inline

s.plot(figsize=(10,5), grid=True, title='{0}% ({1})'.format(ticker_description, "DGS1MO - test"))
plt.show()
# <matplotlib.axes._subplots.AxesSubplot at 0x1092dfe48>