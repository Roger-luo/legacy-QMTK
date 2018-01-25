from qmtk._lattice import *
from qmtk.utils.preprocess import alias, require


class LatticeBase(object):
    """lattice base
    """

    @alias(shape=['length', 'size'])
    @require('shape')
    def __init__(self, **kwargs):
        super(LatticeBase, self).__init__()
        self.shape = kwargs.pop('shape')

    @property
    def shape(self):
        return self._get_shape()

    @shape.setter
    def shape(self, value):
        return self._set_shape(value)


class Chain(LatticeBase, ChainBase):
    pass


class Square(LatticeBase, SquareBase):
    pass
