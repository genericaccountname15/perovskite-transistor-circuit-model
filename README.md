# perovskite-transistor-circuit-model
## Overview
This program was built as part of a summer project to develop a circuit model for perovskite solar cells when nanoparticles 
were added between the perovskite/ETL interfaces. It uses a modified ionic-amplification model[1] with an additional RC
circuit in the electronic branch to simulate the effect of nanoparticles, generating simulated impedance spectroscopy data. <br/>

The experimental data used for software development were obtained using Nova 2.1, so the imported data files expect similar formatting.
More details in **Data formatting**.<br/>

The software's plotting features includes support for other circuit models; however, the fitting system only works for the built-in 
ionic amplification model and the modified nanoparticles model.


## Installation and use
Click the green "<>Code" button, download, and run **User_Interface.py**. <br/>
The following modules may have to be downloaded in advance: numpy, matplotlib, scipy, pandas, tkinter, customtkinter _(This can be done by typing "pip install (module name)" in the command line)_. <br/>

![image](https://github.com/user-attachments/assets/a762b427-384b-481b-ba4b-de4053b17362)
_Diagram of user interface. Note that the "Run Checker checkbox" only works for the built-in models._


## Data formatting
Imported data files are to be in .csv format in the following format:
### Impedance data
| Index | Angular frequency | Real part of impedance | Imaginary part of impedance |
|-------|-------------------|------------------------|-----------------------------|

### Current-voltage data
| Index | ... | ... | Current | Potential |
|-------|-----|-----|---------|-----------|

### OCP data
| Index | ... | ... | ... | ... | OCP value |
|-------|-----|-----|-----|-----|-----------|

_Current-voltage and OCP data files are optional, if an OCP file is not included you will be prompted to enter a bias voltage value into the terminal_

## Importing your own model
Imported models require:
- a python file which contains the impedance function in the form: __Z(w, *params)__ with filename: **Impedancefunction.py**
- a csv file which contains the initial parameters with filename: **Initial_params.csv** with comma delimiters

| parameter name | value | slider | log |
|---|---|---|---|
| Name of parameter (string) | value (float) | Create slider (boolean) | Create logarithmic slider (boolean) |

_Format of Initial_params.csv_


## Example use

## References
1) 	Energy Environ. Sci., 2019,12, 1296-1308. Ionic-to-electronic current amplification in hybrid perovskite solar cells: ionically gated transistor-interface circuit model explains hysteresis and impedance of mixed conducting devices. Available at: https://pubs.rsc.org/en/content/articlelanding/2019/ee/c8ee02362j
