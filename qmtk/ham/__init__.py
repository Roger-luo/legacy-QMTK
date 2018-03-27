"""a collection of hamiltonians


TODO:
    * hamiltonian expr parser
    * cpp implementation
"""

from .core import HamiltonianBase, SpinHBase
from .tfi import TFI
from .heisenberg import J1J2

__all__ = [
    'TFI',
    'J1J2',
]

# factory method


def ham(name, **kwargs):
    for each in HamiltonianBase.__subclasses__():
        if each.__name__.lower() == name.lower():
            return each(**kwargs)

    for each in SpinHBase.__subclasses__():
        if each.__name__.lower() == name.lower():
            return each(**kwargs)
    raise ValueError("%s is not in the collection" % name)
