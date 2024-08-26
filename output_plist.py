"""
Outputs plist nice and pretty
Very demure

Timothy Chew
23/8/24
"""

import pandas as pd
from tabulate import tabulate

def output_params(init_paramfilename, plist):
    """
    Outputs list of parameters using tabulate module
    Args:
        init_paramfilename (string): Filename of init_params.csv under model folder
        plist (tuple): list of parameters to output
    Returns:
        tabulate object containing parameter names and values
    """
    output_array = []
    param_names = pd.read_csv(init_paramfilename, delimiter=",").values[:,0]

    for i, param_name in enumerate(param_names):
        output_array.append([param_name, plist[i]])
    
    print(tabulate(output_array, headers=["param", "value"]))


if __name__ == "__main__":
    plist = [5.42008853e+00, 7.01909189e-07, 1.89283000e-05, 1.67179300e+02,
    4.10450510e-21, 1.07789316e+00, 2.05120023e-16, 1.02287292e+00,
    1.32622328e+01, 1.22326815e+06]

    init_paramfilename = "single_transistor_model\Initial_params.csv"

    output_params(init_paramfilename, plist)