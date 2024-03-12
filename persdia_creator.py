import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def create_base_plot(persistence_points, title, max_dim=2):
    # Create Plot
    fig, ax = plt.subplots()
    cmap = matplotlib.cm.Set1.colors
    ax.set_facecolor('black')
    fig.patch.set_facecolor('black')
    plt.gca().set_aspect(0.8)
    plt.rc(group='axes', labelsize=12)
    plt.xlabel('Birth')
    plt.ylabel('Death')

    for point in persistence_points:
        ax.scatter(point[1][0], point[1][1], color=cmap[point[0]], alpha=0.75, s=45, zorder=10, clip_on=False)
    ax.set_title('Persistence Diagram of\n{}'.format(title))
    ax.legend(
        handles=[
            mpatches.Patch(
                color=cmap[dim],
                label=r'$H_{}$'.format(str(dim))) for dim in list(range(0, max_dim + 1))
        ],
        labelcolor='linecolor',
        handlelength=1,
        handleheight=1,
        loc=4
    )

    # Create frequency labels for overlapping points
    frequency_values, frequency_coords = persistence_frequencies(persistence_points)

    # Create annotations for overlapping points
    for index, annotation in enumerate(frequency_values):
        x_coord, y_coord = frequency_coords[index]
        ax.annotate(annotation, (x_coord, y_coord), xytext=(5, 3), textcoords='offset points', fontsize=12, zorder=11)
    return fig, ax


def persistence_frequencies(persistence_points):
    """
    :param persistence_points: list of persistence diagram points
    return: list of frequencies for points that occur more than once, coordinates of points that occur more than once.
    """
    # Create list of indices for unique points in the persistence points list
    unique_points = set((point[1][0], point[1][1]) for point in persistence_points)
    unique_indices = [index for index, point in enumerate(persistence_points) if
                      (point[1][0], point[1][1]) in unique_points]

    # Create list of frequencies for overlapping unique points
    frequency_values = []
    frequency_coords = []
    for index in range(len(persistence_points)):
        point_count = 0

        # Count number of overlapping points
        if unique_indices.__contains__(index):
            point_count = persistence_points.count(persistence_points[index])

        # Add total of overlapping points and respective coordinates
        if point_count > 1:
            append_value = str(point_count)
            frequency_values.append(append_value)
            frequency_coords.append([persistence_points[index][1][0],
                                     persistence_points[index][1][1]])
    return frequency_values, frequency_coords


def infinity_handler(persistence_points, max_factor=1.1, inf_factor=1.15, max_dim=2):
    persistence_points = [(point[0], (point[1][0], point[1][1])) for point in persistence_points if point[0] <= max_dim]
    y_values = [point[1][1] for point in persistence_points]

    # Set value for infinity line/infinity annotation by increasing tick height of max y value
    y_max_orig = None
    y_max_tick = None
    y_inf_tick = None
    inf_bool = False
    if not len(y_values) == 1:
        # If persistence points contain infinity, repalce math.inf with math.nan
        if y_values.__contains__(math.inf):
            # Get maximum non-infinity y_value
            y_max_orig = max([val for val in y_values if not math.isinf(val)])

            # Increase maximum y_value by increase factors to create location for infinity, set alternate y_max
            y_max_tick = y_max_orig * max_factor
            y_inf_tick = y_max_orig * inf_factor

            # replace math.inf value with new y_max value
            for index in range(len(y_values)):
                if math.isinf(y_values[index]):
                    y_values[index] = y_inf_tick
    elif len(y_values) == 1:
        y_values = [2]
        y_max_orig = 2
        y_max_tick = 2
        y_inf_tick = 2
        inf_bool = True

    # Update persistence points with new y values
    new_persistence = []
    for point, y_val in zip(persistence_points, y_values):
        new_persistence.append([point[0], [point[1][0], y_val]])
    return new_persistence, y_max_orig, y_max_tick, y_inf_tick, inf_bool


def mpl_tick_handler(ax, y_max_orig, y_max_tick, y_inf_tick):
    # Create gap between infinity line and top of plot
    y_buffer_space = y_max_orig * 1.2

    # Alter original x and y limits with new y_max
    plt.xlim(0, y_max_orig)
    plt.ylim(0, y_max_tick)

    # Create new y_ticks
    y_ticks = [i for i in plt.yticks()[0]]
    y_ticks[-1] = y_inf_tick
    y_ticks.append(y_buffer_space)

    # Create new y_labels with new y_ticks
    y_labels = [str('{:.2f}'.format(round(i, 2))) for i in y_ticks]
    y_labels[-2] = r'$\infty$'
    y_labels[-1] = ''

    # Set y_ticks and labels
    ax.set_yticks(y_ticks, labels=y_labels)
    plt.yticks()[1][-2].set_fontsize(18)

    # Create diagonal dashed line
    plt.plot([0, y_max_tick], [0, y_max_tick], linestyle='dashed', linewidth=0.75, c='black')

    # Create gray shaded area below line y=x
    x = np.linspace(0, y_max_tick, 100)
    y = x
    plt.fill_between(x, y, color='lightgray', where=(y <= x), alpha=0.5, zorder=0)

    # create solid horizontal line for infinity
    plt.axvline(0, color='black')
    plt.gca().axhline(y_inf_tick, linestyle='solid', linewidth=0.75, c='black')


def plot_persdia_main(persistence_points, title, save_dir, show_plot=False):
    """
    plots the persistence diagram of the gudhi_simplex_tree generated by smm.create_simplex.
    :param persistence_points: persistence points of simplex tree from selected complex
    :param title: Title of plot
    :param save_dir: String of full file path (including extension) to save plot file to
    :param show_plot: Boolean to show plot, default=False
    """
    print('\nPlotting Persistence Diagram ...')

    # Adjust dimensions to be shown
    persistence_points, y_max_orig, y_max_tick, y_inf_tick, inf_bool = infinity_handler(persistence_points)

    # Create initial plot
    fig, ax = create_base_plot(persistence_points, title)

    # Assign values for certain ticks
    mpl_tick_handler(ax, y_max_orig, y_max_tick, y_inf_tick)

    file_path = save_dir.split('.')[0]
    extension = save_dir.split('.')[1]
    plt.savefig(file_path + '.' + extension, bbox_inches='tight', dpi=300, format=extension)
    print('Persistence Diagram saved to {}'.format(save_dir))

    if show_plot:
        plt.show()


def save_persistence_points(persistence_points, save_file_name):
    with open(save_file_name, 'w') as file:
        for line in persistence_points:
            file.write(f"{line}\n")
