from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt 

import numpy as np

import json

from detect import DroneTracker

if __name__ == "__main__":

    tracker = DroneTracker("D:/Projects/Capstone/DroneDetection/video/pixel_synced_Trim_Trim.mp4",
                            "D:/Projects/Capstone/DroneDetection/video/s10_synced_Trim_Trim.mp4")

    data = tracker.process_video() # y/z plane

    x_coords = []
    y_coords = []
    z_coords = []
    t_vals =[]

    for tup in data:
        t_vals.append(tup[0])
        x_coords.append(tup[1])
        y_coords.append(tup[2])
        z_coords.append(tup[3])

    fig = plt.figure()

    plot = fig.add_subplot(111, projection="3d")

    plot.scatter(x_coords, y_coords, z_coords, s=6, c="k", marker="o")

    plot.set_xlabel("x")
    plot.set_ylabel("y")
    plot.set_zlabel("z")
    plot.set_title("flight path")

    plot.set_xlim3d(0, 15)
    plot.set_ylim3d(0, 15)
    plot.set_zlim3d(0, 10)

    plt.show()

    output = {"coords": data}
    formatted = json.dumps(output, sort_keys=True, indent=4)

    print(formatted)
