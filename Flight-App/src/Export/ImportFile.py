import json

def importData(inPath):
    """
    Imports the flight data from a JSON file stored with a ".flight" extension.
    :param inPath: String containing the pilot name
    :return: pilotName, instructorName, flightDate, flightLength, flightInstructions, x, y, z, velocityPoints
    """

    with open(inPath, 'r') as infile:
        flightDict = json.load(infile)
        print(flightDict)

    return flightDict

importData('../Tests/TestFiles/JSONDUMP.flight')