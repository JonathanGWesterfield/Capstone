import unittest
import Views.Graph as Graph
import math
from Export.ImportFile import importData

class Graph_Test(unittest.TestCase):
    """
    This class is for testing the graphing functions that we are using to display the flight path
    onto the UI. We want to make sure that what is being displayed is correct.
    """

    def test_computeVelocity(self) -> None:
        """
        Test that the velocity is computed as expected between two points (1,1,1) and (3,3,1) with timeDiff = 1.

        :return: None
        """
        velocity = Graph.computeVelocity(1,1,1,3,3,1,1,2)
        self.assertEqual(velocity, math.sqrt(8))

    def test_checkLegalInput(self) -> None:
        """
        Test that legal and illegal coordinate points can be detected.

        :return: None
        """
        # Check normal point. Expected output: True.
        self.assertTrue(Graph.checkLegalInput(10.5, 5.5, 3.4))

        # Check when coordinate values are same. Expected output: True.
        self.assertTrue(Graph.checkLegalInput(1, 1, 1))

        # Check when x is negative. Expected output: False.
        self.assertFalse(Graph.checkLegalInput(-1, 4, 9))

        # Check when y is negative. Expected output: False.
        self.assertFalse(Graph.checkLegalInput(1, -4, 2.5))

        # Check when z is negative. Expected output: False.
        self.assertFalse(Graph.checkLegalInput(25, 12, -0.1))

        # Check smallest legal bound. Expected output: True.
        self.assertTrue(Graph.checkLegalInput(0, 0, 0))

        # Check largest legal bound. Expected output: True.
        self.assertTrue(Graph.checkLegalInput(15, 15, 10))

        # Check when x is string input. Expected output: False.
        self.assertFalse(Graph.checkLegalInput('hi there', 5, 3))

        # Check when y is string input. Expected output: False.
        self.assertFalse(Graph.checkLegalInput('n', '\n', 3))

        # Check when z is string input. Expected output: False.
        self.assertFalse(Graph.checkLegalInput(3, 2, "howdy"))

    def test_readCoordinates_small_legal(self) -> None:
        """
        Test that coordinates from a small data file are read in correctly.

        :return: None
        """
        test_dict = importData('TestFiles/JSONDUMP.flight')
        self.assertEqual(test_dict["coords"], [[0, 0, 0, 0], [1, 0, 0, 1], [2, 0, 0, 3], [3, 0, 0, 8]])

    def test_readCoordinates_small_illegal(self) -> None:
        """
        Test that coordinates from a small data file are read in correctly.

        :return: None
        """
        test_dict = importData('TestFiles/JSONDUMP_with_illegal.flight')
        test_dict = Graph.checkCoordinates(test_dict)
        self.assertEqual(test_dict["coords"], [[0, 0, 0, 0], [1, -10, 15, 5], [2, 0, 0, 1], [3, 0, 0, 3], [4, 0, 0, 8]])
        self.assertEqual(test_dict["legalPoints"], [[0, 0, 0, 0], [2, 0, 0, 1], [3, 0, 0, 3], [4, 0, 0, 8]])

        test_dict = Graph.velocityPoints(test_dict)
        self.assertIsNotNone(Graph.generateGraph(test_dict, True, 0, test_dict["flightLength"]))

    def test_readCoordinates_size100_allLegal(self) -> None:
        """
        Test that file containing 100 (x,y,z) points is read in correctly.
        This test contains all legal inputs.
        Illegal coordinate points in file should not be included in "legalPoints" list in dictionary.

        :return: None
        """
        length = 100
        test_dict = importData('TestFiles/new_size100_legal100.flight')
        test_dict = Graph.checkCoordinates(test_dict)
        self.assertEqual(len(test_dict["coords"]), length)
        self.assertEqual(len(test_dict["legalPoints"]), length)

    def test_readCoordinates_size100_someLegal(self) -> None:
        """
        Test that file containing 100 (x,y,z) points is read in correctly.
        This test contains 80% legal inputs.
        Illegal coordinate points in file should not be included in "legalPoints" list in dictionary.

        :return: None
        """
        length = 100
        numLegal = length * 0.8
        test_dict = importData('TestFiles/new_size100_legal80.flight')
        test_dict = Graph.checkCoordinates(test_dict)
        self.assertEqual(len(test_dict["coords"]), length)
        self.assertEqual(len(test_dict["legalPoints"]), numLegal)

    def test_readCoordinates_size200_allLegal(self) -> None:
        """
        Test that file containing 200 (x,y,z) points is read in correctly. This contains all legal inputs.
        Illegal coordinate points in file should not be included in "legalPoints" list in dictionary.

        :return: None
        """
        length = 200
        test_dict = importData('TestFiles/new_size200_legal100.flight')
        test_dict = Graph.checkCoordinates(test_dict)
        self.assertEqual(len(test_dict["coords"]), length)
        self.assertEqual(len(test_dict["legalPoints"]), length)

    def test_readCoordinates_size200_someLegal(self) -> None:
        """
        Test that file containing 200 (x,y,z) points is read in correctly. This contains 80% legal inputs.
        Illegal coordinate points in file should not be included in "legalPoints" list in dictionary.

        :return: None
        """
        length = 200
        numLegal = length * 0.8
        test_dict = importData('TestFiles/new_size200_legal80.flight')
        test_dict = Graph.checkCoordinates(test_dict)
        self.assertEqual(len(test_dict["coords"]), length)
        self.assertEqual(len(test_dict["legalPoints"]), numLegal)

    def test_readCoordinates_size600_allLegal(self) -> None:
        """
        Test that file containing 600 (x,y,z) points is read in correctly. This contains all legal inputs.
        Illegal coordinate points in file should not be included in "legalPoints" list in dictionary.

        :return: None
        """
        length = 600
        test_dict = importData('TestFiles/new_size600_legal100.flight')
        test_dict = Graph.checkCoordinates(test_dict)
        self.assertEqual(len(test_dict["coords"]), length)
        self.assertEqual(len(test_dict["legalPoints"]), length)

    def test_readCoordinates_size600_someLegal(self) -> None:
        """
        Test that file containing 600 (x,y,z) points is read in correctly. This contains 80% legal inputs.
        Illegal coordinate points in file should not be included in "legalPoints" list in dictionary.

        :return: None
        """
        length = 600
        numLegal = length * 0.8
        test_dict = importData('TestFiles/new_size600_legal80.flight')
        test_dict = Graph.checkCoordinates(test_dict)
        self.assertEqual(len(test_dict["coords"]), length)
        self.assertEqual(len(test_dict["legalPoints"]), numLegal)

    def test_readCoordinates_size1200_allLegal(self) -> None:
        """
        Test that file containing 1200 (x,y,z) points is read in correctly. This contains all legal inputs.
        Illegal coordinate points in file should not be included in "legalPoints" list in dictionary.

        :return: None
        """
        length = 1200
        test_dict = importData('TestFiles/new_size1200_legal100.flight')
        test_dict = Graph.checkCoordinates(test_dict)
        self.assertEqual(len(test_dict["coords"]), length)
        self.assertEqual(len(test_dict["legalPoints"]), length)

    def test_readCoordinates_size1200_someLegal(self) -> None:
        """
        Test that file containing 1200 (x,y,z) points is read in correctly. This contains 80% legal inputs.
        Illegal coordinate points in file should not be included in "legalPoints" list in dictionary.

        :return: None
        """
        length = 1200
        numLegal = 961
        test_dict = importData('TestFiles/new_size1200_legal80.flight')
        test_dict = Graph.checkCoordinates(test_dict)
        self.assertEqual(len(test_dict["coords"]), length)
        self.assertEqual(len(test_dict["legalPoints"]), numLegal)

    def test_graphShows_noError(self) -> None:
        """
        Test that graph generates correctly with and with velocity changes shown
        for data set of 100, then 200, then 800, then 1200 data points.
        For each size, two tests are run. One test contains all legal inputs. Another test contains 80% legal inputs.
        Illegal coordinate points in file should not be included in "legalPoints" list in dictionary.

        :return: None
        """
        # Test small data sets
        test_dict = importData('TestFiles/new_size100_legal100.flight')
        test_dict = Graph.checkCoordinates(test_dict)
        test_dict = Graph.velocityPoints(test_dict)
        self.assertIsNotNone(Graph.generateGraph(test_dict, True, 0, test_dict["flightLength"]))
        self.assertIsNotNone(Graph.generateGraph(test_dict, False, 0, test_dict["flightLength"]))

        test_dict = importData('TestFiles/new_size100_legal80.flight')
        test_dict = Graph.checkCoordinates(test_dict)
        test_dict = Graph.velocityPoints(test_dict)
        self.assertIsNotNone(Graph.generateGraph(test_dict, True, 0, test_dict["flightLength"]))
        self.assertIsNotNone(Graph.generateGraph(test_dict, False, 0, test_dict["flightLength"]))

        test_dict = importData('TestFiles/new_size200_legal100.flight')
        test_dict = Graph.checkCoordinates(test_dict)
        test_dict = Graph.velocityPoints(test_dict)
        self.assertIsNotNone(Graph.generateGraph(test_dict, True, 0, test_dict["flightLength"]))
        self.assertIsNotNone(Graph.generateGraph(test_dict, False, 0, test_dict["flightLength"]))

        test_dict = importData('TestFiles/new_size200_legal80.flight')
        test_dict = Graph.checkCoordinates(test_dict)
        test_dict = Graph.velocityPoints(test_dict)
        self.assertIsNotNone(Graph.generateGraph(test_dict, True, 0, test_dict["flightLength"]))
        self.assertIsNotNone(Graph.generateGraph(test_dict, False, 0, test_dict["flightLength"]))

        test_dict = importData('TestFiles/new_size600_legal100.flight')
        test_dict = Graph.checkCoordinates(test_dict)
        test_dict = Graph.velocityPoints(test_dict)
        self.assertIsNotNone(Graph.generateGraph(test_dict, True, 0, test_dict["flightLength"]))
        self.assertIsNotNone(Graph.generateGraph(test_dict, False, 0, test_dict["flightLength"]))

        test_dict = importData('TestFiles/new_size600_legal80.flight')
        test_dict = Graph.checkCoordinates(test_dict)
        test_dict = Graph.velocityPoints(test_dict)
        self.assertIsNotNone(Graph.generateGraph(test_dict, True, 0, test_dict["flightLength"]))
        self.assertIsNotNone(Graph.generateGraph(test_dict, False, 0, test_dict["flightLength"]))

        test_dict = importData('TestFiles/new_size1200_legal100.flight')
        test_dict = Graph.checkCoordinates(test_dict)
        test_dict = Graph.velocityPoints(test_dict)
        self.assertIsNotNone(Graph.generateGraph(test_dict, True, 0, test_dict["flightLength"]))
        self.assertIsNotNone(Graph.generateGraph(test_dict, False, 0, test_dict["flightLength"]))

        test_dict = importData('TestFiles/new_size1200_legal80.flight')
        test_dict = Graph.checkCoordinates(test_dict)
        test_dict = Graph.velocityPoints(test_dict)
        self.assertIsNotNone(Graph.generateGraph(test_dict, True, 0, test_dict["flightLength"]))
        self.assertIsNotNone(Graph.generateGraph(test_dict, False, 0, test_dict["flightLength"]))

    def test_velocityPoints(self) -> None:
        """
        Test that velocity between consecutive points is computed as expected.

        :return: None
        """
        test_dict = {
        "pilotName": "Hayley",
        "instructorName": "Eckert",
        "flightInstr": "Bob",
        "flightDate": "11/03/2019",
        "flightLength": 3,
        "coords": [(0, 0, 0, 0), (1, 0, 0, 1), (2, 0, 0, 2), (3, 1, 1, 3)],
        "velocities": [],
        "avgVel": 0.0,
        "maxVel": 0.0,
        "minVel": 0.0,
        "smoothness": 0.0,
        "legalPoints": [(0, 0, 0, 0), (1, 0, 0, 1), (2, 0, 0, 2), (3, 1, 1, 3)]
        }
        velocityArray = [1, 1, math.sqrt(3)]
        test_dict = Graph.velocityPoints(test_dict)
        self.assertEqual(test_dict["velocities"], velocityArray)

    def test_velocityColors(self) -> None:
        """
        Test that the correct color is assigned to the graph segment between consecutive velocity values.

        :return: None
        """
        test_dict = {
            "pilotName": "Hayley",
            "instructorName": "Eckert",
            "flightInstr": "Bob",
            "flightDate": "11/03/2019",
            "flightLength": 3.5,
            "coords": [(0, 0, 0, 0), (1, 0, 0, 1), (2, 0, 0, 2), (3, 1, 1, 3), (3.5, 1, 1, 2.5)],
            "velocities": [],
            "avgVel": 0.0,
            "maxVel": 0.0,
            "minVel": 0.0,
            "smoothness": 0.0,
            "legalPoints": [(0, 0, 0, 0), (1, 0, 0, 1), (2, 0, 0, 2), (3, 1, 1, 3), (3.5, 1, 1, 2.5)]
        }
        test_dict = Graph.velocityPoints(test_dict)
        colors = Graph.velocityColors(test_dict)
        self.assertEqual(colors, ['g', 'g', 'g', 'r'])

    def test_velocityComputes_correctSize(self) -> None:
        """
        Test that velocityPoints returns array of correct size when inputted data set of 100, 200, then 800,
        then 1200 data points. For each size, two tests are run.
        One test contains all legal inputs. Another test contains 80% legal inputs.
        Illegal coordinate points in file should not be included in "legalPoints" list in dictionary.

        :return: None
        """
        # Test small data sets
        size = 100
        test_dict = importData('TestFiles/new_size100_legal100.flight')
        test_dict = Graph.checkCoordinates(test_dict)
        test_dict = Graph.velocityPoints(test_dict)
        self.assertEqual(len(test_dict["velocities"]), size-1)

        test_dict = importData('TestFiles/new_size100_legal80.flight')
        test_dict = Graph.checkCoordinates(test_dict)
        test_dict = Graph.velocityPoints(test_dict)
        self.assertEqual(len(test_dict["velocities"]), 0.8*size-1)

        size = 200
        test_dict = importData('TestFiles/new_size200_legal100.flight')
        test_dict = Graph.checkCoordinates(test_dict)
        test_dict = Graph.velocityPoints(test_dict)
        self.assertEqual(len(test_dict["velocities"]), size-1)

        test_dict = importData('TestFiles/new_size200_legal80.flight')
        test_dict = Graph.checkCoordinates(test_dict)
        test_dict = Graph.velocityPoints(test_dict)
        self.assertEqual(len(test_dict["velocities"]), 0.8*size-1)

        # Test medium data sets
        size = 600
        test_dict = importData('TestFiles/new_size600_legal100.flight')
        test_dict = Graph.checkCoordinates(test_dict)
        test_dict = Graph.velocityPoints(test_dict)
        self.assertEqual(len(test_dict["velocities"]), size - 1)

        test_dict = importData('TestFiles/new_size600_legal80.flight')
        test_dict = Graph.checkCoordinates(test_dict)
        test_dict = Graph.velocityPoints(test_dict)
        self.assertEqual(len(test_dict["velocities"]), 0.8 * size - 1)

        # Test largest data sets
        size = 1200
        test_dict = importData('TestFiles/new_size1200_legal100.flight')
        test_dict = Graph.checkCoordinates(test_dict)
        test_dict = Graph.velocityPoints(test_dict)
        self.assertEqual(len(test_dict["velocities"]), size - 1)

        test_dict = importData('TestFiles/new_size1200_legal80.flight')
        test_dict = Graph.checkCoordinates(test_dict)
        test_dict = Graph.velocityPoints(test_dict)
        self.assertEqual(len(test_dict["velocities"]), 0.8 * size)

    def test_velocityColorsComputes_correctSize(self) -> None:
        """
        Test that velocityColors returns array of correct size when inputted data set of 100, then 200, then 800,
        then 1200 data points. For each size, two tests are run.
        One test contains all legal inputs. Another test contains 80% legal inputs.
        Illegal coordinate points in file should not be included in "legalPoints" list in dictionary.

        :return: None
        """

        # Test small data sets
        size = 100
        test_dict = importData('TestFiles/new_size100_legal100.flight')
        test_dict = Graph.checkCoordinates(test_dict)
        test_dict = Graph.velocityPoints(test_dict)
        self.assertEqual(len(Graph.velocityColors(test_dict)), size - 1)

        test_dict = importData('TestFiles/new_size100_legal80.flight')
        test_dict = Graph.checkCoordinates(test_dict)
        test_dict = Graph.velocityPoints(test_dict)
        self.assertEqual(len(Graph.velocityColors(test_dict)), 0.8*size - 1)

        size = 200
        test_dict = importData('TestFiles/new_size200_legal100.flight')
        test_dict = Graph.checkCoordinates(test_dict)
        test_dict = Graph.velocityPoints(test_dict)
        self.assertEqual(len(Graph.velocityColors(test_dict)), size - 1)

        test_dict = importData('TestFiles/new_size200_legal80.flight')
        test_dict = Graph.checkCoordinates(test_dict)
        test_dict = Graph.velocityPoints(test_dict)
        self.assertEqual(len(Graph.velocityColors(test_dict)), 0.8 * size - 1)

        # Test medium data sets
        size = 600
        test_dict = importData('TestFiles/new_size600_legal100.flight')
        test_dict = Graph.checkCoordinates(test_dict)
        test_dict = Graph.velocityPoints(test_dict)
        self.assertEqual(len(Graph.velocityColors(test_dict)), size - 1)

        test_dict = importData('TestFiles/new_size600_legal80.flight')
        test_dict = Graph.checkCoordinates(test_dict)
        test_dict = Graph.velocityPoints(test_dict)
        self.assertEqual(len(Graph.velocityColors(test_dict)), 0.8 * size - 1)

        # Test large data sets
        size = 1200
        test_dict = importData('TestFiles/new_size1200_legal100.flight')
        test_dict = Graph.checkCoordinates(test_dict)
        test_dict = Graph.velocityPoints(test_dict)
        self.assertEqual(len(Graph.velocityColors(test_dict)), size - 1)

        test_dict = importData('TestFiles/new_size1200_legal80.flight')
        test_dict = Graph.checkCoordinates(test_dict)
        test_dict = Graph.velocityPoints(test_dict)
        self.assertEqual(len(Graph.velocityColors(test_dict)), 0.8 * size)

    def test_smoothnessValues(self) -> None:
        """
        Test that smoothness function returns expected number.

        :return: None
        """
        size = 100
        test_dict = importData('TestFiles/new_size100_legal100.flight')
        test_dict = Graph.checkCoordinates(test_dict)
        test_dict = Graph.velocityPoints(test_dict)
        smoothness = Graph.log_dimensionless_jerk(test_dict["velocities"], 0.5)
        self.assertEqual(round(smoothness, 2), -17)

        test_dict = importData('TestFiles/new_size100_legal80.flight')
        test_dict = Graph.checkCoordinates(test_dict)
        test_dict = Graph.velocityPoints(test_dict)
        smoothness = Graph.log_dimensionless_jerk(test_dict["velocities"], 0.5)
        self.assertEqual(round(smoothness, 2), -16.24)

    def test_smoothnessComputes(self) -> None:
        """
        Test that smoothness function returns a number when inputted data set of 100, then 200, then 800,
        then 1200 data points. For each size, two tests are run.
        One test contains all legal inputs. Another test contains 80% legal inputs.
        Illegal coordinate points in file should not be included in "legalPoints" list in dictionary.

        :return: None
        """
        size = 100
        test_dict = importData('TestFiles/new_size100_legal100.flight')
        test_dict = Graph.checkCoordinates(test_dict)
        test_dict = Graph.velocityPoints(test_dict)
        self.assertIsNotNone(Graph.log_dimensionless_jerk(test_dict["velocities"], 0.5))

        test_dict = importData('TestFiles/new_size100_legal80.flight')
        test_dict = Graph.checkCoordinates(test_dict)
        test_dict = Graph.velocityPoints(test_dict)
        self.assertIsNotNone(Graph.log_dimensionless_jerk(test_dict["velocities"], 0.5))

        # Test small data sets
        size = 100
        test_dict = importData('TestFiles/new_size100_legal100.flight')
        test_dict = Graph.checkCoordinates(test_dict)
        test_dict = Graph.velocityPoints(test_dict)
        self.assertIsNotNone(Graph.log_dimensionless_jerk(test_dict["velocities"], 0.5))

        test_dict = importData('TestFiles/new_size100_legal80.flight')
        test_dict = Graph.checkCoordinates(test_dict)
        test_dict = Graph.velocityPoints(test_dict)
        self.assertIsNotNone(Graph.log_dimensionless_jerk(test_dict["velocities"], 0.5))

        size = 200
        test_dict = importData('TestFiles/new_size200_legal100.flight')
        test_dict = Graph.checkCoordinates(test_dict)
        test_dict = Graph.velocityPoints(test_dict)
        self.assertIsNotNone(Graph.log_dimensionless_jerk(test_dict["velocities"], 0.5))

        test_dict = importData('TestFiles/new_size200_legal80.flight')
        test_dict = Graph.checkCoordinates(test_dict)
        test_dict = Graph.velocityPoints(test_dict)
        self.assertIsNotNone(Graph.log_dimensionless_jerk(test_dict["velocities"], 0.5))

        # Test medium data sets
        size = 600
        test_dict = importData('TestFiles/new_size600_legal100.flight')
        test_dict = Graph.checkCoordinates(test_dict)
        test_dict = Graph.velocityPoints(test_dict)
        self.assertIsNotNone(Graph.log_dimensionless_jerk(test_dict["velocities"], 0.5))

        test_dict = importData('TestFiles/new_size600_legal80.flight')
        test_dict = Graph.checkCoordinates(test_dict)
        test_dict = Graph.velocityPoints(test_dict)
        self.assertIsNotNone(Graph.log_dimensionless_jerk(test_dict["velocities"], 0.5))

        # Test large data sets
        size = 1200
        test_dict = importData('TestFiles/new_size1200_legal100.flight')
        test_dict = Graph.checkCoordinates(test_dict)
        test_dict = Graph.velocityPoints(test_dict)
        self.assertIsNotNone(Graph.log_dimensionless_jerk(test_dict["velocities"], 0.5))

        test_dict = importData('TestFiles/new_size1200_legal80.flight')
        test_dict = Graph.checkCoordinates(test_dict)
        test_dict = Graph.velocityPoints(test_dict)
        self.assertIsNotNone(Graph.log_dimensionless_jerk(test_dict["velocities"], 0.5))

if __name__ == '__main__':
    unittest.main()