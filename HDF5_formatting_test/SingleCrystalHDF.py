import h5py
import numpy as np
import matplotlib.pyplot as plt
import csv
import shutil

################################################################################
def write_or_create_dataset(new_file, group_name, data_arr):
    try:
        new_file.create_dataset(group_name, data=data_arr)
    except ValueError:
        del new_file[group_name]
        new_file.create_dataset(group_name, data=data_arr)

    if group_name == 'entry1/data/normalisation':
        print('     rewriting normalisation')
        data_arr = data_arr.astype(np.bytes_)
        del new_file[group_name]
        new_file.create_dataset(group_name, data=data_arr)
    return

################################################################################
def copy_run_info(old_file, new_file):
    "copies auxillary data from the original run HDF to the new formatted HDF"
    groups_to_copy = ['entry1/sample/name',
                      'entry1/sample/azimuthal_angle',
                      'entry1/sample/description',
                      'entry1/sample/short_title',
                      'entry1/user/name',
                      'entry1/site_name',
                      'entry1/experiment/title',
                      'entry1/experiment/file_name',
                      'entry1/data/x_pixel_angular_offset',
                      'entry1/data/y_pixel_offset',
                      'entry1/start_time',
                      'entry1/end_time'
                      ]
    
    for group_name in groups_to_copy:
        try:
            data_arr = old_file[group_name]
            write_or_create_dataset(new_file, group_name, data_arr)
        except KeyError:
            print('no HDF group called {0} in original file'.format(group_name))
            print('skipping {0}'.format(group_name))
    print('     copied auxillary data from original HDF into new formatted HDF')
    
    return

################################################################################
def normalise_frames_to_monitor_counts(old_file, new_file, 
                                       normalisation_value = 0):
    # get data
    beam_monitor_counts = old_file['entry1/monitor/bm1_counts'][:]
    detector_data = old_file['entry1/data/hmm_xy'][:]
    if normalisation_value == 0:
        average_beam_monitor_counts = np.sum(beam_monitor_counts)/len(beam_monitor_counts)
        normalisation_value_used = average_beam_monitor_counts
        print('     Normalisation value used: {0:.1f} (average beam monitor 1 counts)'.format(normalisation_value_used))
    else:
        normalisation_value_used = normalisation_value
        print('     Normalisation value used: {0}'.format(normalisation_value_used))
    normalised_data = np.divide(detector_data,beam_monitor_counts[:,np.newaxis, np.newaxis])*normalisation_value_used
    # write normalised data 
    write_or_create_dataset(new_file,'entry1/data/hmm_xy', normalised_data)
    normalisation_label = 'NORMALISED BM1 counts {0}'.format(normalisation_value_used)
    norm_label_arr = np.array([normalisation_label]).astype(np.bytes_)
    write_or_create_dataset(new_file,'entry1/data/normalisation', norm_label_arr)
    print('     Normalisation applied to data')

    return

################################################################################
def apply_efficiency_calibration(new_file, efficiency_file_path):
    # get data
    eff_file = h5py.File(efficiency_file_path,mode='r')
    eff_cal_array = eff_file['entry1/data/signal'][:]
    detector_data = new_file['entry1/data/hmm_xy'][:]
    eff_cal_data = np.repeat(eff_cal_array[np.newaxis],len(detector_data),axis=0)
    eff_calibrated_counts = np.multiply(eff_cal_data,detector_data)
    # write efficiency calibrated data 
    write_or_create_dataset(new_file,'entry1/data/hmm_xy', eff_calibrated_counts)
    eff_cal_label_arr = np.array([efficiency_file_path]).astype(np.bytes_)
    write_or_create_dataset(new_file,'entry1/data/efficiency_calibration', eff_cal_label_arr)
    print('     Efficiency calibration {0} applied to data'.format(efficiency_file_path))
    eff_file.close()
    return

