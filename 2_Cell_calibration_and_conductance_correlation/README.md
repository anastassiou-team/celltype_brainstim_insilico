# Necessary data, algorithms and results for main **Figure 5 c**, and supplementary **Figure S9**.
***
### Contents
* **Four almost identical directories** for the 2 Pvalb and 2 Pyramidal cells used (**Pvalb A, Pvalb B,
Pyramidal A, Pyramidal B**), each containing the following:
    * **1_Supplemental** directory contains two simulation scripts, which will set up and run two simulations for a high and a low current injection for comparison with experimental spike-trains, as shown in supplementary *Figure S9*.
    * **2_Calibrate** directory implements a perturb and observe algorithm, which will calibrate all 40 hof models to the same state (spike rate distribution). The algorithm runs through *RunAll.py*, which will call the *00_Initialize.py*, *01_Set_up.py*, *02_Generate.py* and *03_Erase_files.py* scripts. *Calibrated.csv* will contain the optimized mean and std current injections for each hof model.
    * **3_Correlate** directory contains the *01_Set_up.py*, *02_Gather_Data.py* and *03_Erase_files.py* scripts which are called by the *MultiRun.bat* windows batch file. Run of the *MultiRun.bat* file will give the raw simulation outputs for the calibrated simulations of all hall of fame models.
* **Combined_plots** directory contains scripts for the final figures' creation and the corresponding created figures (**Script name** - Description - ***Output figure file***).
    * **0_Plot traces.py** - Plots spiking traces as shown in supplemental *Figure S8*. The script will seek for experimental data file (".nwb" file) whithin each *1_Supplemental* directory. You need to download the corresponding file for each cell model from the *Allen Brain Map* portal https://celltypes.brain-map.org/ - ***0_Traces.pdf***
    * **1_Plot_Correlations_and_stats.py** - Plots individual vector lengths per hof model and correlation heatmaps as shown in main *Figure 5 c* and conductance distribution heatmaps as shown in supplementary *Figure S8*.  - ***1_Vector_lengths.pdf***, ***1_Correlations.pdf*** and ***1_Conductances.pdf***. Separate files for each model (PVA, PVB, PYA, PYB for Pvalb A, Pvalb B, Pyramidal A, Pyramidal B, respectively.
***