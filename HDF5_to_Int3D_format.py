# Make images of wombat detector efficiency correction, derived from vanadium calibration run

# in the detector image array, element (0,0) i.e. 1st row, 1st col,
# is the "bottom left" of the detector, i.e. smallest 2theta and vertical min of detector
# element (127, 967) is the "top right" of the detector, i.e. largest 2theta and vertical max of detector

# how the efficiency correction is applied

import h5py
import numpy as np
import matplotlib.pyplot as plt
import csv
import shutil

data_dir = ''
files_list = []
for n in range(39056,39066):
    file_name = 'WBT00{0}.nx.hdf'.format(n)
    files_list.append(file_name)

for j in range(len(files_list)):
    run_number = files_list[j][:-7]
    file_path = data_dir + files_list[j]
    new_int3D_hdf = '{0}_int3D_format.nx.hdf'.format(run_number)
    try:
        shutil.copy2(file_path, new_int3D_hdf)
        with h5py.File(new_int3D_hdf, 'a') as f:
            som_angle = f['entry1/sample/rotate'][:]
            number_of_steps = len(som_angle)
            echi_angle = np.zeros(number_of_steps)
            ephi_angle = np.zeros(number_of_steps)
            # write angles to new groups to match Int3D input format 
            f['entry1/sample/euler_omega'] = som_angle
            f['entry1/sample/euler_chi'] = echi_angle
            f['entry1/sample/euler_phi'] = ephi_angle
        print('done {0}'.format(new_int3D_hdf))
    except FileNotFoundError:
        print('file {0} does not exist'.format(file_path))
    