"""1-local hamiltonians
"""


from vmc.ham.base import HamiltonianBase


class SigmaX(HamiltonianBase):
    """1-local sigma_x hamiltonian"""

    def __init__(self, **params):
        name = '1-local sigma x'
        super(SigmaX, self).__init__(name, **params)

    def nnz(self, config):
        RHS = config.clone()
        for i in self.lattice.grid(nn=0):
            RHS[i] *= -1
            yield RHS, 1
            RHS[i] *= -1


class SigmaY(HamiltonianBase):
    """1-local sigma_y hamiltonian"""

    def __init__(self, **params):
        name = '1-local sigma y'
        super(SigmaY, self).__init__(name, **params)

    def nnz(self, config):
        RHS = config.clone()
        for i in self.lattice.grid(nn=0):
            RHS[i] *= -1
            yield RHS, -1.j * RHS[i]
            RHS[i] *= -1


class SigmaZ(HamiltonianBase):
    """1-local sigma z hamiltonian"""

    def __init__(self, **params):
        name = '1-local sigma z'
        super(SigmaZ, self).__init__(name, **params)

    def nnz(self, config):
        RHS = config.clone()
        ret = 0.0
        for i in self.lattice.grid(nn=0):
            ret += RHS[i]
        yield RHS, ret
