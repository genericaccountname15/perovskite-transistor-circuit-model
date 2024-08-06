"""
Plots the impedance spectra, resonance and bode plots of impedance functions
Generates sliders for initial params

Timothy Chew
6/8/24
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from single_transistor_model.Impedancefunction import Z

#get phase of complex number
def arg(z):
    return np.arctan2(z.imag, z.real)

df = pd.read_csv("single_transistor_model\Initial_params.csv", delimiter=",")
init_params = df.values

#initialising values and figures
init_values = init_params[:,1]
w = np.logspace(-2,6,500)
fig, (ax1, ax2) = plt.subplots(1, 2)
twin = ax2.twinx()

line1, = ax1.plot(Z(w, *init_values).real, 
                -1*Z(w, *init_values).imag, 
                label="model impedance")

line2, = ax2.plot(w, abs(Z(w, *init_values)), label="model |Z|", color="blue")
line3, = twin.plot(w, arg(Z(w, *init_values)), label="model arg(Z)", color="red")

#list of axes positions
axes_pos = [[0.10, 0.15, 0.2, 0.03],
            [0.10, 0.1, 0.2, 0.03],
            [0.10, 0.05, 0.2, 0.03],
            [0.40, 0.15, 0.2, 0.03],
            [0.40, 0.1, 0.2, 0.03],
            [0.40, 0.05, 0.2, 0.03],
            [0.7, 0.15, 0.2, 0.03],
            [0.7, 0.1, 0.2, 0.03],
            [0.7, 0.05, 0.2, 0.03]]

#generate sliders
sliders = [] #array of slider objects
i = 0

for j in range(len(init_params)):
    if init_params[j,2]:
        slider_axis = fig.add_axes(axes_pos[i])
        valinit = init_values[i]
        sliders.append(Slider(ax=slider_axis, label=init_params[i,0], valmin=valinit/10, valmax=valinit*10, valinit=valinit))
        i += 1        

#adjust position of figure
fig.subplots_adjust(bottom=0.25)

#making graphs pretty
fig.suptitle("Simple ionic-electronic model")

ax1.set_title("Impedance spectra")
ax1.set_ylabel("-Z''")
ax1.set_xlabel("Z")

ax2.set_xscale('log')
ax2.set_yscale('log')
ax2.set_title("Resonance and bode plot")
ax2.set_ylabel("|Z|")
ax2.set_xlabel("w")

twin.set_ylabel("Phase")

print(sliders)
#plt.show()