"""
Plots the impedance spectra, resonance and bode plots of impedance functions
Generates sliders for initial params

Timothy Chew
6/8/24
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons
from nanoparticles_model.Impedancefunction import Z

#get phase of complex number
def arg(z):
    return np.arctan2(z.imag, z.real)

df = pd.read_csv("nanoparticles_model\Initial_params.csv", delimiter=",")
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

line2a, = ax2.plot(w, Z(w, *init_values).real, label="model Z'", color="green", visible=False)
line2b, = ax2.plot(w, -1*Z(w, *init_values).imag, label = 'model -Z"', color="purple", visible=False)
line2c, = ax2.plot(w, (1/(Z(w, *init_values)).imag * 1/w), label = "model capacitance", color="orange", visible=False)

lines_by_labels = {l.get_label(): l for l in [line2, line2a,line2b,line2c]}
line_colors = [l.get_color() for l in lines_by_labels.values()]

#adjust position of figure
fig.subplots_adjust(bottom=0.25)

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

axes_pos = [[0.07, 0.15, 0.07, 0.03],
            [0.07, 0.1, 0.07, 0.03],
            [0.07, 0.05, 0.07, 0.03],
            [0.32, 0.15, 0.07, 0.03],
            [0.32, 0.1, 0.07, 0.03],
            [0.32, 0.05, 0.07, 0.03],
            [0.57, 0.15, 0.07, 0.03],
            [0.57, 0.1, 0.07, 0.03],
            [0.57, 0.05, 0.07, 0.03],
            [0.82, 0.15, 0.07, 0.03],
            [0.82, 0.1, 0.07, 0.03],
            [0.82, 0.05, 0.07, 0.03]]

ax_storage = [0.1, 0.9, 0.07, 0.03] #hidden slider location

#generate sliders
sliders = [] #array of slider objects
slider_axes = [] #array of slider axes objects

log_sliders = [] #array of logscale slider objects
log_slider_axes = [] #array of logscale slider axes objects
i = 0 #index for axes positions

for j in range(len(init_params)):
    #check if we want a slider for this value
    if init_params[j,2]:
        slider_axes.append(fig.add_axes(axes_pos[i]))
        valinit = init_values[j]
        sliders.append(Slider(ax=slider_axes[j], label=init_params[j,0], valmin=valinit/10, valmax=valinit*10, valinit=valinit))
        i += 1 
    else:
        #append value if not placing a slider
        slider_axes.append("None")
        sliders.append(init_values[j])

    #check if we want a log slider for this value
    if init_params[j,3]:
        log_slider_axes.append(fig.add_axes(ax_storage))
        log_sliders.append(Slider(ax=log_slider_axes[j], label=init_params[j,0], valmin=-16, valmax=7, valinit=init_values[j], dragging=False))
    else:
        log_slider_axes.append("None")
        log_sliders.append(init_values[j])


#toggling logscale
togglelog_ax = fig.add_axes([0.05, 0.75, 0.04, 0.02])
togglelog_button = Button(togglelog_ax, "Logscale", hovercolor="0.975")

logscale = False #boolean logscale state

def toggle_logscale(event):
    global logscale
    for j in range(len(init_params)):
        #check if it has a log slider
        if logscale:
            if init_params[j,3]:
                log_val = 10 ** (log_sliders[j].val)
                log_slider_axes[j].clear()
                slider_axes[j].clear()
                sliders[j] = Slider(ax=slider_axes[j], label=init_params[j,0], valmin=log_val/10, valmax=log_val*10, valinit=log_val)
                log_sliders[j] = Slider(ax=log_slider_axes[j], label="log"+init_params[j,0], 
                                        valmin=round(np.log10(log_val))-4, valmax=round(np.log10(log_val))+4, valinit=np.log10(log_val))
                sliders[j].on_changed(update)
                log_sliders[j].on_changed(update)
        else:
            if init_params[j,3]:
                lin_val = sliders[j].val
                log_slider_axes[j].clear()
                slider_axes[j].clear()
                sliders[j] = Slider(ax=log_slider_axes[j], label=init_params[j,0], valmin=lin_val/10, valmax=lin_val*10, valinit=lin_val)
                log_sliders[j] = Slider(ax=slider_axes[j], label="log"+init_params[j,0], 
                                        valmin=round(np.log10(lin_val))-4, valmax=round(np.log10(lin_val))+4, valinit=np.log10(lin_val))
                sliders[j].on_changed(update)
                log_sliders[j].on_changed(update)
    
    #flipper
    if logscale:
        logscale = False
    else:
        logscale = True
    
togglelog_button.on_clicked(toggle_logscale)


#update using sliders
def update(val):
    param_list_updated = []
    for slider in sliders:
        if isinstance(slider, float):
            param_list_updated.append(slider)
        else:
            param_list_updated.append(slider.val)

    line1.set_xdata(Z(w, *param_list_updated).real)
    line1.set_ydata(-1*Z(w, *param_list_updated).imag)
    line2.set_ydata(abs(Z(w, *param_list_updated)))
    line3.set_ydata(arg(Z(w, *param_list_updated)))
    fig.canvas.draw_idle()

def update(val):
    param_list_updated = []
    if logscale:
        for i in range(len(init_params)):
            if init_params[i,3]:
                param_list_updated.append(log_sliders[i].val)
            elif isinstance(sliders[i], float):
                param_list_updated.append(sliders[i])
            else:
                param_list_updated.append(sliders[i].val)
    else:
        for slider in sliders:
            if isinstance(slider, float):
                param_list_updated.append(slider)
            else:
                param_list_updated.append(slider.val)

    padding = 0.1
    #adjust limits
    ax1.set_xlim(min(line1.get_xdata()) * (1-padding), max(line1.get_xdata()) * (1+padding))
    ax1.set_ylim(min(line1.get_ydata()) * (1-padding), max(line1.get_ydata()) * (1+padding))
    ax2.set_xlim(min(line2.get_xdata()) * (1-padding), max(line2.get_xdata()) * (1+padding))
    ax2.set_ylim(min(line2.get_ydata()) * (1-padding), max(line2.get_ydata()) * (1+padding))
    twin.set_xlim(min(line3.get_xdata()) * (1-padding), max(line3.get_xdata()) * (1+padding))
    twin.set_ylim(min(line3.get_ydata()) * (1-padding), max(line3.get_ydata()) * (1+padding))


    line1.set_xdata(Z(w, *param_list_updated).real)
    line1.set_ydata(-1*Z(w, *param_list_updated).imag)
    line2.set_ydata(abs(Z(w, *param_list_updated)))
    line3.set_ydata(arg(Z(w, *param_list_updated)))
    fig.canvas.draw_idle()

#call on sliders when moved
for slider in sliders:
    if not isinstance(slider, float):
        slider.on_changed(update)

for log_slider in log_sliders:
    if not isinstance(log_slider, float):
        log_slider.on_changed(update)



#buttons
#resets sliders
reset_ax = fig.add_axes([0.05, 0.8, 0.03, 0.02])
reset_button = Button(reset_ax, "Reset", hovercolor="0.975")

def reset(event):
    for slider in sliders:
        if not isinstance(slider, float):
            slider.reset()
reset_button.on_clicked(reset)

#Checkboxes
plots_ax = fig.add_axes([0, 0.5, 0.12, 0.1])
plots_check = CheckButtons(ax = plots_ax, 
                           labels=lines_by_labels.keys(),
                           actives=[l.get_visible() for l in lines_by_labels.values()],
                            label_props={'color': line_colors},
                            frame_props={'edgecolor': line_colors},
                            check_props={'facecolor': line_colors}
                            )

def display_plots(label):
    ln = lines_by_labels[label]
    ln.set_visible(not ln.get_visible())
    ln.figure.canvas.draw_idle()

plots_check.on_clicked(display_plots)

#log and fix buttons
button_axes_pos = [[0.2, 0.15, 0.02, 0.03],
                   [0.2, 0.1, 0.02, 0.03],
                   [0.2, 0.05, 0.02, 0.03],
                   [0.45, 0.15, 0.02, 0.03],
                   [0.45, 0.1, 0.02, 0.03],
                   [0.45, 0.05, 0.02, 0.03],
                   [0.68, 0.15, 0.02, 0.03],
                   [0.68, 0.1, 0.02, 0.03],
                   [0.68, 0.05, 0.02, 0.03],
                   [0.93, 0.15, 0.02, 0.03],
                   [0.93, 0.1, 0.02, 0.03],
                   [0.93, 0.05, 0.02, 0.03]]

#test log slider
# ax_test2 = fig.add_axes([0.05, 0.6, 0.1, 0.02])
# ax_test3 = fig.add_axes([0.05, 0.5, 0.1, 0.02])
# log_slider = Slider(ax_test2, "log", valmin=-8, valmax=2, valinit=init_values[1])
# lin_slider = Slider(ax_test3, "lin", valmin=0, valmax=10, valinit=init_values[1])

# def update_log(val):
#     amp = 10 ** (log_slider.val)
#     amp = f"{amp:.{3}g}"
#     log_slider.valtext.set_text(amp)
# log_slider.on_changed(update_log)

# ax_test = fig.add_axes([0.2, 0.15, 0.02, 0.03])
# togglelog_button = Button(ax_test, "log", hovercolor="0.975")

# logscale = True
# def swaplog(event):
#     global log_slider, lin_slider, logscale
#     log_val = 10 ** (log_slider.val)
#     lin_val = lin_slider.val
#     if logscale:
#         ax_test2.clear()
#         ax_test3.clear()
#         lin_slider = Slider(ax_test3, "lin", valmin=log_val/10, valmax=log_val*10, valinit=log_val)
#         log_slider = Slider(ax_test2, "log", valmin=-8, valmax=2, valinit=np.log10(log_val))
#         logscale = False
#     else:
#         ax_test2.clear()
#         ax_test3.clear()
#         lin_slider = Slider(ax_test2, "lin", valmin=lin_val/10, valmax=lin_val*10, valinit=lin_val)
#         log_slider = Slider(ax_test3, "log", valmin=-8, valmax=2, valinit=np.log10(lin_val))
#         logscale = True

# togglelog_button.on_clicked(swaplog)





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

plt.show()