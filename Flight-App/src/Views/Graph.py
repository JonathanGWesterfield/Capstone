from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import csv
import math

def readCoordinates(filename, timeStep):
    """
    Reads the input file of drone coordinates, where a 3d coordinate is stored as a row. Also takes in a value timeStep
    denoting the time difference (in seconds) between coordinates.
    :return: An array of x coordinates, an array of y coordinates, an array of z coordinates, an array of time values
    as seconds counting up from 0 with change timeStep between two legal inputs.
    """
    # Initialize time at 0
    initialTime = 0
    timeDiff = initialTime

    # Initialize arrays
    x, y, z, timearray = [], [], [], []

    # Read line by line through the file. Only add the point if legal input. Time value should still increment even if
    # value is illegal input.
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=' ')
        for row in reader:
            if (checkLegalInput(row[0],row[1],row[2])):
                x.append(float(row[0]))
                y.append(float(row[1]))
                z.append(float(row[2]))
                timearray.append(timeDiff)
            timeDiff = timeDiff + timeStep

    # Return arrays
    return x, y, z, timearray

def checkLegalInput(x, y, z):
    """
    Checks if the inputted 3D coordinate is within legal bounds. Legal bounds are:
    x, y, z > 0 and x < 30 and y < 15 and z < 10
    return: A boolean denoting if legal or not (true if legal, false if outside bounds).
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
    elif x > 30:
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

def velocityPoints(x, y, z, timearray):
    """
    Calculates the velocity of the drone between consecutive points for the entire flight.
    Input: array of x coordinates, array of y coordinates, array of z coordinates, array of time values as seconds
    counting up from 0.
    :return: An array of velocity points for the drone.
    """
    if len(x) != len(y) or len(y) != len(z) or len(y) != len(x):
        raise Exception('Coordinate arrays are different sizes')
    velocityArray = []
    i=0
    for i in range(len(x)-1):
       vel = computeVelocity(x[i], y[i], z[i],x[i+1],y[i+1],z[i+1],timearray[i],timearray[i+1])
       velocityArray.append(vel)

    return velocityArray

def velocityColors(vel):
    """
    Determines the color of the line segment between two points based on velocity values. The line color is determined
    by the change in velocity of the drone between two points. The color of the line should be green if the
    velocity point is greater than the previous velocity point, yellow if within 0.5 m/s, and red if less.
    :return: An array of color values to use when plotting line segments between points.
    """
    colors = ['g']
    for i in range(len(vel) - 1):
        velDelta = vel[i+1]-vel[i]
        if velDelta < 0:
            colors.append('r')
        elif velDelta > 0 and velDelta < 0.5:
            # TODO: tune this range (if the velocities are within x of each other, consider it "constant")
            colors.append('y')
        else:
            colors.append('g')
    return colors

def generateGraph(x, y, z, timearray):
    """
    Driver function for generating the 3d graph of drone coordinates.
    Input: array of x coordinates, array of y coordinates, array of z coordinates, array of time values as seconds
    counting up from 0.
    :return: The figure to display as the 3d graph.
    """
    # Plot points on the graph
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x, y, z, s=6, c="k", marker='o')

    # Get velocities and line segment coloring
    vel = velocityPoints(x, y, z, timearray)
    colors = velocityColors(vel)

    # Add line segment coloring
    for i in range(len(vel)):
        plt.plot([x[i], x[i + 1]], [y[i], y[i + 1]], [z[i], z[i + 1]], colors[i], linewidth = 1)

    # TODO: try to use the below method to do all the plotting in one swoop (may be faster)
    # ax.plot(x, y, z, '-p', color=colors,
    #         markersize=15, linewidth=4,
    #         markerfacecolor='white',
    #         markeredgecolor='gray',
    #         markeredgewidth=2)

    # Set axis limits
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.set_xlim3d(0, 30)
    ax.set_ylim3d(0, 15)
    ax.set_zlim3d(0, 10)
    ax.set_title("Flight Path")

    return fig