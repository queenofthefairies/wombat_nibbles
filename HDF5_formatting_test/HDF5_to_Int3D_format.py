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
import shutil

import SingleCrystalHDF

data_dir = 'data'
formatted_data_dir = 'formatted_data' 
first_file_number = 107754
last_file_number = 107755

temperature = 40
tilt = 0
omega = -9

if temperature == 40:
    if tilt == 0:
        if omega == -9:
            BM1_normalisation_value = 58000
            run_number_list = [[107754, 107772],
                               [107755, 107773],
                               [107756, 107774],
                               [107757, 107775]]

############# first sum frames from different run numbers if required
file_list = []
for i in range(len(run_number_list)):
    sector_file = run_number_list[i]
    if type(run_number_list[i]) == list:
        print('summing frames in files')
        files_to_sum_list = []
        for run_number in run_number_list[i]:
            file_to_sum_name = '{0}/WBT0{1}.nx.hdf'.format(data_dir,run_number)
            files_to_sum_list.append(file_to_sum_name)
        output_file = 'summed_{0}_{1}.nx.hdf'.format(run_number_list[i][0],
                                                     run_number_list[i][-1])
        SingleCrystalHDF.sum_equivalent_frames_in_HDFs(files_to_sum_list, output_file)
    elif type(run_number_list[i]) == int:
        new_sector_file = '{0}/WBT0{1}.nx.hdf'.format(data_dir,run_number_list[i])
        file_list.append(new_sector_file)

############# then concatenate files
output_file = 'concatenated_{0}mK_tilt{1}_omega{2}.nx.hdf'.format(temperature,
                                                                  tilt,
                                                                  omega)

output_file_path = data_dir +'/' + output_file
SingleCrystalHDF.concatenate_HDF(file_list, output_file_path)

############# then re-format for int3D
SingleCrystalHDF.HDF_to_Int3D_format(data_dir, [output_file], formatted_data_dir,
                                     eom_angle = 'som', echi_angle = 0, 
                                     ephi_angle = 'msom', 
                                     normalisation_value = BM1_normalisation_value,
                                     efficiency_calibration='eff_2026_04_13.gumtree.hdf') 

print()
print('      Done aggregating dataset for {0} mK, tilt {1}, som {2}'.format(temperature,tilt,omega))
# files_list = []
# for n in range(first_file_number,last_file_number+1):
#     file_name = 'WBT0{0}.nx.hdf'.format(n)
#     files_list.append(file_name)

# files_list = ['WBT0107754.nx.hdf', 'WBT0107772.nx.hdf']
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
# input_files = ['data/WBT0107754.nx.hdf', 'data/WBT0107772.nx.hdf']
# output_file = 'summed.nx.hdf'
# #SingleCrystalHDF.sum_equivalent_frames_in_HDFs(input_files, output_file)
# data_dir = ''
# SingleCrystalHDF.HDF_to_Int3D_format(data_dir, ['summed.nx.hdf'], formatted_data_dir,
#                                      eom_angle = 'som', echi_angle = 0, 
#                                      ephi_angle = 'msom', 
#                                      normalisation_value = 0)#,
                                     #efficiency_calibration='eff_2026_04_13.gumtree.hdf') 
