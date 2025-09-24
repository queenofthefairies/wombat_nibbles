''' Do box integration of wombat detector step by step for a list of HDF files
specify box boundary for integration.

Save box integration values to a csv file along with relevant parameters such 
as sample temperature, field value and run number.

Optionally visualise box on detector images to check whether box covers the 
peak of interest '''

import h5py
import numpy as np
import math
import matplotlib.pyplot as plt
import csv

################################################################################
# Import Wombat data
################################################################################
# data where the raw HDF are
data_dir = 'raw_data/rawdata/'

# make a list of all 001 peak numbers (all msom -86.25 degrees)
files_list = []
file_numbers = range(104030,104143,4)
for i in file_numbers:
    file_name = 'WBT0{0}.nx.hdf'.format(i)
    files_list.append(file_name)
file_numbers2 = range(104146,104187,2)
for i in file_numbers2:
    file_name = 'WBT0{0}.nx.hdf'.format(i)
    files_list.append(file_name)
print(files_list)

################################################################################
# Detector calibration array
################################################################################
calibration_file = data_dir + 'eff_2025_06_12.gumtree.hdf'
with h5py.File(calibration_file, 'r') as f:
    calibration_dataset = f['entry1/data/signal']
    calibration_array = np.array(calibration_dataset)

################################################################################
# Integration details
################################################################################
integration_label = '001_peak' # to be appended to filename
box_two_theta_min = 19
box_two_theta_max = 21
box_vert_pixel_min = 45
box_vert_pixel_max = 90

visualise_on = 0
intensity_min = 0
intensity_max = 200

is_test = 0

################################################################################
# INTEGRATION AND VISUALISATION
################################################################################
vertical_pixel_min = 0
vertical_pixel_max = 127

box_height = box_vert_pixel_max - box_vert_pixel_min
box_width = box_two_theta_max - box_two_theta_min

# string containing parameters of integration to go at start of output csv file
intro_string = 'integration_label = {0} \n two_theta_min = {1} \n two_theta_max = {2} \n vertical_pixel_min = {3} \n vertical_pixel_max = {4} \n'.format(integration_label,
                                                                                                                                                         box_two_theta_min, 
                                                                                                                                                         box_two_theta_max, 
                                                                                                                                                         box_vert_pixel_min,
                                                                                                                                                         box_vert_pixel_max)

params_string = '\n run number, field, temperature, msom, integrated value'
to_write_csv = [intro_string, params_string]

# if test, don't do every single file
if is_test:
    files_to_integrate = range(5)
else:
    files_to_integrate = range(len(files_list))

# go through HDF files one by one 
for j in files_to_integrate:
    run_number = files_list[j][0:10]
    file_path = data_dir + files_list[j]
    with h5py.File(file_path, 'r') as f:
        # get detector data
        image_dataset = f['entry1/data/hmm_xy']
        # horizontal pixels of detector correspond to a range of two theta angles
        two_theta = f['entry1/data/x_pixel_angular_offset'] 
        # wombat stth, the first two theta corresponding to pixel 0
        two_theta_0 = f['entry1/sample/azimuthal_angle'] 
        two_theta_min = two_theta[0] + two_theta_0[0]
        two_theta_max = two_theta[-1] + two_theta_0[0]
        # get magnetic field
        field_variable = f['entry1/sample/magnet1/magnet/field']
        field_value = field_variable[0]
        # get temperature of sample
        temp_sensor_variable = f['entry1/sample/tc2/sensor/sensorValueB']
        temp_sensor_value = temp_sensor_variable[0]
        # get msom angle of sample
        msom_variable = f['entry1/instrument/msom']
        msom_value = msom_variable[0]
        # get beam monitor counts
        monitor_counts = f['entry1/monitor/bm1_counts'] 
        # if test, don't do every step of the file
        if is_test:
            no_steps = 3
        else:
            no_steps = len(image_dataset)

        ################# Do integration of box
        int_x_min = math.floor((box_two_theta_min - two_theta_0[0])/two_theta[-1]*968)
        int_x_max = math.ceil((box_two_theta_max - two_theta_0[0])/two_theta[-1]*968)
        int_y_min = box_vert_pixel_min
        int_y_max = box_vert_pixel_max
        # to begin with integration value of box is zero
        int_value = 0
        # go through HDF file step by step. 
        for i in range(no_steps):
            image_array = image_dataset[i]
            # normalise by detector calibration array and monitor counts
            image_array_eff_corrected = np.multiply(calibration_array,image_array)/monitor_counts[i]*10**6
            image_box_to_int = image_array_eff_corrected[int_x_min:int_x_max, int_y_min:int_y_max]
            # sum up all pixels inside box
            int_value_i = np.sum(image_box_to_int)
            # integration of box from this step is added to total integration value
            int_value = int_value + int_value_i
            print('done step {0} of {1}: {2}'.format(i, no_steps, int_value_i))
        print('run number: {0}. box integration value: {1}'.format(run_number, int_value))
        # write string of result
        int_result_to_write_to_csv = '{0}, {1:.2f}, {2:.2f}, {3:.2f}, {4}'.format(run_number, field_value, temp_sensor_value, msom_value, int_value)
        to_write_csv.append(int_result_to_write_to_csv)

        # visualise box on plot of detector. Show first, middle and last steps.
        if visualise_on:
            fig, axs = plt.subplots(3,1, figsize=(6, 9),sharex=True, sharey=True)
            middle_step = math.floor(no_steps/2)
            subplot_no = 0
            for i in [0, middle_step, no_steps-1]:
                int_box_to_plot = plt.Rectangle((box_two_theta_min, box_vert_pixel_min), box_width, box_height,
                                                fill=0, facecolor=None, edgecolor='red')
                image_array = image_dataset[i]
                # normalise by detector calibration array and monitor counts
                image_array_eff_corrected = np.multiply(calibration_array,image_array)/monitor_counts[i]*10**6
                axs[subplot_no].imshow(image_array_eff_corrected, aspect='auto', extent=(two_theta_min,two_theta_max,vertical_pixel_min,vertical_pixel_max),
                                       vmin=intensity_min, vmax=intensity_max)
                axs[subplot_no].set_title('step {0} of {1}'.format(i, no_steps-1))
                axs[subplot_no].add_patch(int_box_to_plot)
                subplot_no = subplot_no + 1
            fig.supxlabel(r'2$\theta$ (degrees)')
            fig.supylabel('Vertical pixel')
            fig.suptitle("{0} HDF5, field = {1:.2f} T, temperature = {2:.2f} K".format(run_number,field_value,temp_sensor_value))
                
            plt.show()
        else:
            pass
    
    # Write output file of integration values, relevant parameters from all run numbers
    output_file_name = 'box_integration_{0}_two_theta_{1:.0f}-{2:.0f}_vertical_{3}-{4}.csv'.format(integration_label,
                                                                                                   box_two_theta_min, 
                                                                                                   box_two_theta_max, 
                                                                                                   box_vert_pixel_min,
                                                                                                   box_vert_pixel_max)
    with open(output_file_name, 'w') as g:
        for line in to_write_csv:
            g.write(line + '\n')
    print('done {0}'.format(output_file_name))


print()
print('all done!')

