import json

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import csv
import math
import statistics
import numpy as np
import re

def checkCoordinates(flightDict: dict):
    """
    Reads the input dictionary of flight data from a .flight file.
    :param flightDict: Dictionary containing flight data.
    :return: Dictionary of flight data.
    """
    legalPoints = []
    for coord in flightDict["coords"]:
        if checkLegalInput(coord[1], coord[2], coord[3]):
            legalPoints.append(coord)

    flightDict["legalPoints"] = legalPoints
    return flightDict

def checkLegalInput(x, y, z):
    """
    Checks if the inputted 3D coordinate is within legal bounds. Legal bounds are:
    x, y, z > 0 and x < 15 and y < 15 and z < 10.
    :param x: x value to check.
    :param y: y value to check.
    :param z: z value to check.
    :return: A boolean denoting if legal or not (true if legal, false if outside bounds).
    """
    try:
        x = float(x)
        y = float(y)
        z = float(z)
    except:
        return False
    if math.isnan(x) or math.isnan(y) or math.isnan(z):
        return False
    elif x < 0 or y < 0 or z < 0:
        return False
    elif x > 15:
        return False
    elif y > 15:
        return False
    elif z > 10:
        return False
    else:
        return True

    return True

def computeVelocity(x1, y1, z1, x2, y2, z2, t1, t2):
    """
    Computes the velocity of the drone between two points (x1,y1,z1) and (x2,y2,z2) at respective times t1 and t2.
    :return: A float value representing the velocity of the drone.
    """
    distance = math.sqrt(math.pow(x2 - x1, 2) +
                  math.pow(y2 - y1, 2) +
                  math.pow(z2 - z1, 2) * 1.0)
    timestep = t2 - t1
    velocity = distance/timestep
    return velocity

def velocityPoints(flightData: dict):
    """
    Calculates the velocity of the drone between consecutive points for the entire flight.
    :param flightData: Dictionary of flight Data.
    :return: Modified flightData dictionary.
    """
    velocityArray = []
    for i in range(len(flightData["legalPoints"])-1):
       vel = computeVelocity(flightData["legalPoints"][i][1], flightData["legalPoints"][i][2], flightData["legalPoints"][i][3],
                             flightData["legalPoints"][i+1][1], flightData["legalPoints"][i+1][2], flightData["legalPoints"][i+1][3],
                             flightData["legalPoints"][i][0], flightData["legalPoints"][i+1][0])
       velocityArray.append(vel)

    flightData["velocities"] = velocityArray

    return flightData

def velocityColors(flightDict: dict):
    """
    Determines the color of the line segment between two points based on velocity values. The line color is determined
    by the change in velocity of the drone between two points. The color of the line should be green if the
    velocity point is greater than the previous velocity point, yellow if within 0.5 m/s, and red if less.
    :param flightDict: Dictionary of flight data.
    :return: An array of color values to use when plotting line segments between points.
    """
    colors = ['g']
    for i in range(len(flightDict["velocities"]) - 1):
        velDelta = flightDict["velocities"][i+1]-flightDict["velocities"][i]
        if velDelta < 0:
            colors.append('r')
        elif velDelta > 0 and velDelta < 0.5:
            # TODO: tune this range (if the velocities are within x of each other, consider it "constant")
            colors.append('y')
        else:
            colors.append('g')
    return colors

def computeVelocityStatistics(flightDict: dict):
    """
    Computes statistics on the velocity points.
    :param flightDict: Dictionary of flight data
    :return: Updated dictionary.
    """
    avgVel = statistics.mean(flightDict["velocities"])
    numArray = np.array(flightDict["velocities"])
    maxVel = np.amax(numArray)
    minVel = np.amin(numArray)

    flightDict["avgVel"] = avgVel
    flightDict["minVel"] = minVel
    flightDict["maxVel"] = maxVel

    return flightDict

def dimensionless_jerk(movement: list, fs: int) -> float:
    """i
    Calculates the dimensionless jerk for a 1 dimensional array of points.
    :param movement: The numpy array of points to calculate the jerk for. The array
        containing the movement speed profile. Doesn't need to be numpy array but it MUST at least be
        a 1 dimensional list.
    :param fs: The sampling frequency of the data points.
    :return: The dimensionless jerk estimate of the given movement's smoothness.
    """
    # first enforce data into an numpy array.
    movement = np.array(movement)

    # calculate the scale factor and jerk.
    movement_peak = max(abs(movement))
    dt = 1. / fs
    movement_dur = len(movement) * dt
    jerk = np.diff(movement, 2) / pow(dt, 2)
    scale = pow(movement_dur, 3) / pow(movement_peak, 2)

    # estimate dj
    return - scale * sum(pow(jerk, 2)) * dt

def log_dimensionless_jerk(movement: list, fs: int) -> float:
    """
    Calculates the smoothness metric for the given speed profile using the log dimensionless jerk
    metric.
    :param movement: The numpy array of points to calculate the jerk for. The array
        containing the movement speed profile. Doesn't need to be numpy array but it MUST at least be
        a 1 dimensional list.
    :param fs: The sampling frequency of the data points.
    :return: The dimensionless jerk estimate of the given movement's smoothness.
    """
    return -np.log(abs(dimensionless_jerk(movement, fs)))

def generateGraph(flightData: dict, displayVelocity: bool):
    """
    Driver function for generating the 3d graph of drone coordinates.
    :param flightData: Dictionary containing flight data
    :param displayVelocity: Boolean saying if velocity changes should be displayed on the graph.
    :return: The figure to display as the 3d graph.
    """
    # Plot points on the graph
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x_data = [x[1] for x in flightData["legalPoints"]]
    y_data = [y[2] for y in flightData["legalPoints"]]
    z_data = [z[3] for z in flightData["legalPoints"]]
    ax.scatter(x_data, y_data, z_data, s=6, c="k", marker='o')

    if displayVelocity is True:
        # Get velocities and line segment coloring
        colors = velocityColors(flightData)

        # Add line segment coloring
        for i in range(len(flightData["legalPoints"])-1):
            plt.plot([flightData["legalPoints"][i][1], flightData["legalPoints"][i+1][1]],
                     [flightData["legalPoints"][i][2], flightData["legalPoints"][i+1][2]],
                     [flightData["legalPoints"][i][3], flightData["legalPoints"][i+1][3]],
                     colors[i], linewidth = 1)

    # Set axis limits
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.set_xlim3d(0, 15)
    ax.set_ylim3d(0, 15)
    ax.set_zlim3d(0, 10)
    ax.set_title("Flight Path")

    return fig

# size = 600
# flightLength = 0.5*size
#
with open('../Tests/TestFiles/new_size100_legal80.flight', 'r') as infile:
    flightDict = json.load(infile)

print(flightDict["smoothness"])
flightDict = checkCoordinates(flightDict)
flightDict = velocityPoints(flightDict)
flightDict = computeVelocityStatistics(flightDict)
flightDict["smoothness"] = log_dimensionless_jerk(flightDict["velocities"], 0.5)
print(flightDict["smoothness"])
#
# with open('../Tests/TestFiles/new_size100_legal80.flight', 'w') as outfile:
#     json.dump(flightDict, outfile)
#
# # test_dict = readCoordinates('../Tests/TestFiles/new_size1200_legal100.flight')
# test_dict = velocityPoints(test_dict)
# test_dict = computeVelocityStatistics(test_dict)
# # print(len(test_dict["coords"]))
# # print(len(test_dict["legalPoints"]))
# generateGraph(test_dict, True)