################################################################################
def assign_eulerian_angles(old_file, new_file, 
                           eom_angle = 0, echi_angle = 0, ephi_angle = 0):
    
    beam_monitor_counts = old_file['entry1/monitor/bm1_counts'][:]
    number_of_steps = len(beam_monitor_counts)

    ##### EPHI could be
    # 0
    # msom (serotabs/sample probe omega if NON-ZERO TILT)
    # some other fixed number
    if ephi_angle == 0:
        new_ephi_angle = np.zeros(number_of_steps)
    elif ephi_angle == 'msom':
        new_ephi_angle = -old_file['entry1/instrument/msom'][:] # ephi = -msom angle
    else:
        if type(ephi_angle) is not float or int:
            print('!!! check ephi angle. needs to be a number or msom')
        else:
            new_ephi_angle = ephi_angle*np.ones(number_of_steps) 
    
    ##### ECHI could be 
    # 0
    # sphi (sample stage tilt)
    # some other fixed number
    if echi_angle == 0:
        new_echi_angle = np.zeros(number_of_steps)
    elif echi_angle == 'sphi':
        new_echi_angle = -old_file[''] # echi = -sphi angle
    else:
        if type(echi_angle) is not float or int:
            print('!!! check echi angle. needs to be a number or sphi')
        else:
            new_echi_angle = echi_angle*np.ones(number_of_steps) 

    ##### EOM could be
    # 0
    # som (sample stage omega)
    # msom (serotabs/sample probe omega if ZERO TILT)
    # some other fixed number
    if eom_angle == 0:
        new_eom_angle = np.zeros(number_of_steps)
    elif eom_angle == 'som':
        new_eom_angle = old_file['entry1/sample/rotate'][:] # eom = som angle
    elif eom_angle == 'msom':
        new_eom_angle = -old_file['entry1/instrument/msom'][:] # eom = -msom angle
    else:
        if type(eom_angle) is not float or int:
            print('!!! check echi angle. needs to be a number or sphi')
        else:
            new_eom_angle = eom_angle*np.ones(number_of_steps)
    
    # write angles to new groups to match Int3D input format 
    write_or_create_dataset(new_file,'entry1/sample/euler_omega', new_eom_angle)
    write_or_create_dataset(new_file,'entry1/sample/euler_chi', new_echi_angle)
    write_or_create_dataset(new_file,'entry1/sample/euler_phi', new_ephi_angle)
    print('     Eulerian angles written to new formatted HDF')

    return

################################################################################
def HDF_to_Int3D_format(data_dir, data_list, formatted_data_dir, 
                        eom_angle = 0, echi_angle = 0, ephi_angle = 0, 
                        normalisation_value = 0, efficiency_calibration = None):
    """ takes a Wombat HDF for a non-Eulerian cradle measurement
    and formats it for Int3D """

    for j in range(len(data_list)):
        run_number = data_list[j][:-7]
        if data_dir == '':
            original_file_path = data_list[j]
        elif data_dir[-1] != '/':
            original_file_path = data_dir +'/' + data_list[j]
        else: 
            original_file_path = data_dir + data_list[j]
        
        print()
        print('opening {0}'.format(original_file_path))
        try:
            #### Read original HDF
            old_file = h5py.File(original_file_path, 'r')
        except FileNotFoundError:
            print('file {0} does not exist or destination directory does not exist'.format(original_file_path))
            break

        ########## write everything to new HDF
        new_int3D_hdf = '{0}/{1}_int3D_format.nx.hdf'.format(formatted_data_dir,run_number)
        new_file = h5py.File(new_int3D_hdf, 'a')
        # normalisation
        normalise_frames_to_monitor_counts(old_file, new_file, normalisation_value)
        # efficiency calibration
        if efficiency_calibration:
            apply_efficiency_calibration(new_file, efficiency_calibration)
        else:
            print('     no efficiency calibration applied')
        # eulerian angles
        assign_eulerian_angles(old_file, new_file, 
                               eom_angle, echi_angle, ephi_angle)
        # auxillary data
        copy_run_info(old_file, new_file)

        # add new group for consistency with any HDF arising from summed files
        try:
            # add new group for consistency with any HDF arising from summed files
            summed_file_name_array = old_file['entry1/data/summed_frames_from_files'][:]
        except KeyError:
            # add new group for consistency with any HDF arising from summed files
            summed_file_name_array = old_file['entry1/experiment/file_name'][:]
            # should be a row (not a column) in case this summed file is then concatenated
            summed_file_name_array = np.transpose(summed_file_name_array)
        
        write_or_create_dataset(new_file,'entry1/data/summed_frames_from_files', summed_file_name_array)
        #new_file.create_dataset('entry1/data/summed_frames_from_files', data=summed_file_name_array)

        print('done {0}'.format(new_int3D_hdf))
        new_file.close()
        old_file.close()

    return

