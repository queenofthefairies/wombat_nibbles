# Make images from each step in Wombat som scan

import h5py
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import csv

# get data
data_dir = 'hdf/'
files_list = ['WBT0103525.nx.hdf','WBT0103526.nx.hdf']

# figure formatting
fig_width = 8 # this is in inches
fig_height = 4 # this is in inches
plot_x_label = 'Detector horizontal pixel'
plot_x_min = 0 
plot_x_max = 967
plot_y_label = 'Detector vertical pixel'
plot_y_min = 0 
plot_y_max = 967
# set up colourmap
f1_colourmap = 'plasma'
colourmap_min = 0
colourmap_max = 300
norm = colors.Normalize(vmin=colourmap_min, 
                        vmax=colourmap_max)
#norm = colors.LogNorm(vmin=f6_z_axis_colourmap_min, vmax=f6_z_axis_colourmap_max, clip=False)

for j in range(len(files_list)):
    run_number = files_list[j][0:10]
    file_path = data_dir + files_list[j]
    with h5py.File(file_path, 'r') as f:
        image_dataset = f['entry1/data/hmm_xy']
        no_steps = len(image_dataset)
        step_var_name = 'som'
        step_var = f['entry1/sample/rotate']
        for i in range(no_steps):
            image_array = image_dataset[i]
            step_var_value = step_var[i]
            # make a figure called fig1, with an axes called ax1
            fig1, ax1 = plt.subplots(nrows = 1, ncols = 1, 
                                     figsize=(fig_width, fig_height))
            wom_colour_plot = ax1.imshow(image_array, norm=norm, cmap = f1_colourmap, aspect = 'auto',
                                         extent = (plot_x_min, plot_x_max, 
                                         plot_y_min, plot_y_max))
            cbar = fig1.colorbar(wom_colour_plot, shrink = 0.7)
            cbar.set_label('Intensity (arb. units)')
            ax1.set_xlabel(plot_x_label)
            ax1.set_ylabel(plot_y_label)
            plt.title("{0}: {1} step {2}/{3}".format(run_number,step_var_name,i,no_steps))
            fig_file_name = run_number + '_{0}_{1:.0f}_detector.png'.format(step_var_name,step_var_value)
            # save figure (always do this before show)
            # bbox_inches='tight' minimises white space around plot when it's saved
            plt.savefig(fig_filename,bbox_inches='tight',dpi=300)
            plt.show()

            # write text file
            output_file_name = run_number + '_{0}_{1:.0f}_detector.txt'.format(step_var_name,step_var_value)
            with open(output_file_name, 'w') as g:
                csv.writer(g, delimiter=' ').writerows(image_array)
            print('done {0}'.format(output_file_name))