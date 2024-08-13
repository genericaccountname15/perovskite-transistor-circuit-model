"""
This module performs a leastsq fit to data
using the lmfit module.
Fits frequencies to imaginary impedance

Timothy Chew
13/8/2024
"""

import numpy as np
import matplotlib.pyplot as plt
import cmath

from scipy.optimize import minimize
from single_transistor_model.Impedancefunction import Z
from Guesser_Single import param_guesser

# Define a cost function for the minimization
def cost_function(params, w, Z_data):
    model = Z(w, *params)
    return np.sum(np.abs(model - Z_data) ** 2)


nobias_data = np.loadtxt("test_data\\nyquist_dark.txt", skiprows=1)
bias_data = np.loadtxt("test_data\\nyquist_dark.txt", skiprows=1)
bias_voltage = 1.023

param_guess = param_guesser(nobias_data, bias_data, bias_voltage, 4.1302114835e-21, 2.31e-16)

w_data = bias_data[:,1]
Z_data = bias_data[:,2] + 1j * bias_data[:,3]
fit = minimize(cost_function, param_guess, args=(w_data, Z_data))
print(param_guess)
print(fit.x)