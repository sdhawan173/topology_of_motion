import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pickle as pkl
import file_code as fc

PWD = os.getcwd()
COLOR = 'red'
mpl.rcParams['text.color'] = COLOR
mpl.rcParams['axes.labelcolor'] = COLOR
mpl.rcParams['axes.edgecolor'] = COLOR
mpl.rcParams['xtick.color'] = COLOR
mpl.rcParams['ytick.color'] = COLOR


def transform_data(all_png_data, sample_dir, dir_index):
    reduced_data = None
    print('Checking for existing data file ... ', end="")
    variable_name = 'reduced_data'
    extension = '.pkl'
    file_exists, file_dir = fc.file_check(variable_name, sample_dir, dir_index, extension)
    if file_exists:
        print('\'.pkl\' file found!')

        reduced_data = pkl.load(open(file_dir, 'rb'))
    elif not file_exists:
        print('\'.pkl\' file not found.')

        print('Transforming data with SVD ...')
        axisNum = 1  # axis=1, work along the rows, axis=0, work along the rows
        mean_data = all_png_data.mean(axisNum, keepdims=True)
        centered_data = all_png_data - mean_data
        U, S, VT = np.linalg.svd(centered_data)
        D, N = centered_data.shape
        sigma = np.hstack([np.diag(S), np.zeros((N, 0))])
        reduced_data = (sigma @ VT)[:2, :]

        fc.pickle_dump(reduced_data, sample_dir, dir_index)
    return reduced_data


def save_score_plot(svd_reduction, sample_dir, dir_index):
    motion_type = sample_dir[dir_index].split('- ')[-1]
    plot_type = 'SVD score plot'
    extension = '.png'
    file_name = plot_type + ' - ' + motion_type
    output_name = PWD + '/' + sample_dir[dir_index] + '/' + file_name
    fig, ax = plt.subplots()
    ax.set_facecolor('black')
    fig.patch.set_facecolor('black')
    ax.scatter(
        svd_reduction[0, :],
        svd_reduction[1, :],
        s=5,
        c='red'
    )
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.title(motion_type + ' ' + plot_type)
    file_exists, file_dir = fc.file_check(file_name, sample_dir, dir_index, extension)
    if file_exists:
        plt.show()
    elif not file_exists:
        plt.savefig(output_name + extension, bbox_inches='tight')
