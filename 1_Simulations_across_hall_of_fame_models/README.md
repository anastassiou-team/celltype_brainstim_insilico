# Necessary data, algorithms, and results for main **Figure 5 a-b**, and supplementary **Figure S8**.

### Contents
* **Six almost identical directories** for the two cell types used (**3 for Pvalb A and 3 for Pyramidal A**), each containing the following:
    * **Plots** directory contains the *04_Plot_results.py* script which creates low-level rose-plots for each simulation, as well as the created figures. For the two cases where all hall of fame models are simulated (see below), this script will also export vector-length metrics across models in *Results* directory.
    * **required_files** directory contains necessary parameter, morphology, and mod files, as well as the *Simulation_(Main).py* script which is called for each simulation.
    * **MultiRun.bat** windows batch file, which will set and run all simulations.
    * **Results** directory will contain raw simulation data after successful run of *MultiRun.bat*.
    * **01_Set_up.py**, **02_Gather_Data.py** and **03_Erase_files.py** scripts are called by *MultiRun.bat*.
* **Combined_plots** directory contains scripts for the final figures' creation and the corresponding created figures (**Script name** - Description - ***Output figure file***).
    * **0_Plot traces.py** - Plots spiking traces as shown in main *Figure 5 a* - ***0_Traces.pdf***
    * **1_Plot_RoseHists_and_stats.py** - Plots rose histograms as shown in main *Figure 5 a* and supplementary *Figure S9 a-b*, as well as ISI distributions as shown in main *Figure 5 a*, and vector-length/p-value plots as shown in supplementary *Figure S9 a-b* - ***1_RoseHists_and_stats.pdf***
    * **2_Plot_across_HOF.py** - Plots vector-length vs spike-rate figures as shown in main *Figure 5 b (top)* and supplementary *Figure S9 c-d*, as well as spike-rate vs injected current figures as shown in supplementary *Figure S9 c-d* - ***2_Across_HOF.pdf***
***
**MultiRun.bat** windows batch file is the main script which will set and run all simulations.
* For **Pvalb A** at **8** and **30 Hz**, *333* simulations will run for different intracellular current injections (200-1200 pA, step = 3 pA), x2 with and without ES, only for *hall of fame model #0*.
* For **Pvalb A** at **140 Hz**, *333* simulations will run for different intracellular current injections (200-1200 pA, step = 3 pA), x2 with and without ES, x40 *hall of fame models (#0-39)*.
* For **Pyramidal A** at **8 Hz**, *316* simulations will run for different intracellular current injections (50-1000 pA, step = 3 pA), x2 with and without ES, x40 *hall of fame models (#0-39)*.
* For **Pyramidal A** at **30** and **140 Hz**, *316* simulations for different intracellular current injections (50-1000 pA, step = 3 pA), x2 with and without ES, only for *hall of fame model #0*.

> Simulations run in parallel, 16 at a time. Parameters such as simulation duration, probe locations or noise can be changed in the **Simulation_(Main).py** script in each **required_files** directory. After successful run of all six **MultiRun.bat** windows batch files and **04_Plot_results.py** scripts, you will find the main analyses and figure creating scripts in the **Combined_plots** directory.
***