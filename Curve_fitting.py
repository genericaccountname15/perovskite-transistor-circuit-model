"""
Performs a least-squares fit on data
using guess params

Timothy Chew
22/8/24
"""

import numpy as np
from scipy.optimize import curve_fit

from Guesser import param_guesser


def fit_leastsq(Z, bias_data, nobias_data, bias_voltage, IV_data=None, run_checker=False, bias=True, 
                nanoparticles=False, fixed_params_indices = [], fixed_params_values = []):
    """
    Performs a least square fit to data using scipy curve_fit function
    Args:
        Z (function): Complex impedance function to fit to
        bias_data (array): Impedance data taken from the cell under electrical bias
        nobias_data (array): Impedance data taken from the cell under 0V bias
        bias_voltage (float): The bias voltage 'bias_data' was taken under
        IV_data (array): Current-Voltage step curve
        run_checker (boolean): Whether to open the 'FinderInterface' checker to double check graphical features
        bias(boolean): Whether to investigate the 'bias_data' array, else will fit to 'nobias_data' array
        nanoparticles (boolean): Whether we are using the nanoparticles model
        fixed_params_indices: indices of parameters to fix
        fixed_params_values: values of parameters to fix
    
    Returns:
        fitted_params (tuple): tuple of optimal parameters generated from curve_fit
        If curve_fit enters a runtime error, fitted_params will be the guessed params and the curve_fit
        will be ignored
    """

    plist_guess = list(param_guesser(bias_data, nobias_data, IV_data, bias_voltage, run_checker=run_checker, bias=bias, nanoparticles=nanoparticles))

    print(plist_guess)

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

        #make sure the parameters STAY >0
        param_list = tuple(abs(value) for value in param_list)

        Z_val = Z(w, *param_list)
        return np.hstack([Z_val.real, -Z_val.imag])
    
    try:
        fitted_params, cov = curve_fit(imp_func, xdata, ydata, p0=plist_guess)
    except RuntimeError:
        print("Unable to find optimal params: using guess params")
        fitted_params = plist_guess
    
    #make sure the parameters STAY >0
    fitted_params = tuple(abs(value) for value in fitted_params)

    return fitted_params

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from Plotter import plotter
    from single_transistor_model.Impedancefunction import Z

    nobias_data = np.loadtxt("test_data\\nyquist_dark.txt", skiprows=1)
    bias_data = np.loadtxt("test_data\\nyquist.txt", skiprows=1)
    IV_data = np.loadtxt("test_data/Pixel5ControlLightForwardsweep/CVafter.txt", skiprows=1)
    bias_voltage = 1.023

    plist_fit = fit_leastsq(Z, bias_data, nobias_data, bias_voltage, IV_data, nanoparticles=False, bias=False, fixed_params_indices=[7], fixed_params_values=[bias_voltage])
    #plist_guess = param_guesser(bias_data, nobias_data, IV_data, bias_voltage, run_checker=False, bias=False, nanoparticles=False)

    plotter(Z, "single_transistor_model\Initial_params.csv", nobias_data, plist_fit)