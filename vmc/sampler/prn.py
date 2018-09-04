import torch

from .base import SamplerBase
from numpy.random import rand
from vmc.utils import shift


class PseudoRandom(SamplerBase):
    """pseudo random sampling"""

    def __init__(self, p_vec, size,
                 generator='randselect',
                 collector='std'):
        l1 = sum(p_vec)
        p_vec = [each / l1 for each in p_vec]
        self.stride = [sum(p_vec[0:k]) for k in range(len(p_vec))]
        super(PseudoRandom, self).__init__(
            p_vec, size, generator, collector)

    def step(self):
        dice = rand()
        sample = torch.zeros(*self.size) - 1
        for i, each in enumerate(self.stride[1:]):
            if dice < each:
                break
            else:
                shift(sample)
        return sample

    def sample(self, itr):
        _curr_itr = 0
        while _curr_itr < itr:
            _curr_itr += 1
            sample = self.step()
            self.collector.collect_sample(sample)
        return self.collector
