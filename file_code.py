import os
import math
from collections import defaultdict
import numpy as np
import PIL.Image as pil_img
import pickle as pkl


PWD = os.getcwd()


def file_search(search_term, dir_string=os.getcwd()):
    """
    searches a directory, with the current working directory as default, for a given filetype.
    :param dir_string: string of directory to search
    :param search_term: string of filetype, input as a string in the format: '.type'
    :return: list of file names with extensions that match search term
    """
    file_list = []
    for list_item in os.listdir(dir_string):
        if list_item.__contains__(search_term):
            file_list.append(list_item)
    return sorted(file_list, key=str.casefold)


def file_check(variable_name, sample_dir, dir_index, extension, os_walk_index=2, check_subdir=False):
    file_exists = False
    file_dir = None
    check_dir = PWD + '/' + sample_dir[dir_index]
    if check_subdir is False:
        check_dir = PWD + '/' + sample_dir
    for file_name in next(os.walk(check_dir + '/'))[os_walk_index]:
        if file_name.__contains__(variable_name) and file_name.__contains__(extension):
            file_dir = check_dir + '/' + file_name
            file_exists = True
            return file_exists, file_dir
    return file_exists, file_dir


def file_read(file_path):
    """
    reads stl file and stores to array
    :param file_path: file path of ast or stl file
    """
    read_file = []
    opened_file = open(file_path, 'r')
    for line in opened_file:
        read_file.append(line)
    opened_file.close()
    return read_file


def choose_index(sample_dirs):
    for index, directory in enumerate(sample_dirs):
        if index < 10:
            print('{}: {}'.format('0' + str(index), directory))
        if index >= 10:
            print('{}: {}'.format(str(index), directory))
    # Select file, print output to confirm choice
    chosen_index = input('Choose directory by entering the corresponding number:\n')
    if int(chosen_index) < 10 and len(chosen_index) >= 2:
        chosen_index = int(chosen_index[-1])
    if int(chosen_index) > 100 and len(chosen_index) >= 3:
        chosen_index = int(chosen_index)
    else:
        chosen_index = int(chosen_index)
    return chosen_index


def get_sample_dirs(search_term='Case'):
    all_subdirs = next(os.walk(PWD))[1]  # 1 = list of subdirectories in working_directory
    sample_dirs = []
    for directory in all_subdirs:
        if directory.__contains__(search_term):
            sample_dirs.append(directory)
    return sorted(sample_dirs)


def get_image_file_names(sample_dirs, dir_index, search_term=None):
    file_list = []
    next_num = 2  # 2 = list all files
    walk_input = sample_dirs[dir_index]
    if len(sample_dirs) == 1:
        walk_input = os.getcwd() + '/' + sample_dirs[0]
    iterator = next(os.walk(walk_input))[next_num]
    for file_name in iterator:
        if (file_name.__contains__('.png') or file_name.__contains__('.jpg')) and not search_term:
            file_list.append(file_name)
        elif (file_name.__contains__('.png') or file_name.__contains__('.jpg')) and file_name.__contains__(search_term):
            file_list.append(file_name)
    return sorted(file_list)


def save_motion_overlay(all_png_data, sample_size, new_height, new_width, sample_dirs, dir_index):
    motion_name = sample_dirs[dir_index].split('- ')[-1]
    overlay_save_name = motion_name + ' overlay'

    all_png_data = all_png_data.astype(np.uint8)

    # Reshape the flattened images back to their original size
    images = all_png_data.reshape(sample_size, new_height, new_width)

    # Initialize an empty canvas to stack the images
    stacked_image = np.zeros((new_height, new_width), dtype=np.float32)

    # Stack the images with transparency
    for i in range(sample_size):
        # Scale the image values by the number of images
        scaled_image = images[i] / sample_size

        # Add the scaled image to the stacked image
        stacked_image += scaled_image

    # Convert the stacked image to uint8
    if motion_name.__contains__('cat'):
        stacked_image_uint8 = stacked_image.astype(np.uint8)
    else:
        stacked_image_uint8 = (stacked_image * 255).astype(np.uint8)

    # Convert the stacked image to PIL Image
    stacked_image_pil = pil_img.fromarray(stacked_image_uint8)
    # stacked_image_pil.show()  # Display the stacked image
    stacked_image_pil.save(os.getcwd() + '/' + sample_dirs[dir_index] + '/' + overlay_save_name + '.jpg')
    stacked_image_pil.close()

    # gudhi_complex = gudhi.RipsComplex(points=stacked_image)
    # simplex_tree = gudhi_complex.create_simplex_tree(max_dimension=2)
    # persistence_points = simplex_tree.persistence()
    # pc.save_persistence_points(
    #     persistence_points,
    #     os.getcwd() + '/' + sample_dirs[dir_index] + '/' + motion_name + ' overlay persdia points.txt'
    # )
    # gudhi.plot_persistence_diagram(persistence_points)
    # pc.plot_persdia_main(
    #     persistence_points,
    #     motion_name + ' images overlay',
    #     os.getcwd() + '/' + sample_dirs[dir_index] + '/' + overlay_save_name + 'persdia.svg',
    #     show_plot=False
    # )
    # plt.clf()
    # plt.close()


