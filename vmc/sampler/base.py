from tqdm import trange
from vmc.configs import Generator
from vmc.collector import Collector
from multiprocessing import current_process


class SamplerBase(object):
    """sampler base"""

    def __init__(self, proposal, size,
                 generator='randselect', collector='std',
                 bar=True, id=None):
        super(SamplerBase, self).__init__()
        if id is not None:
            self.id = id
        else:
            id = current_process()._identity
            if id:
                self.id, = current_process()._identity
            else:
                self.id = 0

        self.proposal = proposal
        self.size = size
        self.generator = Generator(generator)
        self.collector = Collector(collector)
        self.state = dict(itr=0, collect=False, bar=bar)
        self.inverse = None
        self.preload()

    def preload(self):
        pass

    def step(self):
        raise NotImplementedError

    def preprocess(self, kwargs):
        pass

    def sample(self, itr, **kwargs):
        if 'desc' in kwargs:
            desc = kwargs.pop('desc')
        else:
            desc = 'sampling'

        self.preprocess(kwargs)
        if self.state['bar']:
            itr_range = trange(itr, desc=desc, position=self.id)
        else:
            itr_range = range(itr)
        for _curr_itr in itr_range:
            self.step()
            self.state['itr'] += 1
        return self.collector
