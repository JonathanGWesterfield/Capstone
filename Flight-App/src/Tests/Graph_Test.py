import unittest
import math
import src.Views.Graph as Graph

class Graph_Test(unittest.TestCase):

    def test_computeVelocity(self):
        velocity = Graph.computeVelocity(1,1,1,3,3,1,1,2)
        self.assertEqual(velocity, math.sqrt(8))

    def test_checkLegalInput(self):
        # Check normal point
        self.assertTrue(Graph.checkLegalInput(10.5, 5.5, 3.4))

        # Check when coordinate values are same
        self.assertTrue(Graph.checkLegalInput(1, 1, 1))

        # Check when x is negative
        self.assertFalse(Graph.checkLegalInput(-1, 4, 9))

        # Check when y is negative
        self.assertFalse(Graph.checkLegalInput(1, -4, 2.5))

        # Check when z is negative
        self.assertFalse(Graph.checkLegalInput(25, 12, -0.1))

        # Check smallest legal bound
        self.assertTrue(Graph.checkLegalInput(0, 0, 0))

        # Check largest legal bound
        self.assertTrue(Graph.checkLegalInput(30, 15, 10))

        # Check not a number
        self.assertFalse(Graph.checkLegalInput("\n", 5, 3))


    def test_readCoordinates(self):
        x, y, z = Graph.readCoordinates('TestFiles/coordinates_tiny.rtf')
        self.assertEqual(x, [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 3.0, 1.0])
        self.assertEqual(y, [0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 4.0, 6.0, 3.0])
        self.assertEqual(z, [0.0, 1.0, 3.0, 8.0, 10.0, 10.0, 10.0, 9.0, 8.0])

    def test_velocityPoints(self):
        x = [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 3.0, 1.0]
        y = [0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 4.0, 6.0, 3.0]
        z = [0.0, 1.0, 3.0, 8.0, 10.0, 10.0, 10.0, 9.0, 8.0]
        velocityArray = [1, 2, 5, 2, math.sqrt(5), 2, math.sqrt(9), math.sqrt(14)]
        self.assertEqual(Graph.velocityPoints(x,y,z), velocityArray)

    def test_velocityColors(self):
        x = [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 3.0, 1.0]
        y = [0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 4.0, 6.0, 3.0]
        z = [0.0, 1.0, 3.0, 8.0, 10.0, 10.0, 10.0, 9.0, 8.0]
        vel = Graph.velocityPoints(x,y,z)
        self.assertEqual(Graph.velocityColors(vel), ['g', 'g', 'g', 'r','y','r','g','g'])

if __name__ == '__main__':
    unittest.main()