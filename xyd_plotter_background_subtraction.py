# this script plots diffraction data saved in xyd format

####################################################################
# get relevant python packages
####################################################################
import numpy as np
import matplotlib as mpl 
import matplotlib.pyplot as plt 
import pandas as pd 

####################################################################
# READ THE DATA
####################################################################
# titles and names for figures
fig_filename = 'xyd_straightened_background_subtraction'
fig1_title = r'Echidna data straightened, background subtracted. $\lambda = 2.44\,\,\AA$'
fig2_title = r'Echidna data, background subtracted . $\lambda = 2.44\,\,\AA$'
fig3_title = r'Echidna data, difference with  data. $\lambda = 2.44\,\,\AA$'

fig1 = 1 # raw data plot
fig2 = 1 # diff plot
fig3 = 1 # super plot

roi_2theta_min = 5
roi_2theta_max = 90

roi_intensity_min = 600
roi_intensity_max = 3500

# directory where the xyd are
xyd_dir = '25.01.20 NiMoO4 Data (3h) Straightened/'
# names of xyd files in the above directory and the label for each when plotted
xyd_file_list = [['ECH0035209_NiMoO4_30K_0T_straightened.xyd', '30 K, 0 T'],
                 ['ECH0035210_NiMoO4_2p2K_0T_straightened.xyd', '2.2 K, 0 T'],
                 ['ECH0035212_NiMoO4_2p2K_straightened.xyd', '2.2 K, 3 T'],
                 ['ECH0035211_NiMoO4_2p2K_straightened.xyd', '2.2 K, 8 T'],
                 ['ECH0035213_NiMoO4_2p2K_straightened.xyd', '2.2 K, 0 T, oriented'],
                 ['ECH0035214_NiMoO4_30K_0T_oriented_straightened.xyd', '30 K, 0 T, oriented']]

# puts the data from each file into a dataframe and puts each dataframe into a list
# puts all labels into a list
xyd_df_list = []
xyd_label_list = []
for xyd_file in xyd_file_list:
    xyd_file_name = xyd_dir + xyd_file[0]
    xyd_df = pd.read_fwf(xyd_file_name, infer_nrows = 2000, skiprows = 7)
    xyd_df_list.append(xyd_df)
    xyd_label_list.append(xyd_file[1])

################### BACKGROUND DF
background_xyd_file_name = '25.01.19 Background Measurements/ECH0035207_empty_magnet_20K_background_2.xyd'
background_xyd_df = pd.read_fwf(background_xyd_file_name, infer_nrows = 2000, skiprows = 7)
background_scale_factor = 191/130 
background_xyd_df['scaled intensity']=background_scale_factor*background_xyd_df['Intensity']

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



####################################################################
# FIG 2: diff plot
####################################################################
if fig2:
    # make figure
    fig_width = 20 # this is in inches
    fig_height = 10 # this is in inches
    # make a figure called fig2, with an axes called ax2
    fig2, ax2 = plt.subplots(nrows = len(xyd_df_list)-1, ncols = 1, 
                            figsize=(fig_width, fig_height), sharex = True)
    data_to_subtract_df = xyd_df_list[0]
    for i in range(1,len(xyd_df_list)):
        xyd_df = xyd_df_list[i]
        xyd_label = xyd_label_list[i]
        y_unc = np.sqrt(xyd_df['Error']**2 + data_to_subtract_df['Error']**2)
        ax2[i-1].errorbar(xyd_df['Angle'], 
                          xyd_df['Intensity']-data_to_subtract_df['Intensity'],
                          yerr=y_unc,
                         label = xyd_label + ' diff', color = colour_list[i])
        # legend
        ax2[i-1].legend(ncol=1, loc ='lower right', fontsize=10) 
        ax2[i-1].set_ylim(-2500,2500)
        ax2[i-1].set_xlim(roi_2theta_min,roi_2theta_max)
        ax2[i-1].tick_params(direction ='inout', length = 15)
    # minimise white space between plots vertically
    plt.subplots_adjust(hspace = 0)
    # title for main axes
    fig2.suptitle(fig2_title)
    # Label axes
    fig2.supxlabel(r'2 $\theta$')
    fig2.supylabel(r'Intensity (arb. units)')
    # save figure (always do this before show)
    # bbox_inches='tight' minimises white space around plot when it's saved
    plt.savefig(fig_filename+'_diff_plot.png',bbox_inches='tight',dpi=300)
    # then show figure in window
    plt.show()
    print('done figure {0}'.format(fig_filename+'_diff_plot.png'))
    print()


####################################################################
# FIG 3: SUPER PLOT
####################################################################
if fig3:
    # make figure
    fig_width = 20 # this is in inches
    fig_height = 15 # this is in inches
    # make a figure called fig12, with an axes called ax12
    fig3, ax3 = plt.subplots(nrows = len(xyd_df_list), ncols = 1, 
                            figsize=(fig_width, fig_height), sharex = True)
    # first of all plot the region of interest of the diffraction pattern
    for i in range(len(xyd_df_list)):
        xyd_df = xyd_df_list[i]
        xyd_label = xyd_label_list[i]
        ax3[0].errorbar(xyd_df['Angle'], 
                        xyd_df['Intensity']-background_xyd_df['scaled intensity'],
                        yerr=xyd_df['Error'],
                        label = xyd_label, color = colour_list[i])
        # legend
        ax3[0].legend(ncol=1, loc ='upper right', fontsize=10) 
        ax3[0].set_ylim(roi_intensity_min,roi_intensity_max)
        ax3[0].set_xlim(roi_2theta_min,roi_2theta_max)
    # then plot the diff plots so they share the same axes
    data_to_subtract_df = xyd_df_list[0]
    for i in range(1,len(xyd_df_list)):
        xyd_df = xyd_df_list[i]
        xyd_label = xyd_label_list[i]
        y_unc = np.sqrt(xyd_df['Error']**2 + data_to_subtract_df['Error']**2)
        ax3[i].errorbar(xyd_df['Angle'], 
                        xyd_df['Intensity']-background_xyd_df['scaled intensity']-data_to_subtract_df['Intensity'],
                        yerr=y_unc,
                        label = xyd_label + ' diff', color = colour_list[i])
        # legend
        ax3[i].legend(ncol=1, loc ='lower right', fontsize=10) 
        ax3[i].set_ylim(-2500,2500)
        ax3[i].set_xlim(roi_2theta_min,roi_2theta_max)
        ax3[i].tick_params(direction ='inout', length = 15)
    # minimise white space between plots vertically
    plt.subplots_adjust(hspace = 0)
    # title for main axes
    fig3.suptitle(fig3_title, y = 0.92)
    # Label axes
    fig3.supxlabel(r'2 $\theta$', y = 0.075)
    fig3.supylabel(r'Intensity (arb. units)', x = 0.075)
    # save figure (always do this before show)
    # bbox_inches='tight' minimises white space around plot when it's saved
    plt.savefig(fig_filename+'_SUPER_PLOT.png',bbox_inches='tight',dpi=300)
    # then show figure in window
    plt.show()
    print('done figure {0}'.format(fig_filename+'_SUPER_PLOT.png'))
    print()
