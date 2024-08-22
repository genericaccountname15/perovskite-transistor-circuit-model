"""
The big donk

Timothy Chew
13/8/2024
"""

import numpy as np
from nanoparticles_model.Impedancefunction import Z
from Plotter import plotter
from Guesser_Single import param_guesser

def main():
    nobias_data = np.loadtxt("test_data\\nyquist2_dark.txt", skiprows=1)
    bias_data = np.loadtxt("test_data\\nyquist2.txt", skiprows=1)
    bias_voltage = 1.023

    #params = param_guesser(nobias_data, bias_data, bias_voltage, 4.1302114835e-21, 2.31e-16)

    plotter(Z, "nanoparticles_model\Initial_params.csv", bias_data, None)

if __name__ == "__main__":
    main()