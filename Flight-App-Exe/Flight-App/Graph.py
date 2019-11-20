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
    """
    Calculates the dimensionless jerk for a 1 dimensional array of points.

    :param movement: The numpy array of points to calculate the jerk for. The array containing the movement speed profile. Doesn't need to be numpy array but it MUST at least be a 1 dimensional list.
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

    :param movement: The numpy array of points to calculate the jerk for. The array containing the movement speed profile. Doesn't need to be numpy array but it MUST at least be a 1 dimensional list.
    :param fs: The sampling frequency of the data points.
    :return: The dimensionless jerk estimate of the given movement's smoothness.
    """
    return -np.log(abs(dimensionless_jerk(movement, fs)))

def generateGraph(flightData: dict, displayVelocity: bool, t1: float, t2: float):
    """
    Driver function for generating the 3d graph of drone coordinates.

    :param flightData: Dictionary containing flight data.
    :param displayVelocity: Boolean saying if velocity changes should be displayed on the graph.
    :param t1: Minimum time bound for plotting coordinates.
    :param t2: Maximum time bound for plotting coordinates.
    :return: The figure to display as the 3d graph.
    """
    # Plot points on the graph
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x_data = []
    y_data = []
    z_data = []
    if displayVelocity is False:
        # for coord in flightData["legalPoints"]:
        for coord in flightData["coords"]:
            if (coord[0] is not None and coord[1] is not None):
                if coord[0] >= t1 and coord[0] <= t2:
                    # x_data.append(15 - coord[1])
                    x_data.append(coord[1])
                    y_data.append(coord[2])
                    # z_data.append(10 - coord[3])
                    z_data.append(coord[3])

        ax.scatter(x_data, y_data, z_data, s=6, c="k", marker='o')

    if displayVelocity is True:
        # Get velocities and line segment coloring
        colors = velocityColors(flightData)

        # Add line segment coloring
        for i in range(len(flightData["legalPoints"])-1):
            if flightData["legalPoints"][i][0] >= t1 and flightData["legalPoints"][i][0] <= t2 \
                    and flightData["legalPoints"][i+1][0] <= t2:
                ax.scatter(flightData["legalPoints"][i][1], flightData["legalPoints"][i][2],
                         flightData["legalPoints"][i][3], s=6, c=colors[i], marker='o')
                plt.plot([flightData["legalPoints"][i][1], flightData["legalPoints"][i+1][1]],
                         [flightData["legalPoints"][i][2], flightData["legalPoints"][i+1][2]],
                         [flightData["legalPoints"][i][3], flightData["legalPoints"][i+1][3]],
                         colors[i], linewidth=1)

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
# with open('../Tests/TestFiles/new_size100_legal80.flight', 'r') as infile:
#     flightDict = json.load(infile)
# flightDict = {}
#
# flightDict["coords"] = [
#     [
#         0.0,
#         12.1171875,
#         12.6328125,
#         6.699074074074074
#     ],
#     [
#         0.5,
#         12.12109375,
#         12.640625,
#         6.6967592592592595
#     ],
#     [
#         1.0,
#         12.13671875,
#         12.65625,
#         6.694444444444444
#     ],
#     [
#         1.5,
#         12.1328125,
#         12.65625,
#         6.69212962962963
#     ],
#     [
#         2.0,
#         12.12109375,
#         12.640625,
#         6.68287037037037
#     ],
#     [
#         2.5,
#         12.109375,
#         12.609375,
#         6.657407407407407
#     ],
#     [
#         3.0,
#         12.10546875,
#         12.5859375,
#         6.62962962962963
#     ],
#     [
#         3.5,
#         12.1015625,
#         12.5546875,
#         6.601851851851852
#     ],
#     [
#         4.0,
#         12.1015625,
#         12.515625,
#         6.576388888888889
#     ],
#     [
#         4.5,
#         12.1015625,
#         12.46875,
#         6.546296296296297
#     ],
#     [
#         5.0,
#         12.1015625,
#         12.37890625,
#         6.504629629629629
#     ],
#     [
#         5.5,
#         12.10546875,
#         12.203125,
#         6.458333333333334
#     ],
#     [
#         6.0,
#         12.125,
#         11.92578125,
#         6.400462962962963
#     ],
#     [
#         6.5,
#         12.16015625,
#         11.5390625,
#         6.351851851851852
#     ],
#     [
#         7.0,
#         12.19921875,
#         11.08203125,
#         6.298611111111111
#     ],
#     [
#         7.5,
#         12.24609375,
#         10.55859375,
#         6.256944444444445
#     ],
#     [
#         8.0,
#         12.29296875,
#         9.98046875,
#         6.212962962962964
#     ],
#     [
#         8.5,
#         12.33984375,
#         9.4140625,
#         6.141203703703704
#     ],
#     [
#         9.0,
#         12.40625,
#         8.82421875,
#         6.05787037037037
#     ],
#     [
#         9.5,
#         12.4921875,
#         8.25390625,
#         5.995370370370371
#     ],
#     [
#         10.0,
#         12.56640625,
#         7.750000000000001,
#         5.9375
#     ],
#     [
#         10.5,
#         12.61328125,
#         7.25,
#         5.900462962962964
#     ],
#     [
#         11.0,
#         12.6484375,
#         6.71484375,
#         5.868055555555555
#     ],
#     [
#         11.5,
#         12.67578125,
#         6.25390625,
#         5.837962962962963
#     ],
#     [
#         12.0,
#         12.6953125,
#         5.87109375,
#         5.805555555555556
#     ],
#     [
#         12.5,
#         12.703125,
#         5.5546875,
#         5.770833333333333
#     ],
#     [
#         13.0,
#         12.7421875,
#         5.2734375,
#         5.712962962962963
#     ],
#     [
#         13.5,
#         12.859375,
#         5.01953125,
#         5.625
#     ],
#     [
#         14.0,
#         13.0625,
#         4.80859375,
#         5.541666666666667
#     ],
#     [
#         14.5,
#         13.3046875,
#         4.5859375,
#         5.467592592592593
#     ]
# ]
# flightDict = checkCoordinates(flightDict)
# flightDict = velocityPoints(flightDict)
# flightDict = computeVelocityStatistics(flightDict)
#
# flightDict["smoothness"] = log_dimensionless_jerk(flightDict["velocities"], 0.5)
# print(flightDict["smoothness"])
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