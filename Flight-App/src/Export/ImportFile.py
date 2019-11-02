import json

def importData(inPath):
    """
    Imports the flight data from a JSON file stored with a ".flight" extension.
    :param inPath: String containing the pilot name
    :return: pilotName, instructorName, flightDate, flightLength, flightInstructions, x, y, z, velocityPoints
    """

    with open(inPath) as json_file:
        data = json.load(json_file)
        print("Reading file " + inPath)
        pilotName = data['flight']['Pilot Name']
        instructorName = data['flight']['Instructor']
        flightDate = data['flight']['Flight Date']
        flightLength = data['flight']['Flight Length']
        flightInstructions = data['flight']['Flight Instructions']
        xCoord = data['flight']['x-Coordinates']
        yCoord = data['flight']['y-Coordinates']
        zCoord = data['flight']['z-Coordinates']
        velPoints = data['flight']['Velocity Values']
    '''
    print(pilotName)
    print(instructorName)
    print(flightDate)
    print(flightLength)
    print(flightInstructions)
    print(xCoord)
    print(yCoord)
    print(zCoord)
    print(velPoints)
    '''

    return pilotName, instructorName, flightDate, flightLength, flightInstructions, xCoord, yCoord, zCoord, velPoints

#importData('ExportedFiles/Claire Eckert.flight')