# Wombat data analysis and visualisation code snippets
These scripts are NOT a cogent python package but rather a starting point for basic data analysis and making plots quickly. Some scripts are also applicable to data from Echidna. 

The powder data reduction routine developed by James Hester for Echidna and Wombat is described in [this paper](https://doi.org/10.1107/S1600576718014048) and the current Wombat powder data reduction routine is available from the [Gumtree/Wombat_scripts](https://github.com/Gumtree/Wombat_scripts) github repository.

For looking at single crystal data, try [WombatDMCpy](https://github.com/queenofthefairies/Wombat_DMCpy/tree/wombat_WIP).

## List of scripts

- `xyd_plotter_background_subtraction.py`: Example of plotting diffractograms in XYD format and doing a background/paramagnetic phase subtraction
- `xye_parametric_plot.py`: Plots diffractograms stacked with two theta on X axis, parameter such as sample stage angle/field/temperature on Y axis, intensity represented by colour/Z axis.
- `xye_peak_plotter.py`: Plots peak positions extracted from diffractograms to enable signal to be picked out visually against higher background.
- `XYE_sum.py`: Sums GSAS-II xye files together. 
- `image_of_Wombat_detector_from_txt_file.py`: Input: a txt file with 3 columns: Y, X (two theta), intensity. Output: a plot of the detector image.  
- `image_from_each_step_Wombat.py`: Input: HDF file with multiple steps. Output: a detector image and a text file of detector data for each step (not in terms of two theta).
- `Wombat_box_integration.py`: Sums intensity within a rectangular subsection of the Wombat area detector. 







 

