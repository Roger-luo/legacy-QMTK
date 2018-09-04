from .base import SamplerBase
from vmc.utils import randspin
from numpy.random import rand
from sys import float_info
from tqdm import trange

import torch
from vmc.utils import shift


class STMetropolis(SamplerBase):
    """single thread metropolis"""

    def preload(self):
        self.state['last'] = randspin(self.size)
        self.state['prob'] = self.proposal(self.state['last'])
        # TODO: check proposal output shape

    def step(self, collect=True):
        if self.inverse is not None and rand() < self.inverse:
            self.state['last'] *= -1

        cand = self.generator.propose(self.state['last'])
        prob = self.proposal(cand)

        if self.state['prob'] > 1000 * float_info.min:
            accept = min(1.0, prob / self.state['last'])
        else:
            accept = 1.0

        if rand() < accept:
            self.state['last'] = cand
            self.state['prob'] = prob

        if self.state['itr'] % self.state['thin'] == 0:
            self.collector.collect_sample(
                self.state['last'], self.state['prob'])

    def preprocess(self, kwargs):
        if 'burn' in kwargs:
            burn = kwargs.pop('burn')
        else:
            raise ValueError('burn iteration length needed')

        if 'thin' in kwargs:
            self.state['thin'] = kwargs.pop('thin')
        else:
            self.state['thin'] = 1

        print('preprocessing: start burning')
        for _burn_itr in trange(burn, desc='burning:', position=self.id):
            self.step(collect=False)


class STDirect(SamplerBase):
    """single thread direct sampling"""

    def preload(self):
        l1 = sum(self.proposal)
        self.proposal = [each / l1 for each in self.proposal]
        self.stride = [sum(self.proposal[0:k])
                       for k in range(len(self.proposal))]

    def step(self):
        dice = rand()
        sample = torch.zeros(*self.size) - 1
        for each in self.stride[1:]:
            if dice < each:
                break
            else:
                shift(sample)

        self.collector.collect_sample(sample)
