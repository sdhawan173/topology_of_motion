import os
import numpy as np
import PIL.Image as pil


def file_search(extension, dir_string=os.getcwd()):
    """
    searches a directory, with the current working directory as default, for a given filetype.
    :param dir_string: string of directory to search
    :param extension: string of filetype, input as a string in the format: '.type'
    :return: list of file names with extensions that match search term
    """
    file_list = []

    # Run through list and add files with .ast extension to ast_list
    for list_item in os.listdir(dir_string):
        if list_item.__contains__(extension):
            file_list.append(list_item)
    return sorted(file_list, key=str.casefold)


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


def get_sample_dirs():
    pwd = os.getcwd()
    all_subdirs = next(os.walk(pwd))[1]  # 1 = list of subdirectories in working_directory
    sample_dirs = []
    for directory in all_subdirs:
        if directory.__contains__('Case'):
            sample_dirs.append(directory)
    return sample_dirs


def choose_index(extension, sample_dirs=None):
    if sample_dirs:
        for i in sample_dirs:
            print(i)
    # Select file, print output to confirm choice
    chosen_index = input('Choose \'' + extension + '\' file by entering the corresponding number:\n')
    if int(chosen_index) < 10 and len(chosen_index) >= 2:
        chosen_index = int(chosen_index[-1])
    if int(chosen_index) > 100 and len(chosen_index) >= 3:
        chosen_index = int(chosen_index)
    else:
        chosen_index = int(chosen_index)
    return chosen_index


def get_file_list(sample_dirs, dir_index, extension):
    file_list = []
    for file_name in next(os.walk(sample_dirs[dir_index]))[2]:  # 2 = list all files
        if file_name.__contains__(extension):
            file_list.append(file_name)
    return sorted(file_list)


def get_sample_data(sample_dirs, dir_index, file_names):
    width, height = pil.open(sample_dirs[dir_index] + '/' + file_names[0]).size
    sample_size = len(file_names)
    all_png_data = np.zeros((width * height, sample_size), int)
    for index in range(sample_size):
        temp_data = pil.open(sample_dirs[dir_index] + '/' + file_names[index])
        temp_data = np.asarray(temp_data.convert('L')).flatten()
        all_png_data[:, index] = temp_data[:, ]
    return all_png_data


def transform_data(all_png_data):
    axisNum = 1  # axis=1, work along the rows, axis=0, work along the rows
    mean_data = all_png_data.mean(axisNum, keepdims=True)
    centered_data = all_png_data - mean_data
    U, S, VT = np.linalg.svd(centered_data)
    D, N = centered_data.shape
    sigma = np.hstack([np.diag(S), np.zeros((N, 0))])
    reduced_data = (sigma @ VT)[:2, :]
    return reduced_data
