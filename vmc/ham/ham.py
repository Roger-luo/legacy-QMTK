"""
Hamiltonians (quantum)
"""

from .hamiltonian import *

# TODO: merge these after lattice is added to other hamiltonians
from .heisenberg import *
from .tfi import *

__all__ = [
    '__traits__',
    'Ham',
    'HamiltonianBase',
    'ConstHamiltonian',
    'SigmaX',
    'SigmaY',
    'SigmaZ',
    'Local1SigmaX',
    'Local1SigmaY',
    'Local1SigmaZ',
    'Local2',
    'Local2SigmaX',
    'Local2SigmaY',
    'Local2SigmaZ',
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
    'local1 x': Local1SigmaX,
    'Local1SigmaX': Local1SigmaX,
    'local1 y': Local1SigmaY,
    'Local1SigmaY': Local1SigmaY,
    'local1 z': Local1SigmaZ,
    'Local1SigmaZ': Local1SigmaZ,
    'local2': Local2,
    'Local2': Local2,
    'local2 x': Local2SigmaX,
    'Local2SigmaX': Local2SigmaX,
    'local2 y': Local2SigmaY,
    'Local2SigmaY': Local2SigmaY,
    'local2 z': Local2SigmaZ,
    'Local2SigmaZ': Local2SigmaZ,
    'TFI': TFI,
    'J1J2': J1J2,
    'XXZ': XXZ
}


def Ham(name, **params):
    if issubclass(__traits__[name], ConstHamiltonian):
        return __traits__[name]()
    else:
        return __traits__[name](**params)
