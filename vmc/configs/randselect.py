from .base import GeneratorBase
from numpy.random import randint


class RandomSelect(GeneratorBase):
    """randomly select one to flip"""

    def __init__(self, **kwargs):
        super(RandomSelect, self).__init__('randselect', params=kwargs)

    def propose(self, data, nflips=1):
        cand = data.clone()
        if nflips == 1:
            ind = tuple(randint(0, each_size) for each_size in data.size())
            cand[ind] *= -1
        else:
            inds = []
            count = 0
            while count != nflips:
                ind = tuple(randint(0, each_size) for each_size in data.size())
                if ind not in inds:
                    inds.append(ind)
                else:
                    count -= 1
                count += 1
            for ind in inds:
                cand[ind] *= -1
        return cand
