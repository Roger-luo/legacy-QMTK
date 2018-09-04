from .base import GeneratorBase
from numpy.random import randint


class SpinConserve(GeneratorBase):
    """spin conserve methods"""

    def __init__(self, **kwargs):
        super(SpinConserve, self).__init__('spin conserve', params=kwargs)

    def propose(self, data, nflips=2):
        cand = data.clone()
        inds = [tuple(randint(0, each_size) for each_size in data.size())
                for i in range(nflips)]
        for ind in inds:
            cand[ind] *= -1
            for i in range(1000):
                conserve_ind = tuple(randint(0, each_size)
                                     for each_size in data.size())
                if cand[conserve_ind] == cand[ind]:
                    break
            cand[conserve_ind] *= -1
        return cand
