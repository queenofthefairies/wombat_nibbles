# this script plots diffraction data saved in xye format

####################################################################
# get relevant python packages
####################################################################
import numpy as np
import matplotlib as mpl 
import matplotlib.pyplot as plt
import matplotlib.colors as colors 
import pandas as pd 
import os

####################################################################
# READ THE DATA
####################################################################
# titles and names for figures
fig_filename = 'BaZrS3_high_temp_straightened'
fig1_title = r'BaZrS3 Wombat data. $\lambda = 2.41\,\,\AA$'
fig4_title = fig1_title
fig6_title = r'BaZrS3 peaks in straightened Wombat data. $\lambda = 2.41\,\,\AA$'

fig4 = 1 # parametric plot

# directory where the xye are
xye_dir = 'High_Temperature_Work/temperature_runs_40_mins_Straightened/'
# names of xye files in the above directory and the label for each when plotted
xye_file_list = [['WBT0099991_BaZrS3_at_300C_2p41Ang_straightened.xye', 300],
                 ['WBT0099994_BaZrS3_at_350C_2p41Ang_straightened.xye', 350],
                 ['WBT0099997_BaZrS3_at_400C_2p41Ang_straightened.xye', 400],
                 ['WBT0100000_BaZrS3_at_450C_2p41Ang_straightened.xye', 450],
                 ['WBT0100003_BaZrS3_at_500C_2p41Ang_straightened.xye', 500],
                 ['WBT0100006_BaZrS3_at_550C_2p41Ang_straightened.xye', 550],
                 ['WBT0100009_BaZrS3_at_600C_2p41Ang_straightened.xye', 600],
                 ['WBT0100012_BaZrS3_at_650C_2p41Ang_straightened.xye', 650],
                 ['WBT0100015_BaZrS3_at_700C_2p41Ang_straightened.xye', 700],
                 ['WBT0100018_BaZrS3_at_750C_2p41Ang_straightened.xye', 750],
                 ['WBT0100021_BaZrS3_at_800C_2p41Ang_straightened.xye', 800],
                 ['WBT0100024_BaZrS3_at_850C_2p41Ang_straightened.xye', 850],
                 ['WBT0100027_BaZrS3_at_900C_2p41Ang_straightened.xye', 900],
                 ['WBT0100030_BaZrS3_at_950C_2p41Ang_straightened.xye', 950],
                 ['WBT0100033_BaZrS3_at_1000C_2p41Ang_straightened.xye', 1000]
                 ]

# practical 2 theta limits
two_theta_min_to_plot = 18
two_theta_max_to_plot = 133

# parametric plot details
f4_y_axis_label = r'Temperature ($^\circ$C)'
f4_colourmap = 'plasma'

param_list = list(zip(*xye_file_list))[1]
print(param_list)
f4_y_axis_min = 275
f4_y_axis_max = 1025
f4_z_axis_colourmap_min = 7000
f4_z_axis_colourmap_max = 30000

# puts the data from each file into a dataframe and puts each dataframe into a list
# puts all labels into a list
xye_df_list = []
xye_label_list = []
for xye_file in xye_file_list:
    xye_file_name = xye_dir + xye_file[0]
    xye_df = pd.read_fwf(xye_file_name, infer_nrows = 700, skiprows = 1)
    xye_df_list.append(xye_df)
    xye_label_list.append(xye_file[1])

# list of colours to use in plotting
# default matplotlib colours
#colour_list = ['C0', 'C1', 'C2', 'C3', 'C4', 'C5' ]
# nicer colours
colour_list = ['#0D3B66','#F5A6E6','#4392F1','#EE6352', '#4ADBC8','#F3A712']


####################################################################
# FIG 4: parametric plot
####################################################################
if fig4:
    # make figure
    fig_width = 20 # this is in inches
    fig_height = 10.5 # this is in inches
    # make a figure called fig1, with an axes called ax1
    fig4, ax4 = plt.subplots(nrows = 1, ncols = 1, 
                            figsize=(fig_width, fig_height))

    # set up colourmap
    norm = colors.Normalize(vmin=f4_z_axis_colourmap_min, 
                            vmax=f4_z_axis_colourmap_max)
    
    two_theta_min = 10
    two_theta_max = 120
    # make array to plot
    for i in range(len(xye_df_list)):
        xye_df = xye_df_list[i]
        xye_df = xye_df.loc[(xye_df['Angle'] > two_theta_min_to_plot) & (xye_df['Angle'] < two_theta_max_to_plot)]
        xye_intensity = xye_df['Intensity'].to_numpy()
        number_of_two_theta_bins = len(xye_intensity)
        xye_intensity = np.reshape(xye_intensity, (1, number_of_two_theta_bins))
        if i == 0:
            xye_array = xye_intensity
            two_theta_min = xye_df['Angle'].min()
            two_theta_max = xye_df['Angle'].max()
        else:
            xye_array = np.concatenate((xye_array, xye_intensity), axis=0)
        print(xye_array.shape)
    xye_array_flipped = np.flip(xye_array, axis = 0) # flip vertically 
    wom_colourplot = ax4.imshow(xye_array_flipped, norm=norm, cmap = f4_colourmap, aspect = 'auto',
                                extent = (two_theta_min, two_theta_max, 
                                f4_y_axis_min, f4_y_axis_max))
    for j in range(len(param_list)):
        ax4.hlines(xmin=two_theta_min, xmax=two_theta_max, y=param_list[j]-25, color = 'w', ls = '-', lw = 0.5, zorder = 15)
    # Label axes
    ax4.set_xlabel(r'$2 \theta \,\, (^\circ)$', fontsize = 12)
    ax4.set_ylabel(f4_y_axis_label, fontsize = 12) 
    # # legend
    # ax1.legend(ncol=1, loc ='upper left', fontsize=10) 
    ax4.set_yticks(param_list)
    # # title for main axes
    ax4.set_title(fig4_title)  
    cbar = fig4.colorbar(wom_colourplot, shrink = 0.7)
    cbar.set_label('Intensity (arb. units)')
    # # title for main axes
    ax4.set_title(fig4_title)  
    # save figure (always do this before show)
    # bbox_inches='tight' minimises white space around plot when it's saved
    plt.savefig(fig_filename+'_param_plot.png',bbox_inches='tight',dpi=300)
    # # then show figure in window
    plt.show()
    print('done figure {0}'.format(fig_filename+'_param_plot.png'))
    print()

