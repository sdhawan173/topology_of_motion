import os
import gudhi
import pickle as pkl
import image_preprocessing as ipp
import file_code as fc
import persdia_creator as pc


def load_preprocess_data(sample_directories, transform_type, svd_pkl_string='reduced_data'):
    print('Searching for SVD reduced motion data ...')
    svd_data = []
    loaded_data = []

    print('Transformation Type = {}'.format(transform_type))
    for dir_index, directory in enumerate(sample_directories):
        print('Current Directory: {}'.format(directory))
        print('Getting image data for all files ...')
        image_file_names = fc.get_image_file_names(sample_directories, dir_index)
        all_png_data = fc.get_sample_data(sample_directories, dir_index, image_file_names, transform_type)

        loaded_data.append(all_png_data)

        svd_reduction = None
        if transform_type == 'svd':
            print('Searching for \'.pkl\' file ...')
            pkl_check, pkl_file_path = fc.file_check(svd_pkl_string, directory, dir_index, '.pkl')
            if pkl_check is False:
                svd_reduction = ipp.transform_data(all_png_data, sample_directories, dir_index)
            elif pkl_check:
                svd_reduction = pkl.load(open(pkl_file_path, 'rb'))

            print('Searching for score plot file ...')
            score_plot_check, score_path = fc.file_check('score plot', directory, dir_index, '.svg')
            if score_plot_check is False:
                print('{}: No score plot found,\n-----Creating SVD score plot ...'.format(directory))
                ipp.save_score_plot(svd_reduction, sample_directories, dir_index)
            svd_data.append(svd_reduction)

    if transform_type == 'svd':
        loaded_data = svd_data
    return loaded_data


method = 'flatten'
sample_dirs = fc.get_sample_dirs()
data_list = load_preprocess_data(sample_dirs, transform_type=method)
for data, data_directory in zip(data_list, sample_dirs):
    # Create file path strings to save persistence diagram and persistence points to
    motion_name = data_directory.split('- ')[-1]
    print('\nRunning {} ... '.format(motion_name))
    save_path_base = os.getcwd() + '/' + data_directory + '/' + motion_name
    if method == 'svd':
        save_path_base += ' - SVD score plot'
    save_path_persdia = save_path_base + ' persdia' + '.svg'
    save_path_persdia_points = save_path_base + ' persistence' + '.txt'

    if method == 'svd':
        input_data = [(x, y) for x, y in zip(data[0, :], data[1, :])]
    else:
        input_data = data
    print('Creating VR Complex ...')
    # Create vietoris rips complex
    # noinspection PyUnresolvedReferences
    gudhi_complex = gudhi.RipsComplex(points=input_data)
    print('Creating Simplex Tree ...')
    simplex_tree = gudhi_complex.create_simplex_tree(max_dimension=2)

    # Create and save persistence points
    print('Creating Persistence Points ...')
    persistence_points = simplex_tree.persistence()
    pc.save_persistence_points(persistence_points, save_path_persdia_points)

    # Create and save persistence diagram
    print('Plotting Persistence Diagram ...')
    pc.plot_persdia_main(persistence_points, motion_name, save_path_persdia, show_plot=False)
    print('Completed run for {}\n'.format(motion_name))
