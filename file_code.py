import os
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
    for file_name in next(os.walk(sample_dirs[dir_index]))[2]:  # 2 = list all files
        if (file_name.__contains__('.png') or file_name.__contains__('.jpg')) and not search_term:
            file_list.append(file_name)
        elif (file_name.__contains__('.png') or file_name.__contains__('.jpg')) and file_name.__contains__(search_term):
            file_list.append(file_name)
    return sorted(file_list)


def get_sample_data(sample_dirs, dir_index, file_names, max_dim=100):
    orig_width, orig_height = pil_img.open(sample_dirs[dir_index] + '/' + file_names[0]).size
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
    all_png_data = np.zeros((new_width * new_height, sample_size), int)
    for index in range(sample_size):
        temp_data = pil_img.open(sample_dirs[dir_index] + '/' + file_names[index])
        temp_data = temp_data.resize((new_width, new_height), pil_img.Resampling.LANCZOS)
        temp_data = np.asarray(temp_data.convert('L')).flatten()
        all_png_data[:, index] = temp_data[:, ]
    return all_png_data


def create_output_name(working_dir, output_dir_list, output_dir_index, file_name, extension):
    return working_dir + '/' + output_dir_list[output_dir_index] + '/' + file_name + extension


def pickle_dump(variable, sample_dir, dir_index):
    motion_type = sample_dir[dir_index].split('- ')[-1]
    variable_name = motion_type + ' - ' + 'reduced_data'
    output_name = create_output_name(PWD, sample_dir, dir_index, variable_name, '.pkl')
    pkl.dump(variable, open(output_name, 'wb'))
