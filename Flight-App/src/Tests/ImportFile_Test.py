import unittest
import Export.ImportFile

class ImportFileTests(unittest.TestCase):
    def test_min(self):
        """
        Test that .flight file generated using data set of 10 legal coordinates can be imported successfully.
        :return: None
        """
        pilotName, instructorName, flightDate, flightLength, flightInstructions, xCoord, yCoord, zCoord, \
        velPoints = Export.ImportFile.importData('../Export/ExportedFiles/Claire Eckert.flight')
        self.assertEqual(pilotName, "Claire Eckert")
        self.assertEqual(instructorName, "ok!")
        self.assertEqual(flightDate, "11/02/2019")
        self.assertEqual(flightLength, "00:00:00")
        self.assertEqual(flightInstructions, "")
        self.assertEqual(xCoord, [
            15.0,
            15.0,
            15.0,
            15.0,
            15.0,
            16.0,
            16.0,
            18.0,
            16.0
        ])
        self.assertEqual(yCoord, [
            7.5,
            7.5,
            7.5,
            7.5,
            7.5,
            9.5,
            11.5,
            13.5,
            11.5
        ])
        self.assertEqual(zCoord, [
            0.0,
            1.0,
            3.0,
            8.0,
            10.0,
            10.0,
            10.0,
            9.0,
            8.0
        ])
        self.assertEqual(velPoints, [
            1.0,
            2.0,
            5.0,
            2.0,
            2.23606797749979,
            2.0,
            3.0,
            3.0
        ])

    def test_large(self):
        """
        Test that .flight file generated using data set of 200 legal coordinates can be imported successfully.
        :return: None
        """
        pilotName, instructorName, flightDate, flightLength, flightInstructions, xCoord, yCoord, zCoord, \
        velPoints = Export.ImportFile.importData('../Export/ExportedFiles/spiral_size200_legal100.flight')
        self.assertEqual(pilotName, "spiral_size200_legal100")
        self.assertEqual(instructorName, "Hayley")
        self.assertEqual(flightDate, "11/02/2019")
        self.assertEqual(flightLength, "00:00:00")
        self.assertEqual(flightInstructions, "Pls work x2")
        self.assertEqual(len(xCoord), 200)
        self.assertEqual(len(yCoord), 200)
        self.assertEqual(len(zCoord), 200)
        self.assertEqual(len(velPoints), 199)

    def test_max(self):
        """
        Test that .flight file generated using data set of 1200 coordinates with 80% legality can be imported successfully.
        :return: None
        """
        pilotName, instructorName, flightDate, flightLength, flightInstructions, xCoord, yCoord, zCoord, \
        velPoints = Export.ImportFile.importData('../Export/ExportedFiles/random_size1200_legal80.flight')
        self.assertEqual(pilotName, "random_size1200_legal80")
        self.assertEqual(instructorName, "Big boy test")
        self.assertEqual(flightDate, "11/02/2019")
        self.assertEqual(flightLength, "00:00:00")
        self.assertEqual(flightInstructions, "Here \nwe \ngo!")
        self.assertEqual(len(xCoord), 960)
        self.assertEqual(len(yCoord), 960)
        self.assertEqual(len(zCoord), 960)
        self.assertEqual(len(velPoints), 959)

if __name__ == '__main__':
    unittest.main()
