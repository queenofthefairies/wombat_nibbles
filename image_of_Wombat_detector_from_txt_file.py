# Make images from each step in Wombat som scan

import h5py
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import csv
import pandas as pd

my_text_file = 'helen_102740.txt'

image_df = pd.read_csv(my_text_file,sep='\t', skiprows = 5, names = ['Y', 'two theta', 'Intensity'])
print(image_df)
image_array = image_df['Intensity'].to_numpy()
print(image_array.shape)
image_array = np.reshape(image_array, (975,128))
image_array = np.transpose(image_array)
print(image_array.shape)

y_axis_min = 0
y_axis_max = 200

colourmap_min = 200
colourmap_max = 280

two_theta_min = image_df['two theta'].min()
two_theta_max = image_df['two theta'].max()

fig_filename='Wombat_propane_plot_for_paper.png'
# set up colourmap
f1_colourmap = 'plasma'
norm = colors.Normalize(vmin=colourmap_min, 
                        vmax=colourmap_max)
#norm = colors.LogNorm(vmin=f6_z_axis_colourmap_min, vmax=f6_z_axis_colourmap_max, clip=False)
# make figure
fig_width = 8 # this is in inches
fig_height = 4 # this is in inches
# make a figure called fig1, with an axes called ax1
fig1, ax1 = plt.subplots(nrows = 1, ncols = 1, 
                         figsize=(fig_width, fig_height))
wom_colour_plot = ax1.imshow(image_array, norm=norm, cmap = f1_colourmap, aspect = 'auto',
                             extent = (two_theta_min, two_theta_max, 
                             y_axis_min, y_axis_max))
cbar = fig1.colorbar(wom_colour_plot, shrink = 0.7)
cbar.set_label('Intensity (arb. units)')
ax1.set_xlabel(r'2$\theta$ ($^\circ$)')
ax1.set_ylabel('Detector vertical position (mm)')
#plt.title("Image from HDF5")
# save figure (always do this before show)
# bbox_inches='tight' minimises white space around plot when it's saved
plt.savefig(fig_filename,bbox_inches='tight',dpi=300)
plt.show()

print('done {0}'.format(fig_filename))