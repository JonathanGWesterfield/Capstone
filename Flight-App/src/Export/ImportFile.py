import json

def importData(inPath):
    """
    Imports the flight data from a JSON file stored with a ".flight" extension.
    :param inPath: String containing the pilot name
    :return: Flight dictionary
    """

    with open(inPath, 'r') as infile:
        flightDict = json.load(infile)

    return flightDict