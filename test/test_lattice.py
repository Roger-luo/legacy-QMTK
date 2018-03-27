import unittest
from qmtk.lattice import *


class TestLattice(unittest.TestCase):

    def setUp(self):
        self.chain = Chain(length=5)
        self.square = Square(shape=(5, 5))

    def test_chain(self):
        for i, each in enumerate(self.chain.sites()):
            self.assertEqual(i, each)

        self.chain.shape = 100
        self.assertEqual(self.chain.shape, (100, ))
        self.assertEqual(self.chain.numel(), 100)

        for k in range(5):
            for i, j in self.chain.bonds(k):
                self.assertEqual(i, j - k)

    def test_square(self):
        self.assertEqual(self.square.shape, (5, 5))


if __name__ == '__main__':
    unittest.main()
