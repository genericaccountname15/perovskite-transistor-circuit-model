"""
This module performs all the main fitting things
Basically like the main.py file

Timothy Chew
22/8/24
"""

import numpy as np
import pandas as pd
import importlib.util

from Plotter import plotter
from Curve_fitting import fit_leastsq
from output_plist import output_params

def imp_fitting(imp_model_folder, datafile, nobias_datafile, IVfile, OCPfile, bias, run_checker):
    """
    Performs fitting operations
    Combines functionality of plotter, Curve_fitting, and output_plist modules
    Args:
        imp_model_folder (string): name of folder containing the impedance model
        datafile (string): name of file containing impedance bias data
        nobias_datafile (string): name of file containing impedance data under 0V bias
        IVfile (string or None): name of file containing current-voltage data
        OCP file (string or None): name of file containing OCP data
        bias (boolean): Whether to investigate the bias or no bias data file
        run_checker (boolean): Whether to run the checker FinderInterface
    Returns:
        Tabulate object containing parameter names and values
    """
    #importing function
    spec = importlib.util.spec_from_file_location("Impedancefunction.py", imp_model_folder+"/Impedancefunction.py")
    if spec is None:
        print(f"Cannot load module from folder: {imp_model_folder}")
        return None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    Z = getattr(module, "Z", None)

    #importing associated initial parameters
    init_paramfilename = imp_model_folder+"\Initial_params.csv"
    nano = False
    if imp_model_folder == "nanoparticles_model":
        nano = True

    #loading data
    data = np.loadtxt(datafile, skiprows=1)

    nobias_data=None
    IVdata=None
    biasvoltage=None

    if nobias_datafile is not None:
        nobias_data = np.loadtxt(nobias_datafile, skiprows=1)
    
    if IVfile is not None:
        IVdata = np.loadtxt(IVfile, skiprows=1)
    
    if OCPfile is not None:
        biasvoltage = pd.read_csv(OCPfile, sep="\t", header=0).values[0,5]
    else:
        biasvoltage = float(input("Please enter bias voltage value (V): "))

    #running fit
    if bias:
        plist_fitted = fit_leastsq(Z, data, nobias_data, biasvoltage, IVdata, bias=bias, nanoparticles=nano,
                                run_checker=run_checker, fixed_params_indices=[7], fixed_params_values=[biasvoltage])
        plotter(Z, init_paramfilename, data, plist_fitted)
    else:
        plist_fitted = fit_leastsq(Z, data, nobias_data, biasvoltage, IVdata, bias=bias, nanoparticles=nano,
                                run_checker=run_checker)
        plotter(Z, init_paramfilename, nobias_data, plist_fitted)

    output_params(init_paramfilename, plist_fitted)


if __name__ == "__main__":
    imp_model_folder = "single_transistor_model"
    datafile = "test_data/nyquist.txt"
    nobias_datafile = "test_data/nyquist_dark.txt"
    IVfile = "test_data\Pixel5ControlLightForwardsweep\CVafter.txt"
    OCPfile = "test_data\Pixel5ControlLightForwardsweep\OCP.txt"

    imp_fitting(imp_model_folder, datafile, nobias_datafile, IVfile=IVfile, OCPfile=OCPfile, bias=True, run_checker=False)