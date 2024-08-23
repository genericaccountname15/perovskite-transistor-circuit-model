"""
Performs a least-squares fit on data
using guess params

Timothy Chew
22/8/24
"""

import numpy as np
from scipy.optimize import curve_fit

from Guesser import param_guesser


def fit_leastsq(Z, bias_data, nobias_data, IV_data=None, bias_voltage=None, run_checker=False, bias=True, fixed_params_indices = [], fixed_params_values = []):
    """
    Performs a least square fit to data using scipy curve_fit function
    Args:
        fixed_params_indices: indices of parameters to fix
        fixed_params_values: values of parameters to fix
    """
    if bias_voltage is None:
        bias_voltage = float(input("Please enter bias voltage value (V): "))
    plist_guess = list(param_guesser(bias_data, nobias_data, IV_data, bias_voltage, run_checker=run_checker, bias=bias))

    #set fixed params
    if len(fixed_params_indices) != 0:
        for i, index in enumerate(fixed_params_indices):
            plist_guess[index] = fixed_params_values[i]

    if bias:
        xdata = bias_data[:,1]
        ydata_real = bias_data[:,2]
        ydata_imag = bias_data[:,3]
    else:
        xdata = nobias_data[:,1]
        ydata_real = nobias_data[:,2]
        ydata_imag = nobias_data[:,3]

    ydata = np.hstack( [ydata_real, ydata_imag] )

    def imp_func(w, *param_list):
        #ensure fixed parameters are unchanged
        param_list = list(param_list)
        if len(fixed_params_indices) != 0:
            for i, index in enumerate(fixed_params_indices):
                param_list[index] = fixed_params_values[i]
        
        Z_val = Z(w, *param_list)
        return np.hstack([Z_val.real, -Z_val.imag])

    fitted_params, cov = curve_fit(imp_func, xdata, ydata, p0=plist_guess)

    return fitted_params

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from Plotter import plotter
    from single_transistor_model.Impedancefunction import Z

    nobias_data = np.loadtxt("test_data\\nyquist_dark.txt", skiprows=1)
    bias_data = np.loadtxt("test_data\\nyquist.txt", skiprows=1)
    IV_data = np.loadtxt("test_data/Pixel5ControlLightForwardsweep/CVafter.txt", skiprows=1)
    bias_voltage = 1.023

    plist_fit = fit_leastsq(Z, bias_data, nobias_data, IV_data, bias_voltage, False, True, fixed_params_indices=[7], fixed_params_values=[bias_voltage])

    plotter(Z, "single_transistor_model\Initial_params.csv", bias_data, plist_fit)