import json

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

f = open("sample_data.flight", "r")
flightData = json.load(f)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
x_data = []
y_data = []
z_data = []

for coord in flightData["legalPoints"]:
    x_data.append(coord[1])
    y_data.append(coord[2])
    z_data.append(coord[3])


ax.scatter(x_data, y_data, z_data, s=6, c="k", marker='o')

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.set_xlim3d(0, 15)
ax.set_ylim3d(0, 15)
ax.set_zlim3d(0, 10)
ax.set_title("Flight Path")

fig.show()
plt.show()