"""Hamiltonian

this module provides quantum hamiltonians defined on lattices

TODO:
    * hamiltonian expr parser
"""

from .base import HamiltonianBase
from .consts import ConstHamiltonian, SigmaX, SigmaY, SigmaZ

from .local import one, two
from .tfi import TFI
from .heisenberg import J1J2, XXZ


__all__ = [
    '__traits__',
    'isham',
    'Ham',
    'HamiltonianBase',
    'ConstHamiltonian',
    'SigmaX',
    'SigmaY',
    'SigmaZ',
    'one',
    'two',
    'TFI',
    'J1J2',
    'XXZ'
]

__traits__ = {
    'base': HamiltonianBase,
    'hamiltonian': HamiltonianBase,
    'HamiltonianBase': HamiltonianBase,
    'const': ConstHamiltonian,
    'const hamiltonian': ConstHamiltonian,
    'constham': ConstHamiltonian,
    'sigmax': SigmaX,
    'SigmaX': SigmaX,
    'sigmay': SigmaY,
    'SigmaY': SigmaY,
    'sigmaz': SigmaZ,
    'SigmaZ': SigmaZ,
    'local1 x': one.SigmaX,
    'Local1SigmaX': one.SigmaX,
    'local1 y': one.SigmaY,
    'Local1SigmaY': one.SigmaY,
    'local1 z': one.SigmaZ,
    'Local1SigmaZ': one.SigmaZ,
    'local2': two.Local2,
    'Local2': two.Local2,
    'local2 x': two.SigmaX,
    'Local2SigmaX': two.SigmaX,
    'local2 y': two.SigmaY,
    'Local2SigmaY': two.SigmaY,
    'local2 z': two.SigmaZ,
    'Local2SigmaZ': two.SigmaZ,
    'TFI': TFI,
    'J1J2': J1J2,
    'XXZ': XXZ
}


def isham(ins):
    return isinstance(ins, HamiltonianBase)


def Ham(name, **params):
    if issubclass(__traits__[name], ConstHamiltonian):
        return __traits__[name]()
    else:
        return __traits__[name](**params)
