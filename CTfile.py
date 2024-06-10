import PyCurve.nelson_siegel
import pandas as pd
from fredapi import Fred
from PyCurve.nelson_siegel import NelsonSiegel
import numpy as np
import matplotlib.pyplot as plt
import PyCurve.curve as pycurve

# Function to fetch data from FRED
def fetch_fred_data(api_key, series_ids):
    fred = Fred(api_key=api_key)
    data = {}
    for series_id in series_ids:
        data[series_id] = fred.get_series(series_id)
    return data

# Function to calibrate Nelson-Siegel model
def calibrate_ns_model(data):
    # Convert data to DataFrame
    df = pd.DataFrame(data)

    # Extract maturities and yields
    maturities = [1 / 12, 3 / 12, 1, 2, 5, 10, 30]  # in years
    yields = df.values.flatten() / 100  # convert percentage to decimal

    # Calibrate Nelson-Siegel model
    ns_curve = PyCurve.nelson_siegel.Curve
    ns_curve.fit(yields)
    ns_curve.fit(maturities, yields)

    return ns_curve

def plot_yield_curve(ns_curve):
    # Generate maturities for plotting
    x = np.linspace(0.01, 30, 1000)

    # Calculate yields using calibrated Nelson-Siegel model
    y = ns_curve.predict(x)

    # Plot the yield curve
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, label='Nelson-Siegel Yield Curve', color='blue')
    plt.xlabel('Maturity (Years)')
    plt.ylabel('Yield')
    plt.title('Nelson-Siegel Yield Curve')
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    # API Key for FRED (replace 'YOUR_API_KEY' with your actual FRED API key)
    api_key = '4dc6fb97db665c2cf01cd3377d5f252a'

    # Series IDs for interest rate curve data
    series_ids = ['DGS1MO', 'DGS3MO', 'DGS1', 'DGS2', 'DGS5', 'DGS10', 'DGS30']

    # Fetch data from FRED
    data = fetch_fred_data(api_key, series_ids)

    # Calibrate Nelson-Siegel model
    ns_curve = calibrate_ns_model(data)

    # Plot the yield curve
    plot_yield_curve(ns_curve)

if __name__ == "__main__":
    main()