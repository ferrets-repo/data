import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt

# Example data - time to maturity and corresponding yields
tau = np.array([1, 2, 3, 5, 7, 10, 20])
y = np.array([0.02, 0.025, 0.03, 0.035, 0.04, 0.045, 0.05])

# Nelson-Siegel function
def nelson_siegel(tau, beta):
    b0, b1, b2, lam = beta
    return b0 + b1 * ((1 - np.exp(-tau / lam)) / (tau / lam)) + b2 * (((1 - np.exp(-tau / lam)) / (tau / lam)) - np.exp(-tau / lam))

# Loss function to minimize
def loss_function(beta, tau, y):
    y_pred = nelson_siegel(tau, beta)
    return np.sum((y_pred - y) ** 2)

# Initial guess for beta values
initial_guess = [0.05, 0.2, 0.3, 1.0]

# Fitting the Nelson-Siegel model using minimize
result = minimize(loss_function, initial_guess, args=(tau, y), method='Nelder-Mead')

# Extract fitted parameters
fitted_beta = result.x

# Predict yields using fitted model
y_pred = nelson_siegel(tau, fitted_beta)

# Plotting the original data and the fitted curve
plt.plot(tau, y, 'bo', label='Original Data')  # Original data
plt.plot(tau, y_pred, 'r-', label='Fitted Curve')  # Fitted curve
plt.xlabel('Time to Maturity')
plt.ylabel('Yield')
plt.title('Nelson-Siegel Yield Curve Fitting')
plt.legend()
plt.grid(True)
plt.show()
