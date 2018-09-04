""" Configuration Generators
configs provide spin configuration generators
for quantum many-body system

TODO:
    * support for classical lattice system (like Ising model)
    * more generators (at least a list is needed)
"""

from .base import GeneratorBase
from .iterall import IterateAll
from .randselect import RandomSelect
from .spinconserve import SpinConserve


__all__ = [
    '__traits__',
    'GeneratorBase',
    'isgenerator',
    'Generator',
    'IterateAll',
    'RandomSelect',
    'SpinConserve',
]

# style guide
# traits should offer abrreviation and full name at least
# other alias is welcome
# but pls remember to check if there are same traits in the tests

__traits__ = {
    'base': GeneratorBase,
    'generator': GeneratorBase,
    'rs': RandomSelect,  # abbr.
    'randselect': RandomSelect,  # full name
    'sc': SpinConserve,
    'spin conserve': SpinConserve,
    'ia': IterateAll,
    'iterall': IterateAll,
    'iterate all': IterateAll,
}


def isgenerator(gen):
    return isinstance(gen, GeneratorBase)


def Generator(x, **kwargs):
    if isgenerator(x):
        return x
    elif isinstance(x, str):
        return __traits__[x](**kwargs)
    else:
        raise TypeError("Generator only takes instance of generators"
                        "not %s" % type(x))
