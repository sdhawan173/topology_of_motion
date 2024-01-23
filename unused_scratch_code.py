def insert_points(image_array, pixel_array):
    for pixel in pixel_array:
        for rgb_val in range(3):
            x_val = pixel[0][0]
            y_val = pixel[0][1]
            image_array[x_val][y_val][rgb_val] = pixel[1][rgb_val]
    return image_array


width = 5

test = []
for i in range(width):
    temp = []
    for j in range(width):
        str1=''
        str2=''
        if i < 10:
            str1 = '0' + str(i)
        if j < 10:
            str2 = '0' + str(j)
        if i < 10 and j < 10:
            str1 = '0' + str(i)
            str2 = '0' + str(j)
        else:
            str1 = str(i)
            str2 = str(j)
        temp.append([str1, str2])
    test.append(temp)

for i in range(width):
    print(test[i])
