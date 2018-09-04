import unittest
from vmc.lattice import *


class TestLattice(unittest.TestCase):

    def test_shape_assertions(self):
        name = 'test lattice'
        with self.assertRaises(TypeError):
            LatticeBase(name, (2, 3))

        with self.assertRaises(TypeError):
            LatticeBase(name, length=(2, ))

        with self.assertRaises(TypeError):
            LatticeBase(name, shape="2, 2")

        with self.assertRaises(TypeError):
            LatticeBase(name)

    def test_pbc_assertions(self):
        name = 'test lattice'
        shape = (2, 3)
        with self.assertRaises(TypeError):
            LatticeBase(name, shape=shape, pbc=1)


if __name__ == '__main__':
    unittest.main()
