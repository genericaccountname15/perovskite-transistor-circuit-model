"""
User interface for Finder module

Timothy Chew
17/8/2024
"""

import numpy as np
import matplotlib.pyplot as plt
import curve_fitting.Finder as find

from matplotlib.widgets import Slider
from graphics.Axes_generator import gen_axes

def Interface(bias_data, nobias_data=None, IV_data=None, nanoparticle=False, run_checker=True):
    """
    Plots things and checks for things
    Args:
        bias_data (array): Impedance data taken under bias
        nobias_data (array or None): Impedance data taken under 0V no bias
        IV_data (array or None): Current-Voltage data
        nanoparticle (boolean): Whether to check for a nanoparticle time constant
        run_checker (boolean): Whether to run the checker for obtained features
    Returns:
        features (tuple): Tuple of graphical features e.g.: time constants
    """
    #unpacking data
    bias_w = bias_data[:,1]
    bias_real = bias_data[:,2]
    bias_imag = bias_data[:,3]

    nobias_w = nobias_data[:,1]
    nobias_real = nobias_data[:,2]
    nobias_imag = nobias_data[:,3]

    #getting values
    if IV_data is not None:
        Rsh = find.get_Rsh_IV(IV_data[:,3], IV_data[:,4])
    else:
        Rsh = 1e6
    
    wg_bias, wion_bias = find.get_tconstants(bias_w, bias_real, bias_imag, bias=True)
    wg_nobias, wion_nobias = find.get_tconstants(nobias_w, nobias_real, nobias_imag, bias=False)

    Rs = find.get_Rs_alt(bias_real, bias_imag)

    Rn0, Rninf = find.get_Rn(bias_real, bias_imag, Rs)

    Rion = find.get_Rion(nobias_real, Rsh)
    if Rion is None:
        #maybe the thing measured from the IV is Rion
        Rion = Rsh
        Rsh = find.get_Rsh(nobias_real, Rsh)
    
    #bit for nanoparticles
    if nanoparticle:
        wnano = find.get_tconstant_nano(bias_w, wion_bias, wg_bias)
    else:
        wnano = None
    
    #checking data
    if run_checker:
        wg_bias, wion_bias, wnano = check_tconstants(wg_bias, wion_bias, bias_data, wnano)
        wg_nobias, wion_nobias, emptyhead = check_tconstants(wg_nobias, wion_nobias, nobias_data)
        Rn0, Rninf = check_Rn(Rn0, Rninf, bias_data, Rs)

    features = (Rion, Rsh, Rs, Rn0, Rninf, wg_bias, wg_nobias, wion_bias, wion_nobias, wnano)
    return features


