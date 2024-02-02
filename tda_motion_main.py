import image_preprocessing as ipp
import file_code as fc


ext = '.png'
sample_directories = fc.get_sample_dirs()
sample_index = fc.choose_index(ext, sample_dirs=sample_directories)
png_file_names = fc.get_file_list(sample_directories, sample_index, extension='.png')
all_png_data = fc.get_sample_data(sample_directories, sample_index, png_file_names)
svd_reduction = ipp.transform_data(all_png_data, sample_directories, sample_index)
ipp.save_score_plot(svd_reduction, sample_directories, sample_index)
