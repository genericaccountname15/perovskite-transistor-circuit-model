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

def imp_fitting(imp_model_folder, datafile, nobias_datafile, IVfile, OCPfile, bias, run_checker):
    """
    Performs fitting operations
    Args:
        (Args are string filenames)
    """
    #importing function
    spec = importlib.util.spec_from_file_location("Impedancefunction.py", imp_model_folder+"/Impedancefunction.py")
    if spec is None:
        print(f"Cannot load module from folder: {imp_model_folder}")
        return None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    Z = getattr(module, "Z", None)

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

    #running fit
    plist_fitted = fit_leastsq(Z, data, nobias_data, IVdata, biasvoltage, bias=bias, 
                               run_checker=run_checker, fixed_params_indices=[7], fixed_params_values=[biasvoltage])

    plotter(Z, "single_transistor_model\Initial_params.csv", data, plist_fitted)


if __name__ == "__main__":
    imp_model_folder = "single_transistor_model"
    datafile = "test_data/nyquist.txt"
    nobias_datafile = "test_data/nyquist_dark.txt"
    IVfile = "test_data\Pixel5ControlLightForwardsweep\CVafter.txt"
    OCPfile = "test_data\Pixel5ControlLightForwardsweep\OCP.txt"

    imp_fitting(imp_model_folder, datafile, nobias_datafile, IVfile, OCPfile)