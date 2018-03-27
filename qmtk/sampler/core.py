import numpy as np
from sys import float_info
from numpy.random import rand
from functools import wraps

from qmtk.space import SpaceBase
from qmtk.utils.preprocess import typecheck


__all__ = ['metropolis', 'reject', 'direct']


class SamplerBase(object):
    """sampler base.
    """

    @typecheck(None, SpaceBase, int)
    def __init__(self, space, itr):
        super(SamplerBase, self).__init__()
        # type check for space in base class
        self.space = space
        self.itr = itr
        self.curr_itr = 0
        self.curr_s = None
        self.data = []

    def step(self):
        raise NotImplementedError

    def collect(self):
        raise NotImplementedError

    def __call__(self, func):
        raise NotImplementedError

    def sample(self):
        raise NotImplementedError


class reject(SamplerBase):
    """reject sampling
    """

    def __init__(self, space, n, itr=None):
        itr = 10 * n if itr is None else itr
        super(reject, self).__init__(space, itr)
        self.n = n

    def step(self):
        x = self.space.roll()
        bound = self.func(x)

        if rand() < bound:
            self.curr_s = self.space.copy()
            self.data.append(self.curr_s)

    def sample(self):
        for _curr_itr in range(self.itr):
            self.step()
            self.curr_itr += 1

            if len(self.data) == self.n:
                break
        return self.data

    def __call__(self, func):
        self.func = func

        @wraps(func)
        def wrapper(*args, **kwargs):
            return self.sample()
        return wrapper


class direct(SamplerBase):
    """simple direct sampling
    """

    def __init__(self, space, itr):
        super(direct, self).__init__(space, itr)

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(rand())
        return wrapper


class metropolis(SamplerBase):
    def __init__(self, space, itr=1000, burn=None, thin=1):
        super(metropolis, self).__init__(space, itr)
        if burn is None:
            self.burn = 200 * int(np.log(itr))
        else:
            self.burn = burn

        if thin is None:
            self.thin = 1
        else:
            self.thin = thin

        self.curr_p = None

    def step(self):
        cand_s = self.space.roll()
        cand_p = self.func(cand_s)

        if self.curr_p > 1000 * float_info.min:
            accept = min(1.0, cand_p / self.curr_p)
        else:
            accept = 1.0

        if rand() < accept:
            self.curr_s = self.space.copy()
            self.curr_p = cand_p

    def collect(self):
        if not self.curr_itr % self.thin:
            self.data.append(self.curr_s)

    def __call__(self, func):
        self.func = func
        self.space.roll()
        self.curr_s = self.space.copy()
        self.data.append(self.curr_s)
        self.curr_p = func(self.curr_s)

        @wraps(func)
        def wrapper(*args, **kwargs):
            return self.sample()
        return wrapper

    def sample(self):
        for _burn_itr in range(self.burn):
            self.step()

        for _curr_itr in range(self.itr):
            self.step()
            self.collect()
            self.curr_itr += 1
        return self.data
