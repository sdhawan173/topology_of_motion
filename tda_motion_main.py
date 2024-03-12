import os
import gudhi
import persdia_creator as pc
import pickle as pkl
import image_preprocessing as ipp
import file_code as fc


def load_preprocess_data(sample_directories):
    print('Searching for SVD reduced motion data ...')
    pkl_file_paths = []
    svd_data = []
    for dir_index, directory in enumerate(sample_directories):
        print('Searching for \'.pkl\' file ...')
        pkl_check, pkl_file_path = fc.file_check('reduced_data', directory, dir_index, '.pkl')

        print('Searching for score plot file ...')
        score_plot_check, score_path = fc.file_check('score plot', directory, dir_index, '.svg')

        if (pkl_check and score_plot_check) is True:
            print('\'.pkl\' file and SVD score plot found for: {}!'.format(directory))
        if pkl_check is False:
            print('{}: No \'.pkl\' file found,\n'
                  '-----Creating \'.pkl\' file of SVD data...'.format(directory))
            image_file_names = fc.get_image_file_names(sample_directories, dir_index)
            all_png_data = fc.get_sample_data(sample_directories, dir_index, image_file_names)
            ipp.transform_data(all_png_data, sample_directories, dir_index)
        pkl_check, pkl_file_path = fc.file_check('reduced_data', directory, dir_index, '.pkl')
        pkl_file_paths.append(pkl_file_path)
        svd_reduction = pkl.load(open(pkl_file_path, 'rb'))
        if score_plot_check is False:
            print('{}: No score plot found,\n'
                  '-----Creating SVD score plot ...'.format(directory))
            ipp.save_score_plot(svd_reduction, sample_directories, dir_index)
        svd_data.append(svd_reduction)
    return svd_data


sample_dirs = fc.get_sample_dirs()
svd_reduced_data = load_preprocess_data(sample_dirs)
for reduced_data, data_directory in zip(svd_reduced_data, sample_dirs):
    # Create file path strings to save persistence diagram and persistence points to
    save_path_base = os.getcwd() + '/' + data_directory + '/' + data_directory.split('/')[-1].split('- ')[-1]
    save_path_persdia = save_path_base + ' persdia' + '.svg'
    save_path_persdia_points = save_path_base + ' persistence' + '.txt'

    # Create vietoris rips complex
    input_data = [(x, y) for x, y in zip(reduced_data[0, :], reduced_data[1, :])]
    # noinspection PyUnresolvedReferences
    vr_complex = gudhi.RipsComplex(points=input_data)
    vr_simplex_tree = vr_complex.create_simplex_tree(max_dimension=3)

    # Create and save persistence points
    persistence_points = vr_simplex_tree.persistence()
    pc.save_persistence_points(persistence_points, save_path_persdia_points)

    # Create and save persistence diagram
    pc.plot_persdia_main(persistence_points, data_directory.split('- ')[-1], save_path_persdia, show_plot=False)
