from .base import HamiltonianBase


class ConstHamiltonian(HamiltonianBase):
    """Const Hamiltonian"""

    def __init__(self, name='const hamiltonian'):
        self.name = name
        self.params = {}
        self.size = 1


class SigmaX(ConstHamiltonian):
    """sigma x"""

    def __init__(self):
        super(SigmaX, self).__init__('sigma x')

    def nnz(self, config):
        RHS = config.clone()
        RHS[0] *= -1
        yield RHS, 1


class SigmaY(ConstHamiltonian):
    """sigma y"""

    def __init__(self):
        super(SigmaY, self).__init__('sigma y')

    def nnz(self, config):
        RHS = config.clone()
        RHS[0] *= -1
        yield RHS, 1.j * config[0]


class SigmaZ(ConstHamiltonian):
    """sigma z"""

    def __init__(self):
        super(SigmaZ, self).__init__('sigma z')

    def nnz(self, config):
        RHS = config.clone()
        yield RHS, RHS[0]

