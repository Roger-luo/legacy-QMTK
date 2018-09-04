"""Lattice

This module provide definition of lattices.
All the lattice is iteratable.

TODO:
    * support for arbitrary neighbors
"""

from .base import LatticeBase
from .chain import Chain
from .square import Square

__all__ = [
    'LatticeBase',
    'Lattice',
    'islattice',
    '__traits__',
    'Chain',
    'Square'
]

__traits__ = {
    'base': LatticeBase,
    'LatticeBase': LatticeBase,
    'chain': Chain,
    'Chain': Chain,
    'square': Square,
    'Square': Square,
}


def islattice(ins):
    return isinstance(ins, LatticeBase)


def Lattice(x, **kwargs):
    if isinstance(x, str):
        return __traits__[x](**kwargs)
    else:
        raise TypeError("Lattice only takes instance of lattices"
                        "not %s" % type(x))