################################################################################   
def concatenate_HDF(input_files, output_file):
    """
    Concatenate datasets from multiple HDF5 files that share
    the same group/dataset structure.

    Example:
        Dataset shape (6, 1) + (6, 1) -> (12, 1)
        """

    print('concatenating files ')
    print('from {0}'.format(input_files[0]))
    print('to {0}'.format(input_files[-1]))
    with h5py.File(output_file, "w") as out_f:

        # Open all input files
        input_handles = [h5py.File(f, "r") for f in input_files]

        try:
            # Use the first file as the reference structure
            ref_file = input_handles[0]

            def process_group(ref_group, out_group, group_path="/"):
                for key in ref_group.keys():
                    item = ref_group[key]

                    if isinstance(item, h5py.Group):
                        # Create corresponding group in output
                        new_group = out_group.create_group(key)

                        process_group(
                            item,
                            new_group,
                            group_path + key + "/"
                        )

                    elif isinstance(item, h5py.Dataset):
                        dataset_path = group_path + key
                        # Read matching datasets from all files
                        arrays = [
                            f[dataset_path][:]
                            for f in input_handles
                        ]

                        # Concatenate along axis 0
                        concatenated = np.concatenate(arrays, axis=0)
                        try:
                            # Create dataset in output file
                            out_group.create_dataset(
                                key,
                                data=concatenated,
                                dtype=concatenated.dtype
                            )
                            print(
                            f"     {dataset_path}: "
                            f"{arrays[0].shape} -> {concatenated.shape}"
                            )
                        except TypeError:
                            print('Type Error - skipping this group')
                            print(concatenated)

            process_group(ref_file, out_f)

            ###### some things we don't want to concatenate
            x_pixel_arr = np.linspace(0.10938,120.98,num=969)
            write_or_create_dataset(out_f, 'entry1/data/x_pixel_angular_offset', 
                                    x_pixel_arr)
            y_pixel_arr = np.linspace(-0.19844,203,num=129)
            write_or_create_dataset(out_f, 'entry1/data/y_pixel_offset', 
                                    y_pixel_arr)
            concatenated_file_names_arr = out_f['entry1/experiment/file_name'][:]
            write_or_create_dataset(out_f, 'entry1/data/concatenated_files', 
                                    concatenated_file_names_arr)

        finally:
            # Close all input files
            for f in input_handles:
                f.close()
    print('concatenated HDF written to {0}'.format(output_file))
    return

################################################################################ 
def sum_equivalent_frames_in_HDFs(input_files, output_file):
    " Sum equivalent frames in HDFs to create a new aggregate HDF file"
    "Also sum beam monitor counts for future normalisation"

    print('summing equivalent detector frames in files ')
    print('from {0}'.format(input_files[0]))
    print('to {0}'.format(input_files[-1]))

    if len(input_files) < 2:
        print('cannot sum frames in fewer than 2 files, add more files to the list')
        return

    try:
        shutil.copy2(input_files[0], output_file)
    except FileNotFoundError:
        print('file {0} does not exist'.format(input_files[0]))
              
        return
              
    summed_file = h5py.File(output_file, 'a')
    summed_frame_array = summed_file['entry1/data/hmm_xy'][:]
    summed_monitor_counts_array = summed_file['entry1/monitor/bm1_counts'][:]
    summed_file_name_array = summed_file['entry1/experiment/file_name'][:]
    summed_file_name_list = summed_file_name_array.tolist()

    for input_file in input_files[1:]:
        print('adding {0}'.format(input_file))
        file_to_add = h5py.File(input_file, 'r')
        # summing beam monitor counts together frame by frame
        monitor_counts_array_to_add = file_to_add['entry1/monitor/bm1_counts'][:]
        summed_monitor_counts_array = summed_monitor_counts_array + monitor_counts_array_to_add
        # summing equivalent detector frames together
        frame_array_to_add = file_to_add['entry1/data/hmm_xy'][:]
        summed_frame_array = summed_frame_array + frame_array_to_add
        # adding file name to list
        file_name_to_add = file_to_add['entry1/experiment/file_name'][0]
        summed_file_name_list.append(file_name_to_add)
        file_to_add.close()

    # write summed detector frames
    del summed_file['entry1/data/hmm_xy']
    summed_file.create_dataset('entry1/data/hmm_xy', data=summed_frame_array)

    # write summed monitor counts
    del summed_file['entry1/monitor']
    summed_file.create_dataset('entry1/monitor/bm1_counts', data=summed_monitor_counts_array)

    # write new file_name since new HDF was built from several files
    del summed_file['entry1/experiment/file_name']
    file_name_array = np.array(['created from summing equivalent frames in several files']).astype(np.bytes_)
    summed_file.create_dataset('entry1/experiment/file_name', data=file_name_array)

    # add new group which is an array of the files that have been 
    summed_file_name_array = np.array([summed_file_name_list]).astype(np.bytes_)
    # should be a row (not a column) in case this summed file is then concatenated
    summed_file_name_array = np.transpose(summed_file_name_array)
    summed_file.create_dataset('entry1/data/summed_frames_from_files', data=summed_file_name_array)

    summed_file.close()
    print('summed detector frames written to {0}'.format(output_file))
    return