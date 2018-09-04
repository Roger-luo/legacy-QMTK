from .base import HamiltonianBase


class TFI(HamiltonianBase):
    """traverse field Ising Model"""

    def __init__(self, mag=1, **params):
        name = 'TFI'
        super(TFI, self).__init__(name, **params)
        self.mag = mag

    def nnz_iter(self, RHS):
        for i in self.lattice.grid(nbr=0):
            RHS[i] *= -1
            yield RHS, - self.mag
            RHS[i] *= -1
        sigmaz = 0.0
        for i, j in self.lattice.grid(nbr=1):
            sigmaz += RHS[i] * RHS[j]
        yield RHS, - sigmaz
