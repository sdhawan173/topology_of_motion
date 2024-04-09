import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import file_code as fc

PWD = os.getcwd()
COLOR = 'white'
mpl.rcParams['text.color'] = COLOR
mpl.rcParams['axes.labelcolor'] = 'red'
mpl.rcParams['axes.titlecolor'] = 'red'
mpl.rcParams['axes.edgecolor'] = COLOR
mpl.rcParams['xtick.color'] = COLOR
mpl.rcParams['ytick.color'] = COLOR


def transform_data(all_png_data, sample_dir, dir_index):
    print('Transforming data with SVD ...')
    axisNum = 1  # axis=1, work along the rows, axis=0, work along the rows
    print('-----Centering data ...')
    mean_data = all_png_data.mean(axisNum, keepdims=True)
    centered_data = all_png_data - mean_data
    print('-----Running svd ...')
    U, S, VT = np.linalg.svd(centered_data)
    D, N = centered_data.shape
    sigma = np.hstack([np.diag(S), np.zeros((N, 0))])
    reduced_data = (sigma @ VT)[:2, :]
    fc.pickle_dump(reduced_data, 'reduced_data', sample_dir, dir_index)
    return reduced_data


def save_score_plot(svd_reduction, sample_dir, dir_index, show_plot=False):
    fig, ax = plt.subplots()
    indicies = [i for i in range(len(svd_reduction[0, :]))]
    labels = [str(i) for i in indicies]

    norm_color_values = np.array(indicies)/max(indicies)
    colors = [plt.get_cmap('Reds')(value) for value in norm_color_values]
    ax.set_facecolor('black')
    fig.patch.set_facecolor('black')

    score_plot = ax.scatter(
        svd_reduction[0, :],
        svd_reduction[1, :],
        s=5,
        c=indicies,
        cmap='Reds',
        vmax=max(indicies)
    )
    for label, x, y, color in zip(labels, svd_reduction[0, :], svd_reduction[1, :], colors):
        ax.annotate(label, (x, y), c=color)
    color_bar = plt.colorbar(score_plot,
                             ax=ax,
                             ticks=np.arange(
                                 start=0,
                                 stop=max(indicies),
                                 step=5)
                             )
    color_bar.set_label('Frame Count')
    motion_type = sample_dir[dir_index].split('- ')[-1]
    plot_type = 'SVD score plot'
    extension = '.svg'
    file_name = motion_type + ' - ' + plot_type
    output_name = fc.create_output_name(PWD, sample_dir, dir_index, file_name, extension)
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.title(motion_type + ' ' + plot_type)
    plt.savefig(output_name, bbox_inches='tight')
    if show_plot:
        plt.show()
