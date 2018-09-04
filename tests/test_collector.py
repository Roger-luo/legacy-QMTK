import unittest
import torch
from torch.autograd import Variable
from numpy.random import rand

from vmc.collector import *


class TestCollector(unittest.TestCase):
    """test collector"""

    def test_collection(self):
        collector = STCollector(merge=True, accept=True)
        for i in range(1000):
            config = 2 * torch.LongTensor(2, 2).random_(0, to=2) - 1
            collector.collect(sample=config, accept=rand())
        self.assertEqual(len(collector), 1000)

        with self.assertRaises(TypeError):
            STCollector(params=Variable(torch.rand(2, 2)))
            STCollector(params=torch.rand(2, 2))


if __name__ == '__main__':
    unittest.main()
