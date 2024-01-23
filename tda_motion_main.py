import matplotlib.pyplot as plt
import image_preprocessing as ipp


ext = '.png'
sample_directories = ipp.get_sample_dirs()
# sample_index = choose_index(ext, sample_dirs = sample_directories)
sample_index = 0
png_file_names = ipp.get_file_list(sample_directories, sample_index, extension='.png')
all_png_data = ipp.get_sample_data(sample_directories, sample_index, png_file_names)
svd_reduction = ipp.transform_data(all_png_data)
plt.scatter(
    svd_reduction[0, :],
    svd_reduction[1, :],
    s=5
)
plt.show()
