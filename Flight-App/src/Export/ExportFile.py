import json

def export_data(pilotName, instructorName, flightDate, flightLength,
                xCoordinates, yCoordinates, zCoordinates, velocityValues, outPath):
    """
    Exports the flight data to a JSON file stored with a ".flight" extension.
    :return: none
    """
    flight = {}
    flight['flight'] = {
        "Pilot Name" : pilotName,
        "Instructor" : instructorName, 
        "Flight Date" : flightDate,
        "Flight Length" : flightLength,
        "x-Coordinates" : xCoordinates,
        "y-Coordinates" : yCoordinates,
        "z-Coordinates" : zCoordinates,
        "Velocity Values" : velocityValues
    }
    with open(outPath, "w") as outfile:
        json.dump(flight, outfile, indent= 4)

## Below is a runnable code to test the formatting 
# export_data("ariana", "robin", "date", "xcoord", "ycoord", "zcoord", "time", "velocity")
'''
## The following segment creates arrays of x,y,z coordinates located in random_size10_legal80.txt files
## Thereafter, a call to the "export_file()" function is called with the new arrays. 
xs = []
ys = []
zs = []
with open("../Tests/TestFiles/random_size10_legal80.txt", "r") as infile:
    for line in infile:
        x, y, z = line.split()
        xs.append(x)
        ys.append(y)
        zs.append(z)
## For testing purposes, to see if the code outputs x, y, z coordinate arrays as expected 
# for line in range(len(xs)):
#     print(xs[line])
# print('\n')
# for line in range(len(ys)):
#     print(ys[line])
# print('\n')
# for line in range(len(zs)):
#     print(zs[line])
# print('\n')
# another call to the function to test the arrays of x,y,z coordinates in the random_size10_legal80.txt file
export_data("Ariana Boroujerdi", "Robin Murphy", "11/1/2019", "00:00:00", xs,ys,zs, "Velocity", "ExportedFiles/Hayley.flight")
'''