def check_tconstants(wg, wion, nyquist_data, wnano=None):
    """
    Checks the time constants wion and wg
    Opens window to adjust time constant selection over datafile
    Accepts both bias and non bias cases
    Args:
        wg (float): Guess for Cg time constant from Finder module
        wion (float): Guess for Cion time constant from Finder module
        nyquist_data (array): Impedance data
        wnano (float or None): Guess for Cnano time constant from Finder module
    Returns:
        wg_output (float): Checked Cg time constant
        wion_output (float): Checked Cion time constant
        wnano_output (float): Checked Cnano time constant
    """
    fig, (ax1, ax2) = plt.subplots(1, 2)
    twin = ax2.twinx()

    w_data = nyquist_data[:,1]
    impreal_data = nyquist_data[:,2]
    impimag_data = nyquist_data[:,3]
    mag_data = abs(nyquist_data[:,2] + 1j*nyquist_data[:,3])
    phase_data = np.arctan2(-nyquist_data[:,3], nyquist_data[:,2])

    ax1.plot(impreal_data, impimag_data, 'o', label="experimental impedance")
    ax2.plot(w_data, mag_data, 'o', label="measured |Z|", color="midnightblue")
    twin.plot(w_data, phase_data, 'o', label="measured argz", color="maroon")

    #highlighting
    #WHY IS np.where LIKE THIS AHHHHHH
    wg_index = np.where(w_data == wg)[0][0]
    wion_index = np.where(w_data == wion)[0][0]

    #line objects
    wion_imp, = ax1.plot(impreal_data[wion_index], impimag_data[wion_index], 'o', label="wion", color="orange", markersize=10)
    wion_mag, = ax2.plot(w_data[wion_index], mag_data[wion_index], 'o', label="wion", color="orange", markersize=10)
    wion_phase, = twin.plot(w_data[wion_index], phase_data[wion_index], 'o', label="wion", color="orange", markersize=10)

    wg_imp, = ax1.plot(impreal_data[wg_index], impimag_data[wg_index], 'o', label="wg", color="green", markersize=10)
    wg_mag, = ax2.plot(w_data[wg_index], mag_data[wg_index], 'o', label="wg", color="green", markersize=10)
    wg_phase, = twin.plot(w_data[wg_index], phase_data[wg_index], 'o', label="wg", color="green", markersize=10)

    #sliders
    fig.subplots_adjust(bottom=0.25)

    ax_wion = fig.add_axes([0.1, 0.1, 0.2, 0.03])
    ax_wg = fig.add_axes([0.4, 0.1, 0.2, 0.03])

    wion_slider = Slider(ax = ax_wion, label = "wion index", valmin=0, valmax=len(w_data)-1, valinit=wion_index, valstep=1)
    wg_slider = Slider(ax = ax_wg, label = "wg index", valmin=0, valmax=len(w_data)-1, valinit=wg_index, valstep=1)

    if wnano is not None:
        wnano_index = np.where(w_data == wnano)[0][0]
        
        #line objects
        wnano_imp, = ax1.plot(impreal_data[wnano_index], impimag_data[wnano_index], 'o', label="wnano", color="pink", markersize=10)
        wnano_mag, = ax2.plot(w_data[wnano_index], mag_data[wnano_index], 'o', label="wnano", color="pink", markersize=10)
        wnano_phase, = twin.plot(w_data[wnano_index], phase_data[wnano_index], 'o', label="wnano", color="pink", markersize=10)

        ax_wnano = fig.add_axes([0.7, 0.1, 0.2, 0.03])

        wnano_slider = Slider(ax = ax_wnano, label = "wnano index", valmin=0, valmax=len(w_data)-1, valinit=wnano_index, valstep=1)

    #output variables
    wg_output = wg
    wion_output = wion
    wnano_output = wnano

    def update_wion(val):
        nonlocal wion_output #so output values can change when sliders are moved

        wion_imp.set_xdata([impreal_data[wion_slider.val]])
        wion_imp.set_ydata([impimag_data[wion_slider.val]])
        wion_mag.set_xdata([w_data[wion_slider.val]])
        wion_mag.set_ydata([mag_data[wion_slider.val]])
        wion_phase.set_xdata([w_data[wion_slider.val]])
        wion_phase.set_ydata([phase_data[wion_slider.val]])
        
        wion_output = w_data[wion_slider.val]

    def update_wg(val):
        nonlocal wg_output

        wg_imp.set_xdata([impreal_data[wg_slider.val]])
        wg_imp.set_ydata([impimag_data[wg_slider.val]])
        wg_mag.set_xdata([w_data[wg_slider.val]])
        wg_mag.set_ydata([mag_data[wg_slider.val]])
        wg_phase.set_xdata([w_data[wg_slider.val]])
        wg_phase.set_ydata([phase_data[wg_slider.val]])

        wg_output = w_data[wg_slider.val]
    
    def update_wnano(val):
        nonlocal wnano_output

        wnano_imp.set_xdata([impreal_data[wnano_slider.val]])
        wnano_imp.set_ydata([impimag_data[wnano_slider.val]])
        wnano_mag.set_xdata([w_data[wnano_slider.val]])
        wnano_mag.set_ydata([mag_data[wnano_slider.val]])
        wnano_phase.set_xdata([w_data[wnano_slider.val]])
        wnano_phase.set_ydata([phase_data[wnano_slider.val]])

        wnano_output = w_data[wnano_slider.val]

    wion_slider.on_changed(update_wion)
    wg_slider.on_changed(update_wg)

    if wnano is not None:
        wnano_slider.on_changed(update_wnano)
    else:
        wnano_output = None



    #axes styling
    ax1.set_title("Impedance spectra")
    ax1.set_ylabel("-Z''")
    ax1.set_xlabel("Z")
    ax1.set_ylim(0,)

    ax2.set_xscale('log')
    ax2.set_yscale('log')
    ax2.set_title("Resonance and bode plot")
    ax2.set_ylabel("|Z|")
    ax2.set_xlabel("w")

    ax1.legend()
    ax2.legend()
    twin.legend()

    plt.show()
    return wg_output, wion_output, wnano_output

