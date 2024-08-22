"""
Updated version of Finder.py

Timothy Chew
16/8/2024
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

#Functions that find key points on graph
def get_Rsh_IV(I, V, scan_range=150):
    """
    Finds shunt resistance from gradient of IV curve
    """
    #get gradient using polyfit
    ydata = V[0:scan_range]
    xdata = I[0:scan_range]
    fit = np.polyfit(xdata, ydata, 1)
    return fit[0]

def get_tconstants(w, Zreal, Zimag, bias=False):
    """
    Finds frequency values of loop's time constants
    """
    phase = np.arctan2(-Zimag, Zreal)
    peaks = find_peaks(-phase)[0]
    wg_guess = w[peaks[0]]
    if bias:
        wion_guess = w[peaks[1]]
    else:
        wion_guess = w[np.argmax(Zimag)]
    return wg_guess, wion_guess

def get_Rs_alt(Zreal, Zimag):
    """
    Alternative method of finding Rs
    Uses impedance spectra under non 0V bias
    """
    grad = Zimag[1] - Zimag[0] / (Zreal[1] - Zreal[0])
    #solving for x when y=0 in y - y1 = m(x - x1)
    Rs = - Zimag[0] / grad + Zreal[0]
    return Rs

def get_Rion(Zreal, Rsh_guess):
    """
    Returns the value of Rion given an impedance spectra's real values
    Takes the max of the real values (semicircle width)
    If shunt is low, return None
    """
    Rion_guess = max(Zreal)
    if Rion_guess > Rsh_guess:
        print("Unable to estimate Rion due to low shunt resistance")
        return None
    else:
        return Rion_guess

def get_Rsh(Zreal, Rsh_guess):
    """
    For low shunt case
    Gets Rsh from nyquist plot
    """
    if max(Zreal) > Rsh_guess:
        return max(Zreal)
    else:
        return Rsh_guess

def get_Rn(Zreal, Zimag, Rs):
    """
    Returns value of Rn0 and Rninf under non-0V bias case
    Uses impedance spectra magnitude flats
    """
    peaks = find_peaks(Zimag)[0]
    #0th peak - first loop peak
    #R inf is length to lowest point

    #check for lowest point after 0th peak
    RnO_index = np.argmin(Zimag[peaks[0]+1:]) + peaks[0] - 1
    RnO = Zreal[RnO_index] - Rs

    #possible indices for Rninf (after peak of 1st semicircle to end on 2nd semicircle)
    Rninf_indices = range(peaks[0]+1,RnO_index)

    #look for peaks again
    peaks = find_peaks(Zreal[Rninf_indices])[0]
    Rninf = Zreal[peaks[0]] - Rs

    return RnO, Rninf

def get_tconstant_nano(w, wion_bias, wg_bias):
    """
    Find time constant of nanoparticle bit
    Returns a point between wion and wg cuz idk how to find the point systematically
    """
    wg_index = np.where(w==wg_bias)[0][0]
    wion_index = np.where(w==wion_bias)[0][0]
    wnano_index = (wg_index + wion_index) // 2

    wnano = w[wnano_index]
    return wnano

#functions which calculate parameters values
#should put in a different module
def get_Cg(wg, Rsh, Rs, Rion):
    """
    Cg = 1 / ( wg * sqrt( Rsh * Rs ) ) if Rsh < Rion    LOW SHUNT
    Cg = 1 / ( wg * sqrt( Rion * Rs ) ) if Rion > Rsh   HIGH SHUNT
    """
    if Rsh < Rion:
        Cg = 1 / (wg * np.sqrt(Rsh * Rs))
    else:
        Cg = 1 / (wg * np.sqrt(Rion * Rs))

    return Cg

def get_Cg_Bias(wg, Cion, Rninf):
    """
    Under bias
    wg = 1 / (Ceff * Rninf)
    where Ceff = (1/Cion + 1/Cg )^-1
    """
    Cg = 1 / ( Rninf * wg - 1/Cion )
    return Cg

def get_Cion(wion, Rion):
    """
    wion = 1 / (Rion * Cion) under high bias (more than 1V)
    Unaffected by Rsh even if Rsh < Rion for some reason
    """
    Cion = 1 / (Rion * wion)
    return Cion

def get_Rnano(w, Zreal, wnano, Rninf, Rs):
    """
    Guesses resistance of nanoparticle circuit
    Rninf + Rs - Dist. to nanoparticle time constant
    """
    wnano_index = np.where(w==wnano)[0][0]
    Rnano = Rninf + Rs - Zreal[wnano_index]
    Rnano *= 2 #since the time constant is at half Rnano
    return Rnano

def get_Cnano(wnano, Rnano):
    Cnano = 1 / (wnano * Rnano)
    return Cnano

if __name__ == "__main__":
    #data = np.loadtxt("test_data\Pixel5ControlLightForwardsweep\\nyquist.txt", skiprows=1)
    data = np.loadtxt("test_data\Pixel1NanoparticlesLightForwardsweep\\nyquist.txt", skiprows=1)
    Zreal = data[:,2]
    Zimag = data[:,3]

    wg, wion = get_tconstants(data[:,1], Zreal, Zimag, bias=True)
    wg_index = np.where(data[:,1]==wg)[0]
    wion_index = np.where(data[:,1]==wion)[0]

    plt.plot(Zreal, Zimag, 'o')
    plt.plot(Zreal[wg_index], Zimag[wg_index], 'x', markersize=10)
    plt.plot(Zreal[wion_index], Zimag[wion_index], 'x', markersize=10)
    plt.show()