def get_sample_data(sample_dirs, dir_index, file_names, transform_type=None, max_dim=100):
    all_png_data = None
    orig_width, orig_height = pil_img.open(os.getcwd() + '/' + sample_dirs[dir_index] + '/' + file_names[0]).size

    new_width = orig_width
    new_height = orig_height
    if orig_width or orig_height > 100:
        new_dim = int(max_dim*min(orig_width, orig_height)/max(orig_width, orig_height))
        if orig_width > orig_height:
            new_width = 100
            new_height = new_dim
        elif orig_height > orig_width:
            new_width = new_dim
            new_height = 100

    sample_size = len(file_names)
    if transform_type == 'flatten':

        all_png_data = np.zeros((sample_size, new_width * new_height), int)
        for index in range(sample_size):
            temp_data = pil_img.open(sample_dirs[dir_index] + '/' + file_names[index])
            temp_data = temp_data.resize((new_width, new_height))
            temp_data = np.asarray(temp_data.convert('L')).flatten()
            all_png_data[index, :] = temp_data[:, ]
        save_motion_overlay(all_png_data, sample_size, new_height, new_width, sample_dirs, dir_index)

    if transform_type == 'svd':
        all_png_data = np.zeros((new_width * new_height, sample_size), int)
        for index in range(sample_size):
            temp_data = pil_img.open(sample_dirs[dir_index] + '/' + file_names[index])
            temp_data = temp_data.resize((new_width, new_height), pil_img.Resampling.LANCZOS)
            temp_data = np.asarray(temp_data.convert('L')).flatten()
            all_png_data[:, index] = temp_data[:, ]

    return all_png_data


def create_output_name(working_dir, output_dir_list, output_dir_index, file_name, extension):
    return working_dir + '/' + output_dir_list[output_dir_index] + '/' + file_name + extension


def pickle_dump(variable, file_suffix, sample_dir, dir_index):
    motion_type = sample_dir[dir_index].split('- ')[-1]
    variable_name = motion_type + ' - ' + file_suffix
    output_name = create_output_name(PWD, sample_dir, dir_index, variable_name, '.pkl')
    pkl.dump(variable, open(output_name, 'wb'))


def read_persistence():
    persistence_file_paths = []
    sample_dirs = get_sample_dirs()
    for index, sample_dir in enumerate(sample_dirs):
        next_num = 2  # 2 = list all files
        walk_input = os.getcwd() + '/' + sample_dirs[index]
        iterator = next(os.walk(walk_input))[next_num]
        for file_name in iterator:
            if file_name.__contains__('motion persistence'):
                persistence_file_paths.append(walk_input + '/' + file_name)
                break
    return persistence_file_paths


def parse_persistence(persistence_file):
    read_file = []
    opened_file = open(persistence_file, 'r')
    for line in opened_file:
        temp_line = line.split('\n')[0]
        temp_line = temp_line.replace('(', '').replace(')', '').split(', ')
        h_k = int(temp_line[0])
        birth = float(temp_line[1])
        if temp_line[2] == 'inf':
            death = math.inf
        else:
            death = float(temp_line[2])
        persistence_entry = [h_k, (birth, death)]
        read_file.append(persistence_entry)
    opened_file.close()
    return read_file


def analyze_persistence_files():
    file_paths = read_persistence()
    all_persistence_data = []
    for file_path in file_paths:
        all_persistence_data.append(parse_persistence(file_path))

    all_unique_persistence = []
    for data, file_path in zip(all_persistence_data, file_paths):
        frequency_dict = defaultdict(int)

        for entry in data:
            frequency_dict[tuple(entry)] += 1

        unique_persistence = [[freq, entry] for entry, freq in frequency_dict.items()]

        point_count = 0
        for entry in unique_persistence:
            if entry[1][0] == 0:
                point_count += entry[0]
        print(file_path)
        print(point_count)

        all_unique_persistence.append(unique_persistence)
