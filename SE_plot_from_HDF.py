# this script plots diffraction data saved in xyd format

####################################################################
# get relevant python packages
####################################################################
import numpy as np
import matplotlib as mpl 
import matplotlib.pyplot as plt 
import pandas as pd 
import h5py

####################################################################
# READ THE DATA
####################################################################
# titles and names for figures
fig_filename = 'xyd_straightened_background_subtraction'
fig1_title = r'Echidna data straightened, background subtracted. $\lambda = 2.44\,\,\AA$'

HDF_file_name = 'WBT0108059.nx.hdf'
# get data
f = h5py.File(HDF_file_name, 'r')

tempC = f['entry1/sample/tc1/sensor/sensorValueC'][:]


# list of colours to use in plotting
# default matplotlib colours
#colour_list = ['C0', 'C1', 'C2', 'C3', 'C4', 'C5' ]
# nicer colours
colour_list = ['#0D3B66','#F5A6E6','#4392F1','#EE6352', '#4ADBC8','#F3A712']
####################################################################
# FIG 1: plot of xyd data
####################################################################
if fig1:
    # make figure
    fig_width = 10 # this is in inches
    fig_height = 5.5 # this is in inches
    # make a figure called fig1, with an axes called ax1
    fig1, ax1 = plt.subplots(nrows = 1, ncols = 1, 
                            figsize=(fig_width, fig_height))
    for i in range(len(xyd_df_list)):
        xyd_df = xyd_df_list[i]
        xyd_label = xyd_label_list[i]
        ax1.errorbar(xyd_df['Angle'], 
                     xyd_df['Intensity']-background_xyd_df['scaled intensity'],
                     yerr=xyd_df['Error'],
                    label = xyd_label, color = colour_list[i])
        print('plotted {0}'.format(xyd_label))
    # Label axes
    ax1.set_xlabel(r'$2 \theta$', fontsize = 12)
    ax1.set_ylabel('Intensity (arb. units)', fontsize = 12) 
    # legend
    ax1.legend(ncol=1, loc ='upper left', fontsize=10) 
    # title for main axes
    ax1.set_title(fig1_title)  
    # save figure (always do this before show)
    # bbox_inches='tight' minimises white space around plot when it's saved
    plt.savefig(fig_filename+'_plot.png',bbox_inches='tight',dpi=300)
    # then show figure in window
    plt.show()
    print('done figure {0}'.format(fig_filename+'_plot.png'))
    print()

    # make figure ZOOMED IN
    fig_width = 20 # this is in inches
    fig_height = 5.5 # this is in inches
    # make a figure called fig1, with an axes called ax1
    fig1, ax1 = plt.subplots(nrows = 1, ncols = 1, 
                            figsize=(fig_width, fig_height))
    for i in range(len(xyd_df_list)):
        xyd_df = xyd_df_list[i]
        xyd_label = xyd_label_list[i]
        ax1.errorbar(xyd_df['Angle'], 
                     xyd_df['Intensity']-background_xyd_df['scaled intensity'],
                     yerr=xyd_df['Error'],
                     label = xyd_label, color = colour_list[i])
    # Label axes
    ax1.set_xlabel(r'$2 \theta$', fontsize = 12)
    ax1.set_ylabel('Intensity (arb. units)', fontsize = 12) 
    # legend
    ax1.legend(ncol=1, loc ='upper right', fontsize=10) 
    # title for main axes
    ax1.set_title(fig1_title)  
    ax1.set_ylim(roi_intensity_min,roi_intensity_max)
    ax1.set_xlim(roi_2theta_min,roi_2theta_max)
    # save figure (always do this before show)
    # bbox_inches='tight' minimises white space around plot when it's saved
    plt.savefig(fig_filename+'_plot_zoomed.png',bbox_inches='tight',dpi=300)
    # then show figure in window
    plt.show()
    print('done figure {0}'.format(fig_filename+'_plot_zoomed.png'))
    print()



