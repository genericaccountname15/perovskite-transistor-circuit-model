"""
Locates positions of key points on plots
Calculates parameter guess values for 0V bias
Finds values on plots for non-0V bias

Timothy Chew
12/8/2024
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# #importing data
# def arg(z):
#     return np.arctan2(z.imag, z.real)

# data = np.loadtxt("test_data\\nyquist2.txt", skiprows=1)

def get_Rion(imp_spectra_real):
    """
    Returns the value of Rion given an impedance spectra's real values
    Takes the max of the real values (semicircle width)
    Args:
        imp_spectra_real (array): real part of measured impedance under 0V bias
    """
    return max(imp_spectra_real)

def get_Rion_alt(imp_magnitude):
    """
    Alternative method of getting R_ion
    Returns the value of Rion given the magnitude of impedance under 0V bias
    Takes the max value (flat part at top)
    """
    return max(imp_magnitude)

def get_Rs(imp_magnitude):
    """
    Returns the value of Rs given magnitude of impedance under 0V bias
    Takes the min value (flat part at bottom)
    """
    return min(imp_magnitude)

def get_Rs_alt(imp_spectra_real):
    """
    Alternative method of finding Rs
    Uses impedance spectra under non 0V bias
    """
    return min(imp_spectra_real)

def get_Cg(w, imp_phase, Rs, Rion):
    """
    Returns the value of C_g given the phase spectra under 0V bias
    Based on minimum point
    """
    argZ_min_index = np.argmin(imp_phase)
    wmin = w[argZ_min_index]
    return 1 / (wmin * np.sqrt(Rs * Rion))

def get_Cion(w, imp_phase, C_g, Rion):
    """
    Returns the value of Cion given the phase spectra under 0V bias
    Based on maximum point
    """
    argZ_max_index = np.argmax(imp_phase)
    wmax = w[argZ_max_index]
    return 1 / (Rion * Rion * w * w * C_g) - C_g

def get_Rn(imp_spectra_real, imp_spectra_imag):
    """
    Returns value of Rn0 and Rninf under non-0V bias case
    Uses impedance spectra peaks
    """
    peaks = find_peaks(imp_spectra_imag)[0]
    return imp_spectra_real[peaks[1]], imp_spectra_real[peaks[2]]





# #plotting data
# fig, (ax1, ax2) = plt.subplots(1, 2)
# twin = ax2.twinx()

# # Rn0, Rninf = get_Rn(data[:,2], data[:,3])
# # ax1.axvline(Rn0)
# # ax1.axvline(Rninf)

# ax1.plot(data[:,2], data[:,3], 'o', label="experimental impedance")
# ax2.plot(data[:,1], abs(data[:,2] + 1j*data[:,3]), 'o', label="measured |Z|", color="midnightblue")
# twin.plot(data[:,1], arg(data[:,2] - 1j*data[:,3]), 'o', label="measured argz", color="maroon")

# ax1.set_title("Impedance spectra")
# ax1.set_ylabel("-Z''")
# ax1.set_xlabel("Z")
# ax1.set_ylim(0,)

# ax2.set_xscale('log')
# ax2.set_yscale('log')
# ax2.set_title("Resonance and bode plot")
# ax2.set_ylabel("|Z|")
# ax2.set_xlabel("w")

# plt.show()