def check_Rn(Rn0, Rninf, nyquist_data, Rs):
    """
    Checks Rn0 and Rninf guesses
    Accepts only bias data
    Args:
        Rn0 (float): Width of nyquist spectra under bias from Finder module
        Rninf (float): Width of first loop of nyquist spectra under bias from Finder module
        nyquist_data (array): Impedance data
        Rs (float): Series resistance
    Returns:
        Rn0_output (float): Checked Rn0 resistance
        Rninf_output (float): Checked Rninf resistance
    """
    #plotting data
    fig, (ax1, ax2) = plt.subplots(1, 2)

    w_data = nyquist_data[:,1]
    impreal_data = nyquist_data[:,2]
    impimag_data = nyquist_data[:,3]
    mag_data = abs(nyquist_data[:,2] + 1j*nyquist_data[:,3])

    ax1.plot(impreal_data, impimag_data, 'o', label="experimental impedance")
    ax2.plot(w_data, mag_data, 'o', label="measured |Z|", color="midnightblue")

    #Rn lines
    Rn0_index = np.where(impreal_data == Rn0 + Rs)[0][0]
    Rninf_index = np.where(impreal_data == Rninf + Rs)[0][0]

    #dummy data cuz vlines and hlines DONT HAVE SET METHODS WHYYYYY
    ybaka = np.linspace(0, np.max(impimag_data))
    xbaka = np.linspace(np.min(w_data), np.max(w_data))

    Rn0_imp, = ax1.plot(np.full_like(ybaka, impreal_data[Rn0_index]), ybaka, label="Rn0", color="red")
    Rninf_imp, = ax1.plot(np.full_like(ybaka, impreal_data[Rninf_index]), ybaka, label="Rninf", color="orange")

    Rn0_mag, = ax2.plot(xbaka, np.full_like(xbaka, mag_data[Rn0_index]), label="Rn0", color="red")
    Rninf_mag, = ax2.plot(xbaka, np.full_like(xbaka, mag_data[Rninf_index]), label="Rninf", color="orange")


    #sliders
    fig.subplots_adjust(bottom=0.25)

    ax_Rn0_slider = fig.add_axes([0.2, 0.1, 0.2, 0.03])
    ax_Rninf_slider = fig.add_axes([0.5, 0.1, 0.2, 0.03])

    Rn0_slider = Slider(ax = ax_Rn0_slider, label = "Rn0 index", valmin=0, valmax=len(w_data)-1, valinit=Rn0_index, valstep=1)
    Rninf_slider = Slider(ax = ax_Rninf_slider, label = "Rninf index", valmin=0, valmax=len(w_data)-1, valinit=Rninf_index, valstep=1)

    Rn0_output = Rn0
    Rninf_output = Rninf

    def update(val):
        nonlocal Rn0_output, Rninf_output

        Rn0_imp.set_xdata([np.full_like(ybaka, impreal_data[Rn0_slider.val])])
        Rninf_imp.set_xdata([np.full_like(ybaka, impreal_data[Rninf_slider.val])])

        Rn0_mag.set_ydata([np.full_like(xbaka, mag_data[Rn0_slider.val])])
        Rninf_mag.set_ydata([np.full_like(xbaka, mag_data[Rninf_slider.val])])

        #update output values
        Rn0_output = impreal_data[Rn0_slider.val] - Rs
        Rninf_output = impreal_data[Rninf_slider.val] - Rs

    Rn0_slider.on_changed(update)
    Rninf_slider.on_changed(update)


    #axes styling
    ax1.set_title("Impedance spectra")
    ax1.set_ylabel("-Z''")
    ax1.set_xlabel("Z")
    ax1.set_ylim(0,)

    ax2.set_xscale('log')
    ax2.set_yscale('log')
    ax2.set_title("Resonance and bode plot")
    ax2.set_ylabel("|Z|")
    ax2.set_xlabel("w")

    ax1.legend()
    ax2.legend()

    plt.show()

    return Rn0_output, Rninf_output

if __name__ == "__main__":
    # # reference cell
    # #loading data
    # IV_data = np.loadtxt("test_data/Pixel5ControlLightForwardsweep/CVafter.txt", skiprows=1)
    # bias_data = np.loadtxt("test_data/nyquist.txt", skiprows=1)
    # nobias_data = np.loadtxt("test_data/nyquist_dark.txt", skiprows=1)
    # Interface(bias_data, nobias_data, IV_data)

    # nanoparticles
    IV_data = np.loadtxt("test_data/Pixel1NanoparticlesLightForwardsweep/CVafter.txt", skiprows=1)
    bias_data = np.loadtxt("test_data/nyquist2.txt", skiprows=1)
    nobias_data = np.loadtxt("test_data/nyquist2_dark.txt", skiprows=1)
    Interface(bias_data, nobias_data, IV_data, nanoparticle=True)
