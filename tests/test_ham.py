"""
test hamiltonians

TODO:
    multi-threading tests, it is quite slow currently.
    solution can be adding test suites and multiprocessing package
"""


import unittest
from vmc.ham import *
from vmc.lattice import Chain, Square
from vmc import utils
from vmc.sampler import STMetropolis
import testutils


class TestHam(unittest.TestCase):

    def _test_energy(self, h):
        energy, state = utils.ed(h.mat())
        exact = energy[0]
        state = state[:, 0]

        def _fake_proposal(x):
            return abs(state[utils.bin(x)]) ** 2

        def _fake_ansatz(x):
            return state[utils.bin(x)]

        def _local_energy(x):
            ret = sum(val * _fake_ansatz(config) for config, val in h.nnz(x))
            return ret / _fake_ansatz(x)

        sampler = STMetropolis(_fake_proposal, h.size)
        collector = sampler.sample(itr=10000, burn=500, thin=1)
        energy = sum(_local_energy(config) for config in collector)
        energy /= len(collector)
        self.assertLess(abs(energy - exact), 0.05)

    def test_j1j2(self):
        for i in range(4, 10):
            lattice = Chain(i, pbc=True)
            interaction = (1, 0.5)
            test_h = J1J2(J=interaction, pbc=True, lattice=lattice)
            exact = testutils.J1J2(lattice, J=interaction)
            testutils.assertEqualSparse(self, test_h.mat(), exact)
            self._test_energy(test_h)

        for x in range(2, 4):
            for y in range(2, 4):
                lattice = Square(x, y, pbc=True)
                test_h = J1J2(J=interaction, pbc=True, lattice=lattice)
                exact = testutils.J1J2(lattice)
                testutils.assertEqualSparse(self, test_h.mat(), exact)
                self._test_energy(test_h)

    def test_tfi(self):
        for i in range(4, 10):
            lattice = Chain(i, pbc=True)
            test_h = TFI(mag=1.0, pbc=True, lattice=lattice)
            exact = testutils.TFI(lattice, mag=1.0)
            testutils.assertEqualSparse(self, test_h.mat(), exact)

    def test_general_constructor(self):
        lattice = Chain(3, pbc=True)
        for name in __traits__.keys():
            h = Ham(name, lattice=lattice)
            self.assertIsInstance(h, __traits__[name])


if __name__ == '__main__':
    unittest.main()
