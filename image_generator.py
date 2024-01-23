import numpy as np
import png


def create_blank_image(image_width, image_height):
    image_array = []
    for x in range(image_width):
        temp_array = []
        for y in range(image_height):
            temp_pixel = []
            for _ in range(3):
                temp_pixel.append(0)
            temp_array.append(temp_pixel)
        image_array.append(temp_array)
    return image_array


def insert_circle(image_array, image_width, image_height,
                  x_coord, y_coord, radius, point_color):
    """
    Originally from https://stackoverflow.com/questions/23667646/python-replace-zeros-in-matrix-with-circle-of-ones
    """
    image_array = np.array(image_array)

    # Create index arrays to z
    I, J = np.meshgrid(np.arange(image_width), np.arange(image_height))

    # calculate distance of all points to centre
    dist = np.sqrt((I - x_coord) ** 2 + (J - y_coord) ** 2)

    # Assign value of 1 to those points where dist<radius:
    image_array[np.where(dist <= radius)] = point_color

    return np.asarray(image_array)


def convert_to_png(image_array, image_width, image_height):
    png_array = []
    for x in range(image_width):
        temp = []
        for y in range(image_height):
            for z in range(4):
                if z < 3:
                    temp.append(image_array[x][y][z])
                elif z == 3:
                    temp.append(255)
        png_array.append(temp)
    return png_array


width = 1000
height = width
image_data = create_blank_image(width, height)
red = [255, 0, 0]
image_data = insert_circle(image_data, width, height,
                           300, 500, 40, red)

png_data = convert_to_png(image_data, width, height)

image_count = 0
image_string = 'motion 01 - circle'
count_string = ''
if image_count < 10:
    count_string = '00' + str(image_count)
if image_count < 100:
    count_string = '0' + str(image_count)
with open(image_string, 'wb') as data_sample:
    w = png.Writer(width, height, greyscale=False, alpha='RGBA')
    w.write(data_sample, png_data)
