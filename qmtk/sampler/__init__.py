"""qmtk.sampler.

this module offers samplers for arbitrary tasks.
following sampling methods is implemented:

- Acceptance and Reject sampling
- simple Direct sampling
- Metropolis-Hasting sampling

and there is two factory class implemented:

- sample: for single thread sampling
- multi: for multi processing sampling

to import the sampler, simply import a sampler from the qmtk.sampler
module. or if you would like a multi-process version, import a sampler
from qmtk.sampler.multi.

Usage:

all the samplers are decorators. define your distribution function in python
and use a sampler to decorate it, or just use the factory methods. And you have
to specify the sample domain you are sampling from, which is defined in
qmtk.sampler.space with real for real space domain, discrete for discrete
integer domain, and spinlattice for spin lattice domain
(with a spin on a lattice).

from qmtk.sampler import metropolis


@metropolis(space.real(-4, 4), itr=20000)
def normal(x):
    factor = 1 / np.sqrt(2 * np.pi)
    return factor * np.exp(- x ** 2 / 2)


or for multi-processing version, just import it from here
with exactly same code, you can do it multiprocessly, by
default, the sampler will use all your available processes
on your local CPU chips, but you can always specify it with
keyword `processes` like `processes=8`.

from qmtk.multi import metropolis
@metropolis(space.real(-4, 4), itr=20000, processes=8)
def normal(x):
    factor = 1 / np.sqrt(2 * np.pi)
    return factor * np.exp(- x ** 2 / 2)


have fun!
"""


from .space import real, discrete, spinlattice, SampleSpace
from .core import reject, direct, metropolis, SamplerBase
import multi


__all__ = [
    'reject',
    'direct',
    'metropolis',
    'sample',
    'multi',

    'real',
    'discrete',
    'spinlattice',
    'SampleSpace',
]


class sample(object):

    __alias__ = {
        'metropolis': metropolis,
        'metro': metropolis,
        'MH': metropolis,
        'direct': direct,
        'SDS': direct,
        'reject': reject,
        'AR': reject,
    }

    def __init__(self, sampler, *args, **kwargs):
        if isinstance(sampler, str):
            self.sampler = self.__alias__[sampler](*args, **kwargs)
        elif isinstance(sampler, SamplerBase):
            self.sampler = sampler
        elif issubclass(sampler, SamplerBase):
            self.sampler = sampler(*args, **kwargs)

    def __call__(self, func):
        return self.sampler.__call__(func)
