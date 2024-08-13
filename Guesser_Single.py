"""
Guesses initial params for single-transistor-model
Given 0V bias and non-0V bias data

Timothy Chew
12/8/2024
"""

import numpy as np
import cmath
import scipy.constants as spc
import scipy.special as sps
import Finder as find

def arg(z):
    return np.arctan2(z.imag, z.real)

def param_guesser(nobiasdata, biasdata, bias_voltage, kbt, Js):
    """
    Guesses initial params
    Args:
        nobiasdata: dataset of 0V bias impedance
        biasdata: dataset of bias data
        bias_voltage: steady-state bias voltage at which biasdata was taken
    """
    nobias_w = nobiasdata[:,1]
    nobias_real = nobiasdata[:,2]
    nobias_imag = nobiasdata[:,3]
    nobias_mag = abs(nobias_real + 1j * nobias_imag)
    nobias_phase = arg(nobias_real - 1j * nobias_imag)

    bias_real = biasdata[:,2]
    bias_imag = biasdata[:,3]

    Rion = find.get_Rion(nobias_real)
    Rs = find.get_Rs(nobias_mag)
    Cg = find.get_Cg(nobias_w, nobias_phase, Rs, Rion)
    Cion = find.get_Cion(nobias_w, nobias_phase, Cg, Rion)

    Rn0, Rninf = find.get_Rn(bias_real, bias_imag)

    CA = Cion / (1 - Rninf/Rn0)
    CA_ratio = CA/Cion

    n = spc.elementary_charge/kbt * (1 - Cion/CA) * bias_voltage * 1 / sps.lambertw(1 / Js / Rninf).real

    Rsh = 1e6

    param_list = (CA_ratio, Cg, Cion, Rion, kbt, n, Js, bias_voltage, Rs, Rsh)
    return param_list


if __name__ == "__main__":
    nobias_data = np.loadtxt("test_data\\nyquist_dark.txt", skiprows=1)
    bias_data = np.loadtxt("test_data\\nyquist.txt", skiprows=1)
    bias_voltage = 1.023

    param_guess = param_guesser(nobias_data, bias_data, bias_voltage, 4.1302114835e-21, 2.31e-16)
    print(param_guess)