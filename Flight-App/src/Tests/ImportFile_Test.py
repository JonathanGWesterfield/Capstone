import unittest
import Export.ImportFile

class ImportFileTests(unittest.TestCase):
    def test_import(self):
        """
        Test that .flight file generated from exporting flight data can be imported successfully.
        All data members should exist, and no extra keys should be in the file.
        :return: None
        """
        flightDict = Export.ImportFile.importData('../Export/ExportedFiles/Hayley.flight')
        self.assertIsNotNone(flightDict)
        self.assertEqual(len(flightDict), 12)
        self.assertEqual(flightDict["pilotName"], "Hayley")
        self.assertEqual(flightDict["instructorName"], "Billy")
        self.assertEqual(flightDict["flightDate"], "11/03/2019")
        self.assertEqual(flightDict["flightLength"], "00:00:00")
        self.assertEqual(flightDict["flightInstr"], "Figure 8 please!")
        self.assertEqual(flightDict["coords"], [[0, 0, 0, 0], [1, -10, 15, 5], [2, 0, 0, 1], [3, 0, 0, 3], [4, 0, 0, 8]])
        self.assertEqual(flightDict["velocities"], [0.5, 2.0, 5.0])
        self.assertEqual(flightDict["avgVel"], 2.5)
        self.assertEqual(flightDict["minVel"], 0.5)
        self.assertEqual(flightDict["maxVel"], 5.0)
        self.assertEqual(flightDict["legalPoints"], [[0, 0, 0, 0], [2, 0, 0, 1], [3, 0, 0, 3], [4, 0, 0, 8]])
        self.assertEqual(flightDict["smoothness"], 0.0)

if __name__ == '__main__':
    unittest.main()
