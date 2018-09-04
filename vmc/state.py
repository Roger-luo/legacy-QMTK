from configs import IterateAll
from vmc.lattice import LatticeBase
from vmc.basis import MBOp
from vmc.utils import typecheck, alias, kronprod
from vmc.ham import HamiltonianBase
from numpy.linalg import norm
from numpy.random import rand
import torch



# support for multiple configs
# _measure should output an iterable rather a scalar


class qstate(object):
    def __init__(self, arg):
        super(qstate, self).__init__()
        self.arg = arg
        