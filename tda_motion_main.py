import numpy as np
import image_generator as ig


width = 100
height = width
sample_size = 50
motion_name = 'circle (triangular generation)'
start_point = 0
end_point = width
domain = np.linspace(start_point, end_point, num=sample_size)
x_values = [int((width / 3) * (1 + point)) for point in np.cos(domain)]
y_values = [int((width / 3) * (1 + point)) for point in np.sin(domain)]
radius = 5
color = [255, 0, 0]
png_collection = ig.generate_data_samples(motion_name, x_values, y_values,
                                          width, height, radius, color,
                                          save_png=True)
ig.generate_gif(motion_name)
