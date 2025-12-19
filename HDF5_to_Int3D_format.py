# Int3D expects Wombat data HDF5 files to have 3 angles: euler_omega, euler_chi
# and euler_phi
# However many sample environments there is no 'chi' or 'phi', just omega rotation
# through som or msom
# this script writes a new HDF5 file in the Int3D format:
# it copies som/msom to euler_omega
# and fills euler_chi and euler_phi with a 0 for every omega step.

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
    