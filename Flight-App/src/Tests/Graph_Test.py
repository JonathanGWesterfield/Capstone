import unittest
import Graph
import math

class Graph_Test(unittest.TestCase):

    def test_computeVelocity(self):
        """
        Test that the velocity is computed as expected between two points (1,1,1) and (3,3,1) with timeDiff = 1.
        :return: None
        """
        velocity = Graph.computeVelocity(1,1,1,3,3,1,1,2)
        self.assertEqual(velocity, math.sqrt(8))

    def test_checkLegalInput(self):
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
        self.assertTrue(Graph.checkLegalInput(30, 15, 10))

        # Check when x is string input. Expected output: False.
        self.assertFalse(Graph.checkLegalInput('hi there', 5, 3))

        # Check when y is string input. Expected output: False.
        self.assertFalse(Graph.checkLegalInput('n', '\n', 3))

        # Check when z is string input. Expected output: False.
        self.assertFalse(Graph.checkLegalInput(3, 2, "howdy"))

    def test_readCoordinates_small_legal(self):
        """
        Test that file containing one x, one y, and one z value in each row is read in correctly. File contains
        only legal input, so timearray should count from 0 to 8.
        :return: None
        """
        x, y, z, timearray = Graph.readCoordinates('TestFiles/coordinates_tiny.rtf', 1)
        self.assertEqual(x, [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 3.0, 1.0])
        self.assertEqual(y, [0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 4.0, 6.0, 3.0])
        self.assertEqual(z, [0.0, 1.0, 3.0, 8.0, 10.0, 10.0, 10.0, 9.0, 8.0])
        self.assertEqual(timearray, [0, 1, 2, 3, 4, 5, 6, 7, 8])

    def test_readCoordinates_small_illegal(self):
        """
        Test that file containing one x, one y, and one z value in each row is read in correctly. Illegal coordinate
        points in file should not be included in return result, and timearray should reflect this.
        :return: None
        """
        x, y, z, timearray = Graph.readCoordinates('TestFiles/coordinates_tiny_illegal.rtf', 1)
        self.assertEqual(x, [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 3.0, 1.0])
        self.assertEqual(y, [0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 4.0, 6.0, 3.0])
        self.assertEqual(z, [0.0, 1.0, 3.0, 8.0, 10.0, 10.0, 10.0, 9.0, 8.0])
        self.assertEqual(timearray, [0, 1, 2, 3, 5, 6, 7, 9, 11])

    def test_readCoordinates_size200(self):
        """
        Test that file containing 200 (x,y,z) points is read in correctly.
        One test contains all legal inputs. Another test contains 80% legal inputs.
        Illegal coordinate points in file should not be included in return result.
        :return: None
        """
        length = 200
        numLegal = 200 * 0.8
        x, y, z, timearray = Graph.readCoordinates('TestFiles/spiral_size200_legal100.txt', 1)
        self.assertEqual(len(x), length)
        self.assertEqual(len(y), length)
        self.assertEqual(len(z), length)
        self.assertEqual(len(timearray), length)

        x, y, z, timearray = Graph.readCoordinates('TestFiles/random_size200_legal80.txt', 1)
        self.assertEqual(len(x), numLegal)
        self.assertEqual(len(y), numLegal)
        self.assertEqual(len(z), numLegal)
        self.assertEqual(len(timearray), numLegal)

    def test_readCoordinates_size400(self):
        """
        Test that file containing 400 (x,y,z) points is read in correctly.
        One test contains all legal inputs. Another test contains 80% legal inputs.
        Illegal coordinate points in file should not be included in return result.
        :return: None
        """
        length = 400
        numLegal = length * 0.8
        x, y, z, timearray = Graph.readCoordinates('TestFiles/spiral_size400_legal100.txt', 1)
        self.assertEqual(len(x), length)
        self.assertEqual(len(y), length)
        self.assertEqual(len(z), length)
        self.assertEqual(len(timearray), length)

        x, y, z, timearray = Graph.readCoordinates('TestFiles/random_size400_legal80.txt', 1)
        self.assertEqual(len(x), numLegal)
        self.assertEqual(len(y), numLegal)
        self.assertEqual(len(z), numLegal)
        self.assertEqual(len(timearray), numLegal)

    def test_readCoordinates_size800(self):
        """
        Test that file containing 800 (x,y,z) points is read in correctly.
        One test contains all legal inputs. Another test contains 80% legal inputs.
        Illegal coordinate points in file should not be included in return result.
        :return: None
        """
        length = 800
        numLegal = length * 0.8
        x, y, z, timearray = Graph.readCoordinates('TestFiles/spiral_size800_legal100.txt', 1)
        self.assertEqual(len(x), length)
        self.assertEqual(len(y), length)
        self.assertEqual(len(z), length)
        self.assertEqual(len(timearray), length)

        x, y, z, timearray = Graph.readCoordinates('TestFiles/random_size800_legal80.txt', 1)
        self.assertEqual(len(x), numLegal)
        self.assertEqual(len(y), numLegal)
        self.assertEqual(len(z), numLegal)
        self.assertEqual(len(timearray), numLegal)

    def test_readCoordinates_size1000(self):
        """
        Test that file containing 1000 (x,y,z) points is read in correctly.
        One test contains all legal inputs. Another test contains 80% legal inputs.
        Illegal coordinate points in file should not be included in return result.
        :return: None
        """
        length = 1000
        numLegal = length * 0.8
        x, y, z, timearray = Graph.readCoordinates('TestFiles/spiral_size1000_legal100.txt', 1)
        self.assertEqual(len(x), length)
        self.assertEqual(len(y), length)
        self.assertEqual(len(z), length)
        self.assertEqual(len(timearray), length)

        x, y, z, timearray = Graph.readCoordinates('TestFiles/random_size1000_legal80.txt', 1)
        self.assertEqual(len(x), numLegal)
        self.assertEqual(len(y), numLegal)
        self.assertEqual(len(z), numLegal)
        self.assertEqual(len(timearray), numLegal)

    def test_readCoordinates_size1200(self):
        """
        Test that file containing 1200 (x,y,z) points is read in correctly.
        One test contains all legal inputs. Another test contains 80% legal inputs.
        Illegal coordinate points in file should not be included in return result.
        :return: None
        """
        length = 1200
        numLegal = length * 0.8
        x, y, z, timearray = Graph.readCoordinates('TestFiles/spiral_size1200_legal100.txt', 1)
        self.assertEqual(len(x), length)
        self.assertEqual(len(y), length)
        self.assertEqual(len(z), length)
        self.assertEqual(len(timearray), length)

        x, y, z, timearray = Graph.readCoordinates('TestFiles/random_size1200_legal80.txt', 1)
        self.assertEqual(len(x), numLegal)
        self.assertEqual(len(y), numLegal)
        self.assertEqual(len(z), numLegal)
        self.assertEqual(len(timearray), numLegal)

    def test_graphShows_noError(self):
        """
        Test that graph generates correctly for data set of 200, then 800, then 1200 data points.
        For each size, two tests are run. One test contains all legal inputs. Another test contains 80% legal inputs.
        Illegal coordinate points in file should not be included in return result.
        :return: None
        """

        # Test small data sets
        x, y, z, timearray = Graph.readCoordinates('TestFiles/spiral_size200_legal100.txt', 1)
        self.assertIsNotNone(Graph.generateGraph(x, y, z, timearray))

        x, y, z, timearray = Graph.readCoordinates('TestFiles/random_size200_legal80.txt', 1)
        self.assertIsNotNone(Graph.generateGraph(x, y, z, timearray))

        # Test medium data sets
        x, y, z, timearray = Graph.readCoordinates('TestFiles/spiral_size800_legal100.txt', 1)
        self.assertIsNotNone(Graph.generateGraph(x, y, z, timearray))

        x, y, z, timearray = Graph.readCoordinates('TestFiles/random_size800_legal80.txt', 1)
        self.assertIsNotNone(Graph.generateGraph(x, y, z, timearray))

        # Test largest data sets
        x, y, z, timearray = Graph.readCoordinates('TestFiles/spiral_size1200_legal100.txt', 1)
        self.assertIsNotNone(Graph.generateGraph(x, y, z, timearray))

        x, y, z, timearray = Graph.readCoordinates('TestFiles/random_size1200_legal80.txt', 1)
        self.assertIsNotNone(Graph.generateGraph(x, y, z, timearray))

    def test_velocityPoints(self):
        """
        Test that velocity between consecutive points is computed as expected.
        :return: None
        """
        x = [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 3.0, 1.0]
        y = [0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 4.0, 6.0, 3.0]
        z = [0.0, 1.0, 3.0, 8.0, 10.0, 10.0, 10.0, 9.0, 8.0]
        timearray = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        velocityArray = [1, 2, 5, 2, math.sqrt(5), 2, math.sqrt(9), math.sqrt(14)]
        self.assertEqual(Graph.velocityPoints(x,y,z,timearray), velocityArray)

    def test_velocityColors(self):
        """
        Test that the correct color is assigned to the graph segment between consecutive velocity values.
        :return: None
        """
        x = [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 3.0, 1.0]
        y = [0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 4.0, 6.0, 3.0]
        z = [0.0, 1.0, 3.0, 8.0, 10.0, 10.0, 10.0, 9.0, 8.0]
        timearray = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        vel = Graph.velocityPoints(x,y,z, timearray)
        self.assertEqual(Graph.velocityColors(vel), ['g', 'g', 'g', 'r','y','r','g','g'])

    def test_velocityComputes_correctSize(self):
        """
        Test that velocityPoints returns array of correct size when inputted data set of 200, then 800, then 1200 data points.
        For each size, two tests are run. One test contains all legal inputs. Another test contains 80% legal inputs.
        Illegal coordinate points in file should not be included in return result.
        :return: None
        """

        # Test small data sets
        size = 200
        x, y, z, timearray = Graph.readCoordinates('TestFiles/spiral_size200_legal100.txt', 1)
        self.assertEqual(len(Graph.velocityPoints(x, y, z, timearray)), size-1)

        x, y, z, timearray = Graph.readCoordinates('TestFiles/random_size200_legal80.txt', 1)
        self.assertEqual(len(Graph.velocityPoints(x, y, z, timearray)), (.8*size - 1))

        # Test medium data sets
        size = 800
        x, y, z, timearray = Graph.readCoordinates('TestFiles/spiral_size800_legal100.txt', 1)
        self.assertEqual(len(Graph.velocityPoints(x, y, z, timearray)), size-1)

        x, y, z, timearray = Graph.readCoordinates('TestFiles/random_size800_legal80.txt', 1)
        self.assertEqual(len(Graph.velocityPoints(x, y, z, timearray)), (.8*size - 1))

        # Test largest data sets
        size = 1200
        x, y, z, timearray = Graph.readCoordinates('TestFiles/spiral_size1200_legal100.txt', 1)
        self.assertEqual(len(Graph.velocityPoints(x, y, z, timearray)), size-1)

        x, y, z, timearray = Graph.readCoordinates('TestFiles/random_size1200_legal80.txt', 1)
        self.assertEqual(len(Graph.velocityPoints(x, y, z, timearray)), (.8*size - 1))

    def test_velocityColorsComputes_correctSize(self):
        """
        Test that velocityColors returns array of correct size when inputted data set of 200, then 800, then 1200 data points.
        For each size, two tests are run. One test contains all legal inputs. Another test contains 80% legal inputs.
        Illegal coordinate points in file should not be included in return result.
        :return: None
        """

        # Test small data sets
        size = 200
        x, y, z, timearray = Graph.readCoordinates('TestFiles/spiral_size200_legal100.txt', 1)
        self.assertEqual(len(Graph.velocityColors(Graph.velocityPoints(x, y, z, timearray))), size-1)

        x, y, z, timearray = Graph.readCoordinates('TestFiles/random_size200_legal80.txt', 1)
        self.assertEqual(len(Graph.velocityColors(Graph.velocityPoints(x, y, z, timearray))), (.8*size - 1))

        # Test medium data sets
        size = 800
        x, y, z, timearray = Graph.readCoordinates('TestFiles/spiral_size800_legal100.txt', 1)
        self.assertEqual(len(Graph.velocityColors(Graph.velocityPoints(x, y, z, timearray))), size-1)

        x, y, z, timearray = Graph.readCoordinates('TestFiles/random_size800_legal80.txt', 1)
        self.assertEqual(len(Graph.velocityColors(Graph.velocityPoints(x, y, z, timearray))), (.8*size - 1))

        # Test largest data sets
        size = 1200
        x, y, z, timearray = Graph.readCoordinates('TestFiles/spiral_size1200_legal100.txt', 1)
        self.assertEqual(len(Graph.velocityColors(Graph.velocityPoints(x, y, z, timearray))), size-1)

        x, y, z, timearray = Graph.readCoordinates('TestFiles/random_size1200_legal80.txt', 1)
        self.assertEqual(len(Graph.velocityColors(Graph.velocityPoints(x, y, z, timearray))), (.8*size - 1))

if __name__ == '__main__':
    unittest.main()