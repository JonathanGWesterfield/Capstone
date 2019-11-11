import matplotlib.pyplot as plt 

import numpy as np 

fig = plt.figure()

plot = fig.add_subplot(111, projection="3d")

plot.scatter(x_array, y_array, z_array, s=6, c="k", marker="o")

fig.show()