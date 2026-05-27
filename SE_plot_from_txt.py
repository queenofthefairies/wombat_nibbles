# this script plots diffraction data saved in xyd format

####################################################################
# get relevant python packages
####################################################################
import datetime as dt
import numpy as np
import matplotlib as mpl 
import matplotlib.pyplot as plt 
import pandas as pd 
import h5py

####################################################################
# READ THE DATA
####################################################################
# titles and names for figures
fig_filename = 'SE_data'
fig1_title = r'Wombat P22308'

HDF_file_name = 'SE_data_2026-05-25_AM.txt'
# get data
with open(HDF_file_name, 'r') as file:
    lines = file.readlines()

section_start_list = []
section_end_list = []
number_of_lines = len(lines)
i = 1
while i < number_of_lines:
    line = lines[i]
    if line[0] == '#':
        new_section = 1
        section_start_list.append(i+3)
        i = i + 3
    elif line in ['\n', '\r\n']:
        section_end_list.append(i)
        i = i + 1
    else:
        i = i + 1

print(section_start_list)
print(section_end_list)

section_title_list = []
for section_start_line in section_start_list:
    section_title = lines[section_start_line-1][6:]
    section_title = section_title.strip()
    section_title_list.append(section_title)
print(section_title_list)

data_list = []
for i in range(len(section_start_list)):
    data_lines = lines[section_start_list[i]:section_end_list[i]]
    date_time_list = []
    data_point_list = []
    for line in data_lines:
        line = line.split('\t')
        date_time_str = line[0][4:]
        date_time = dt.datetime.strptime(date_time_str, "%d %b %Y %H:%M:%S")
        data_point = line[1]
        date_time_list.append(date_time)
        data_point_list.append(float(data_point))
    data_list.append([date_time_list,data_point_list])

short_title_list = ['msom', 'Hot puck temp', 'Heat ex temp', 'Heater power %']
# tempC = f['entry1/sample/tc1/sensor/sensorValueC'][:]


# list of colours to use in plotting
# default matplotlib colours
#colour_list = ['C0', 'C1', 'C2', 'C3', 'C4', 'C5' ]
# nicer colours
colour_list = ['#0D3B66','#F5A6E6','#4392F1','#EE6352', '#4ADBC8','#F3A712']
####################################################################
# FIG 1: plot of xyd data
####################################################################

# make figure
fig_width = 7 # this is in inches
fig_height = 7 # this is in inches
# make a figure called fig1, with an axes called ax1
fig1, axs = plt.subplots(nrows = len(data_list), ncols = 1, sharex=True,
                        figsize=(fig_width, fig_height))
for i in range(len(data_list)):
    axs[i].plot(data_list[i][0], data_list[i][1], 
                label = short_title_list[i], color = colour_list[i])
    axs[i].set_ylabel(short_title_list[i], fontsize = 12) 
    print('plotted {0}'.format(section_title_list[i]))
# Label axes
#ax1.set_xlabel(r'$2 \theta$', fontsize = 12)
#ax1.set_ylabel('Intensity (arb. units)', fontsize = 12) 
# legend
#ax1.legend(ncol=1, loc ='upper left', fontsize=10) 
# title for main axes
fig1.suptitle(fig1_title)  
# save figure (always do this before show)
# bbox_inches='tight' minimises white space around plot when it's saved
plt.savefig(fig_filename+'_plot.png',bbox_inches='tight',dpi=300)
# then show figure in window
plt.show()
print('done figure {0}'.format(fig_filename+'_plot.png'))
print()




