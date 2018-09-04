"""collector

this module implements sample collectors,
and provides methods to cooperate with
torch.autograd engine.

TODO:
    * MPI support
"""

from vmc.utils import make_instance
from .base import CollectorBase, gradient
from .stcollector import STCollector

__all__ = [
    '__traits__',
    'Collector',
    'iscollector',
    'gradient',
    'CollectorBase',
    'STCollector',
]

__traits__ = {
    'base': CollectorBase,
    'std': STCollector,
    'STCollector': STCollector,
}


def iscollector(ins):
    return isinstance(ins, CollectorBase)


def Collector(x, **kwargs):
    if iscollector(x):
        return x
    elif isinstance(x, str):
        return __traits__[x](**kwargs)
    else:
        raise TypeError("Collector only takes instance of collectors"
                        "not %s" % type(x))


del make_instance
