from qmtk._lattice import *
from qmtk.utils.preprocess import alias, require


class LatticeBase(object):
    """lattice base
    """

    def __init__(self, nbr):
        super(LatticeBase, self).__init__()
        self._cache = {}
        self.nbr = None

    @property
    def cache(self):
        return self._cache[self.nbr]

    @cache.setter
    def cache(self, value):
        self._cache[self.nbr] = value

    def grid(self, nbr=None):
        if nbr is None:
            self.nbr = 0
        else:
            self.nbr = nbr

        if self.nbr not in self._cache:
            self.cache = self.bonds()
        return self.catch


class Chain(LatticeBase, ChainBase):
    pass


class Square(LatticeBase, SquareBase):
    pass
