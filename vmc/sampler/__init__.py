"""Monte Carlo Samplers

this module provides sampler objects that
generate samples from proposed distribution

TODO:
    * MPI support
    * Metropolis-Hasting method is not actually implemented
"""

from .base import SamplerBase
from .st import STMetropolis, STDirect

__all__ = [
    'SamplerBase',
    'STMetropolis',
    'STDirect',
]

__traits__ = {
    'base': SamplerBase,
    'SamplerBase': SamplerBase,
    'smh': STMetropolis,
    'STMetropolis': STMetropolis,
    'std': STDirect,
    'STDirect': STDirect,
}


def issampler(ins):
    return isinstance(ins, SamplerBase)


def Sampler(x, **kwargs):
    if issampler(x):
        return x
    elif isinstance(x, str):
        return __traits__[x](**kwargs)
    else:
        raise TypeError("Sampler only takes instance of generators"
                        "not %s" % type(x))
