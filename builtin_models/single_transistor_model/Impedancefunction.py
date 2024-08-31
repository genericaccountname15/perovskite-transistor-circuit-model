"""
Function for simple 1 transistor model impedance spectra for a perovskite solar cell

Timothy Chew
6/8/2024
"""

import numpy as np
import cmath
import scipy.constants as spc

def Z(w, C_A_ratio, C_g, C_ion, R_ion, kbt, n_AB, Js, V, R_s, R_sh):
    """
    Impedance response function to a voltage steady state and small perturbation
    with frequency w
    
    Args:
        w(np array): angular frequency of voltage perturbation
        C_A_ratio: C_A/C_ion
        C_g: geometric capacitance of ionic branch
        C_ion: total interfacial capacitance of ionic branch
        n_AB: electron ideality factor (1-2)
        Js: saturation current
        V: diode DC input
        R_s: series resistance
        R_sh: parallel/shunt resistance
    
    Returns:
        Total impedance of the system (complex number)
    """
    q = spc.elementary_charge
    C_A = C_A_ratio * C_ion
    Z_ion = 1 / (1j * w * C_ion) + 1 / (1j * w * C_g + 1/R_ion)
    Z_A = 1 / (1j * w * C_A)

    rec_current = Js * np.exp( q/n_AB/kbt * ( 1 - C_ion/C_A ) * V)
    gen_current = Js * np.exp( -q/n_AB/kbt * C_ion/C_A * V)

    Z_elec = 1 / (rec_current * q/n_AB/kbt * (1 - Z_A/Z_ion) + gen_current * q/n_AB/kbt * Z_A/Z_ion)

    return 1 / (1/Z_elec + 1/Z_ion + 1/R_sh) + R_s
