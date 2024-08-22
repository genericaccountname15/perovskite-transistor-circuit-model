"""
Updated guesser for single transistor model

Timothy Chew
19/8/2024
"""

import numpy as np
import matplotlib.pyplot as plt
import cmath
import scipy.constants as spc
import scipy.special as sps

import Finder as find
from FinderInterface import Interface

def param_guesser(bias_data, nobias_data, IV_data, bias_voltage, kbt=4.1302114835e-21, Js=2.31e-16, bias=True, nanoparticles=False, run_checker=True):
    #unpacking

    Rion, Rsh, Rs, Rn0, Rninf, wg_bias, wg_nobias, wion_bias, wion_nobias, wnano = Interface(bias_data, nobias_data, IV_data, run_checker=run_checker, nanoparticle=nanoparticles)

    #solving for variable values
    Cion_bias = find.get_Cion(wion_bias, Rion)
    Cion_nobias = find.get_Cion(wion_nobias, Rion)

    Cg_bias = find.get_Cg_Bias(wg_bias, Cion_bias, Rninf)
    Cg_nobias = find.get_Cg(wg_nobias, Rsh, Rs, Rion)

    #solving for CA_ratio and n (incorrect depending on Cg Cion values)
    CA = Cion_bias / (1 - Rninf/Rn0)
    CA_ratio = CA/Cion_bias

    n = (spc.elementary_charge/kbt * (1 - Cion_bias/CA) * bias_voltage /
          sps.lambertw(1/Js/Rninf * (1 - Cion_bias/CA) * bias_voltage ).real)
    
    if wnano is not None:
        Rnano = find.get_Rnano(bias_data[:,1], bias_data[:,2], wnano, Rninf, Rs)
        Cnano = find.get_Cnano(wnano, Rnano)
        n = (spc.elementary_charge/kbt * (1 - Cion_bias/CA) * bias_voltage /
          sps.lambertw(1/Js/(Rninf - Rnano) * (1 - Cion_bias/CA) * bias_voltage ).real) 

    if nanoparticles:
        param_list_bias = (CA_ratio, Cg_bias, Cion_bias, Rion, kbt, n, Js, bias_voltage, Rs, Rsh, Rnano, Cnano)
        param_list_nobias = (CA_ratio, Cg_nobias, Cion_nobias, Rion, kbt, n, Js, bias_voltage, Rs, Rsh, Rnano, Cnano)
    else:
        param_list_bias = (CA_ratio, Cg_bias, Cion_bias, Rion, kbt, n, Js, bias_voltage, Rs, Rsh)
        param_list_nobias = (CA_ratio, Cg_nobias, Cion_nobias, Rion, kbt, n, Js, bias_voltage, Rs, Rsh)

    if bias:
        return param_list_bias
    else:
        return param_list_nobias

    

if __name__ == "__main__":
    # single transistor
    # #loading data
    # IV_data = np.loadtxt("test_data/Pixel5ControlLightForwardsweep/CVafter.txt", skiprows=1)
    # bias_data = np.loadtxt("test_data/nyquist.txt", skiprows=1)
    # nobias_data = np.loadtxt("test_data/nyquist_dark.txt", skiprows=1)
    # bias_voltage = 1.023

    # plist = guesser(bias_data, nobias_data, IV_data, bias_voltage, run_checker=False, bias=True)

    # from single_transistor_model.Impedancefunction import Z
    # from Plotter import plotter
    # plotter(Z, "single_transistor_model\Initial_params.csv", bias_data, plist)

    #nanoparticles
    #loading data
    IV_data = np.loadtxt("test_data/Pixel1NanoparticlesLightForwardsweep/CVafter.txt", skiprows=1)
    bias_data = np.loadtxt("test_data/nyquist2.txt", skiprows=1)
    nobias_data = np.loadtxt("test_data/nyquist2_dark.txt", skiprows=1)
    bias_voltage = 1.023

    plist = param_guesser(bias_data, nobias_data, IV_data, bias_voltage, run_checker=False, bias=True, nanoparticles=True)

    from nanoparticles_model.Impedancefunction import Z
    from Plotter import plotter
    plotter(Z, "nanoparticles_model\Initial_params.csv", bias_data, plist)

    