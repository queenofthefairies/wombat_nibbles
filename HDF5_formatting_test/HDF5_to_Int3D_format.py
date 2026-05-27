# Int3D expects Wombat data HDF5 files to have 3 angles: euler_omega, euler_chi
# and euler_phi
# this script writes a new HDF5 file in the Int3D format
# for CF11 + dilution insert
# ephi = -msom
# echi = -sphi
# eom = som


import h5py
import numpy as np
import matplotlib.pyplot as plt
import csv
import shutil

import SingleCrystalHDF

data_dir = 'data'
formatted_data_dir = 'formatted_data' 
first_file_number = 107754
last_file_number = 107755

files_list = []
for n in range(first_file_number,last_file_number+1):
    file_name = 'WBT0{0}.nx.hdf'.format(n)
    files_list.append(file_name)

files_list = ['WBT0107754.nx.hdf', 'WBT0107772.nx.hdf']
# SingleCrystalHDF.HDF_to_Int3D_format(data_dir, files_list, formatted_data_dir,
#                                     eom_angle = 'som', echi_angle = 0, 
#                                     ephi_angle = 'msom', 
#                                     normalisation_value = 5000) 

##################### CONCATENATING FILES
# concatenate_file_list = []
# for n in range(first_file_number,last_file_number+1):
#     file_name = '{0}/WBT0{1}_int3D_format.nx.hdf'.format(formatted_data_dir,n)
#     concatenate_file_list.append(file_name)

# output_file = 'concatenated_{0}-{1}_int3D_format.nx.hdf'.format(first_file_number, 
#                                                                 last_file_number)
# SingleCrystalHDF.concatenate_HDF(concatenate_file_list, output_file)

##################### SUMMING EQUIVALENT DETECTOR FRAMES IN FILES
input_files = ['data/WBT0107754.nx.hdf', 'data/WBT0107772.nx.hdf']
output_file = 'summed.nx.hdf'
SingleCrystalHDF.sum_equivalent_frames_in_HDFs(input_files, output_file)
