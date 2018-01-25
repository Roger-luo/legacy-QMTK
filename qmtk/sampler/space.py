import numpy as np
from numpy.random import randint, rand


class SampleSpace(object):
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


class real(SampleSpace):
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


class discrete(SampleSpace):

    def __init__(self, min, max, shape=None):
        super(discrete, self).__init__()
        self.min = min
        self.max = max
        self.shape = shape

    def roll(self):
        self.history = randint(self.min, high=self.max, size=self.shape)
        return self.history


class spinlattice(SampleSpace):
    """sample space for spin lattice.
    """

    def __init__(self, shape, state=(0, 1), nflips=1, p=0.5):
        super(spinlattice, self).__init__()
        self.down, self.up = state
        self.shape = shape
        self.nflips = nflips
        self.p = p

    def choose(self, x):
        dice = rand()
        if dice > self.p:
            return self.up
        else:
            return self.down

    def rand(self):
        data = np.zeros(self.shape)
        choose = np.vectorize(self.choose)
        return choose(data)

    def randindex(self):
        return tuple(randint(0, each) for each in self.shape)

    def flip(self, index):
        if self.history[index] == self.up:
            self.history[index] = self.down
        else:
            self.history[index] = self.up
        return self.history

    def randflip(self):
        if self.nflips == 1:
            self.flip(self.randindex())
        else:
            inds = []
            count = 0
            while count != self.nflips:
                ind = self.randindex()
                if ind not in inds:
                    inds.append(ind)
                else:
                    count -= 1
                count += 1
            for ind in inds:
                self.flip(ind)
        return self.history

    def roll(self):
        if self.history is None:
            self.history = self.rand()
            return self.history
        else:
            return self.randflip()

    def copy(self):
        return self.history.copy()
