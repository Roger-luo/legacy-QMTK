import unittest
import torch
from vmc.configs import *
from vmc import utils


class TestRandSelect(unittest.TestCase):
    def test_nflips(self):
        config = torch.LongTensor(5, 5)
        config = 2 * config.random_(0, to=2) - 1
        gen = RandomSelect()
        for n in range(10):
            cand = gen.propose(config, nflips=n)
            self.assertEqual(torch.sum(cand != config), n)


class TestIterateAll(unittest.TestCase):
    def test_propose(self):
        config = torch.zeros(5, 5, out=torch.LongTensor())
        config = config - 1
        gen = IterateAll()
        for i in range(1000):
            self.assertEqual(i, utils.bin(config))
            config = gen.propose(config)

    def test_iteration(self):
        gen = IterateAll(size=(2, 2))
        for i, cfg in enumerate(gen):
            self.assertEqual(i, utils.bin(cfg))


if __name__ == '__main__':
    unittest.main()
