"""
Function for impedance spectra when nanoparticles are added

Timothy Chew
6/8/24
"""

import numpy as np
import scipy.special as sps
import cmath
import scipy.constants as spc

#impedance function
def Z(w, C_A_ratio, C_g, C_ion, R_ion, kbt, n_AB, Js, V, R_s, R_sh, R_nano, C_nano):
    """
    n: electron ideality factor (1-2)
    V: diode DC input
    Js: diode saturation current
    R_sh: shunt resistance
    R_s: series resistance
    """
    C_A = C_A_ratio * C_ion

    q = spc.elementary_charge
    Z_nano = 1 / (1/R_nano + 1j * w * C_nano)

    Z_ion = 1 / (1j * w * C_ion) + 1 / (1j * w * C_g + 1/R_ion)
    Z_A = 1 / (1j * w * C_A)

    rec_current = Js * np.exp( q/n_AB/kbt * ( 1 - C_ion/C_A ) * V)

    Z_elec = 1 / ( rec_current * q/n_AB/kbt * (1 - Z_A/Z_ion) / ( 1 + sps.lambertw(rec_current * Z_nano * q/n_AB/kbt) ) )

    return 1 / (1/Z_elec + 1/Z_ion + 1/R_sh) + R_s