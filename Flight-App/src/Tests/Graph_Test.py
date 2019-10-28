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

if __name__ == '__main__':
    unittest.main()