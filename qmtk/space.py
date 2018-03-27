import numpy as np
import qmtk._space as _space
from itertools import product
from numpy.random import randint, rand


class SpaceBase(object):
    """sample space"""

    def __init__(self):
        self.history = None

    def roll(self):
        """this method defined how will you roll
        the dice.
        """
        raise NotImplementedError

    def __call__(self):
        return self.roll()

    def copy(self):
        return self.history


class real(SpaceBase):
    """sample range in real space.
    """

    def __init__(self, min, max, shape=()):
        super(real, self).__init__()
        self.min = min
        self.max = max
        self.shape = shape

    def roll(self):
        self.history = (self.max - self.min) * rand(*self.shape) + self.min
        return self.history


class discrete(SpaceBase):

    def __init__(self, min, max, shape=None):
        super(discrete, self).__init__()
        self.min = min
        self.max = max
        self.shape = shape

    def __iter__(self):
        if self.shape is None:
            return iter(range(self.min, self.max))
        else:
            n = np.prod(self.shape)
            iters = tuple(range(self.min, self.max) for i in range(n))
            for r in product(*iters):
                yield np.array(r).reshape(self.shape)

    def roll(self):
        self.history = randint(self.min, high=self.max, size=self.shape)
        return self.history


class spin(SpaceBase, _space.Spin):
    """sample space for spin lattice.

    Args:
        shape (tuple):
        state (tuple)
    """

    def __init__(self, shape,
                 state=(0, 1), nflips=1, p=0.5,
                 max_flips=10000):
        SpaceBase.__init__(self)
        _space.Spin.__init__(
            self, shape,
            state[0], state[1], nflips, p)
        self.max_flips = max_flips

    def __repr__(self):
        msg = 'x'.join(str(each) for each in self.shape)
        msg += ' spin lattice:\n'
        msg += str(np.array(self, copy=False))
        return msg

    def roll(self):
        self.randflip(self.max_flips)
        return np.array(self, copy=False)

    def copy(self):
        return np.array(self)
