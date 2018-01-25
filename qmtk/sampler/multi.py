import multiprocessing as mp
from sampler import sample
from functools import wraps


class multi(object):
    """multi-process sampling
    """

    def __init__(self, sampler, *args, **kwargs):
        super(multi, self).__init__()
        self.processes = kwargs.pop('processes', 4)
        self.sampler = [sample(sampler, *args, **kwargs)
                        for i in range(self.processes)]
        self.args = args
        self.kwargs = kwargs
        self.manager = mp.Manager()
        self.data = self.manager.dict()

    def spawn(self, func):
        self.pool = []

        def worker(sampler, procnum, data):
            data[procnum] = sampler()

        for i, each in enumerate(self.sampler):
            p = mp.Process(target=worker, args=(each(func), i, self.data))
            p.start()
            self.pool.append(p)

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self.spawn(func)
            for procs in self.pool:
                procs.join()
            samples = []
            for each in self.data.values():
                samples.extend(each)
            return samples
        return wrapper


class metropolis(multi):
    """multi process metropolis hasting
    """

    def __init__(self, *args, **kwargs):
        super(metropolis, self).__init__(
            'metropolis', *args, **kwargs)


class direct(multi):
    """multi process direct sampling
    """

    def __init__(self, *args, **kwargs):
        super(direct, self).__init__(
            'direct', *args, **kwargs)


class reject(multi):
    """multi process reject sampling
    """

    def __init__(self, *args, **kwargs):
        super(reject, self).__init__(
            'reject', *args, **kwargs)
