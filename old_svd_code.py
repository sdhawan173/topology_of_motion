import numpy as np
from numpy import asarray
import matplotlib.pyplot as plt
import os
import glob
import PIL.Image

# INITIALIZE IMPORTANT VARIABLES
# Create string variable to store directory of images
pwd = os.getcwd()
Folder = '/CatMotion/*.jpg'
dirString = pwd + Folder
print("pwd =", dirString)

# Create variable to show number of images
imgTotal = len(glob.glob(dirString))

# Create String variables to be used in for loop to load in images
picDir = os.getcwd()
name = 'CatMotion'
ext = 'ss.jpg'

# Load test image
i = 0
num = str(i + 1)
call = picDir + name + num + ext
image = PIL.Image.open(call)

# Find size of images
width, height = image.size
x = height
y = width
print("Image Width:", width, "; Image Height:", height)

# Create labels for each image
labels = [str(i + 1) for i in range(24)]
print(labels)

# Set variables to be used with array indices and means
columns = width * height
rows = imgTotal
axisNum = 1  # axis=1, work along the rows, axis=0, work along the rows

# CREATE EMPTY ARRAY TO STORE FLATTENED B&W IMAGE DATA
images = np.zeros((columns, rows), int)
print("Size of Empty Array:", images.shape)

# CONVERT ALL IMAGES TO "IMAGES" ARRAY
for i in range(imgTotal):
    #    print(i) #debugging code
    num = str(i + 1)
    call = picDir + name + num + ext
    #    print(call) #debugging code
    imgtmp = PIL.Image.open(call)
    imgtmp = imgtmp.convert('L')
    imgtmp = asarray(imgtmp)
    imgtmp = imgtmp.flatten()
    images[:, i] = imgtmp[:, ]
print("Shape of Images Array:", images.shape)

# CENTERING THE DATA
# Compute the mean of the axis
meanData = images.mean(axisNum, keepdims=True)
centeredData = images - meanData
print("Centered Data Shape:", centeredData.shape)

# DISPLAY FIRST IMAGE OF CENTERED DATA
plt.imshow(centeredData[:, 0].reshape(x, y), cmap='gray')
plt.savefig('CenteredData.jpg', dpi=240, bbox_inches='tight')
plt.show()

# SVD CODE
U, S, VT = np.linalg.svd(centeredData)
print("Shape of U:", U.shape)
print("Shape of S:", S.shape)
print("Shape of VT:", VT.shape)
# print("S:",S)

# CREATE SCORE PLOT
print("Shape of np.diag(S):", np.diag(S).shape)
D, N = centeredData.shape
print("D = ", D, "; N =", N)
Sigma = np.hstack([np.diag(S), np.zeros((N, 0))])
print("Shape of Sigma:", Sigma.shape)
print("Shape of V:", VT.shape)
reducedData = (Sigma @ VT)[:2, :]
print("Shape of Reduced Data =", reducedData.shape)

plt.scatter(
    reducedData[0, :],
    reducedData[1, :],
    s=5
)
for i in range(24):
    plt.annotate(labels[i], (reducedData[0, i], reducedData[1, i]))
plt.title('Score Plot of First Two Principal Components')
plt.ylabel('PC2')
plt.xlabel('PC1')
plt.savefig('ScorePlot.jpg', dpi=240, bbox_inches='tight')
plt.show()
