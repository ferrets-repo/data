# import os
# import requests
# import time
# import datetime
import pandas as pd
from datetime import date
from scipy.optimize import fmin
from scipy.optimize import minimize
import numpy as np
# import fredapi as fapi
from fredapi import Fred
from nelson_siegel_svensson.calibrate import calibrate_ns_ols
from nelson_siegel_svensson import NelsonSiegelCurve
from scipy.optimize import least_squares

# Your FRED API key
fred_key = 'e1ed8f4fb579f8537d1d1d263f4708b8'

# Initialize the FRED client
fred = Fred(api_key=fred_key)

# List of FRED series IDs
ids = ['DGS1MO', 'DGS3MO', 'DGS6MO', 'DGS1', 'DGS2', 'DGS3', 'DGS5', 'DGS7', 'DGS10', 'DGS20', 'DGS30']

# Initialize an empty DataFrame to hold all the series data
combined_df = pd.DataFrame()

# Initialize an empty DataFrame to hold the final NS results
df_final = pd.DataFrame({
    'Date': [''], 
    'Level': [''],
    'Slope': [''],
    'Curveature': [''],
    'Decay': ['']
})

# Mapping series_id to number of months for column names
maturity_mapping = {
    'DGS1MO': '1', 'DGS3MO': '3', 'DGS6MO': '6',
    'DGS1': '12', 'DGS2': '24', 'DGS3': '36',
    'DGS5': '60', 'DGS7': '84', 'DGS10': '120',
    'DGS20': '240', 'DGS30': '360'
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

# Drop rows with NaN values
clean_df = combined_df.dropna()

# Convert the DataFrame to long format
long_df = clean_df.reset_index().melt(id_vars='index', var_name='Maturity', value_name='Yield')

# Rename the 'index' column to 'Date'
long_df.rename(columns={'index': 'Date'}, inplace=True)

# Pivot the DataFrame to get dates as columns, maturities as rows, and yield values as values
pivot_df = long_df.pivot(index='Maturity', columns='Date', values='Yield')

# Convert maturity to integers for sorting purposes
pivot_df.index = pivot_df.index.astype(int)

# Define the desired order of maturities
maturity_order = [1, 3, 6, 12, 24, 36, 60, 84, 120, 240, 360]

# Reindex the pivot table to ensure the maturities are in the correct order
pivot_df = pivot_df.reindex(maturity_order)

# Sort the columns by date for better readability (optional)
pivot_df.sort_index(axis=1, inplace=True)

# Create a new MultiIndex for columns with "Yield" as the second level
pivot_df.columns = pd.MultiIndex.from_product([pivot_df.columns, ['Yield']])

# Function to fit Nelson-Siegel model using a robust least squares method
def robust_calibrate_ns_ols(maturities, yields):
    def ns_function(params, maturities, yields):
        beta0, beta1, beta2, tau = params
        ns_curve = NelsonSiegelCurve(beta0, beta1, beta2, tau)
        return ns_curve(maturities) - yields

    initial_guess = [0.03, -0.02, 0.02, 1.0]  # Example initial guess
    result = least_squares(ns_function, initial_guess, args=(maturities, yields), method='trf', loss='soft_l1')
    if result.success:
        return NelsonSiegelCurve(*result.x), result
    else:
        raise ValueError("Optimization failed")

# Fit the Nelson-Siegel model to the data
for date in pivot_df.columns.get_level_values(0).unique():
    yields = pivot_df[date].values.flatten()
    maturities = pivot_df.index.values / 12  # convert months to years
   
    # Fit the Nelson-Siegel model using robust fitting
    try:
        curve, result = robust_calibrate_ns_ols(maturities, yields)
        # Store results as a row in df_final dataframe
        df_final.loc[len(df_final)] = date, curve.beta0, curve.beta1, curve.beta2, curve.tau
    except ValueError as e:
        print(f"Fitting failed for date {date}: {e}")

# Save the dataframe to a CSV file
df_final.to_csv('NS_model.csv', index=False)