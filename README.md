# perovskite-transistor-circuit-model
## Overview
This program plots and fits impedance spectroscopy data of perovskite solar cells using an ionic-amplification model[1]. <br/>

## Installation and use
Click the green "<>Code" button, download, and run User_Interface.py. <br/>
The following modules may have to be downloaded in advance: numpy, matplotlib, scipy, pandas, tkinter, customtkinter (This can be done by typing "pip install (module name)" in the commmand line)

## Data formatting
Imported data files are to be in .csv format with the following requirements
### Impedance data
| Index | Angular frequency | Real part of impedance | Imaginary part of impedance |
|-------|-------------------|------------------------|-----------------------------|

### Current voltage data
| Index | ... | ... | Current | Potential |
|-------|-----|-----|---------|-----------|

### OCP data
| Index | ... | ... | ... | ... | OCP value |
|-------|-----|-----|-----|-----|-----------|

## References
1) 	Energy Environ. Sci., 2019,12, 1296-1308. Ionic-to-electronic current amplification in hybrid perovskite solar cells: ionically gated transistor-interface circuit model explains hysteresis and impedance of mixed conducting devices. Available at: https://pubs.rsc.org/en/content/articlelanding/2019/ee/c8ee02362j
