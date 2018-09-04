import unittest

import numpy as np
from numpy.linalg import norm
from numpy.random import rand

from vmc.data.generator import *
from vmc.data.datasets import *
from vmc.utils import bin


class TestFixedPauli(unittest.TestCase):

    def setUp(self):
        self.state = rand(16) + 1.j * rand(16)
        self.state = self.state / norm(self.state)
        self.data = FixedPauli(
            root='.', state=self.state, itr=1000, nbasis=10, size=(4, ))

    def test_generate(self):
        syn_dis = np.zeros(16)
        for i in range(len(self.data)):
            config, basis = self.data[i]
            syn_dis[bin(config)] += 1
        syn_dis = [each / sum(syn_dis) for each in syn_dis]
        self.assertLess(norm(self.state * self.state.conj() - syn_dis), 0.05)


if __name__ == '__main__':
    unittest.main()
