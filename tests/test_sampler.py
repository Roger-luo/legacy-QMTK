import unittest
import torch
import numpy as np
from vmc import sampler as spl
from vmc import configs
from vmc import utils
from vmc.collector import STCollector


class TestSampler(unittest.TestCase):

    def setUp(self):
        self.size = (2, 2)
        self.itr = 10000
        self.burn = 500
        self.thin = 1

    def _proposal(self, x):
        return torch.sum(x) ** 2

    def _test_sampler(self, sampler):
        sampler.sample(itr=10000, burn=500, thin=1, inverse=0.4)
        sample_p = np.zeros(2 ** 4)
        exact_p = np.zeros(2 ** 4)
        for each_sample in sampler.collector:
            sample_p[utils.bin(each_sample)] += 1.0
        sample_p = sample_p / sum(sample_p)
        for i, each in enumerate(configs.IterateAll(size=self.size)):
            exact_p[i] = self._proposal(each)
        exact_p = exact_p / sum(exact_p)
        self.assertLess(np.linalg.norm(sample_p - exact_p), 0.05)

    def _test_collector(self, collector):

        sampler = spl.STMetropolis(self._proposal, size=self.size,
                                   generator='randselect',
                                   collector=collector)
        self._test_sampler(sampler, self.size)

    def test_samplers(self):
        # default collector
        print('testing single thread collector')
        collector = STCollector(merge=False, accept=True)
        sampler = spl.STMetropolis(self._proposal, size=self.size,
                                   generator='randselect', collector=collector)
        self._test_sampler(sampler)
        print('test single thread collector (merged)')
        collector = STCollector(merge=True, accept=True)
        sampler = spl.STMetropolis(self._proposal, size=self.size,
                                   generator='randselect', collector=collector)
        self._test_sampler(sampler)

    def test_directsample(self):
        print('testing direct sampler')
        dis = np.random.rand(16)
        dis = dis / np.linalg.norm(dis, ord=1)
        sampler = spl.PseudoRandom(dis, (4, ))
        syn_dis = np.zeros(16)
        for each in sampler.sample(itr=1000):
            syn_dis[utils.bin(each)] += 1
        syn_dis = syn_dis / np.linalg.norm(syn_dis, ord=1)
        self.assertLess(np.linalg.norm(syn_dis - dis), 0.05)

        state = np.random.rand(16) + 1.j * np.random.rand(16)
        dis = state * state.conj()
        dis = dis / np.linalg.norm(dis, ord=1)
        sampler = spl.PseudoRandom(dis, (4, ))
        syn_dis = np.zeros(16)
        for each in sampler.sample(itr=1000):
            syn_dis[utils.bin(each)] += 1
        syn_dis = syn_dis / np.linalg.norm(syn_dis, ord=1)
        self.assertLess(np.linalg.norm(syn_dis - dis), 0.05)


if __name__ == '__main__':
    unittest.main()
