from .core import SpinHBase


class J1J2(SpinHBase):
    """J1J2
    """

    def load_J1J2(self, kwargs):
        if 'J' not in kwargs:
            raise ValueError("J1J2 model requires parameter J")
        self.J = kwargs.pop('J')

    def nnz_iter(self, RHS):
        sigmaz = 0.0
        J = self.J
        for i, j in self.lattice.grid(nbr=1):
            sigmaz += J[0] * RHS[i] * RHS[j]
            RHS[i] = self.flip(RHS[i])
            RHS[j] = self.flip(RHS[j])
            yield RHS, J[0] * (1 - RHS[i] * RHS[j])
            RHS[i] = self.flip(RHS[i])
            RHS[j] = self.flip(RHS[j])
        # next nearest
        for i, j in self.lattice.grid(nbr=2):
            sigmaz += J[1] * RHS[i] * RHS[j]
            RHS[i] = self.flip(RHS[i])
            RHS[j] = self.flip(RHS[j])
            yield RHS, J[0] * (1 - RHS[i] * RHS[j])
            RHS[i] = self.flip(RHS[i])
            RHS[j] = self.flip(RHS[j])
        yield RHS, sigmaz
