"""
From https://stackoverflow.com/questions/23667646/python-replace-zeros-in-matrix-with-circle-of-ones
"""

import numpy as np
import matplotlib.pyplot as plt

z = np.zeros((20, 20))

# specify circle parameters: centre ij and radius
ci, cj = 7, 14
cr = 2

# Create index arrays to z
I, J = np.meshgrid(np.arange(z.shape[0]), np.arange(z.shape[1]))

# calculate distance of all points to centre
dist = np.sqrt((I - ci) ** 2 + (J - cj) ** 2)

# Assign value of 1 to those points where dist<cr:
print(z[np.where(dist < cr)])
z[np.where(dist < cr)] = 1
print(z)

# show result in a simple plot
fig = plt.figure()
ax = fig.add_subplot(111)
ax.pcolormesh(z)
ax.set_aspect('equal')
# plt.show()
