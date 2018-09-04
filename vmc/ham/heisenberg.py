from .base import HamiltonianBase


class J1J2(HamiltonianBase):
    """J1J2"""

    def __init__(self, **params):
        name = 'J1-J2'
        super(J1J2, self).__init__(name, **params)
        if 'J' not in self.params:
            self.params['J'] = (1, 0.5)
        self.J = self.params['J']

    def nnz_iter(self, RHS):
        # sigma_x, sigma_y
        sigmaz = 0.0
        J = self.J
        for i, j in self.lattice.grid(nbr=1):
            sigmaz += J[0] * RHS[i] * RHS[j]
            RHS[i] *= -1
            RHS[j] *= -1
            yield RHS, J[0] * (1 - RHS[i] * RHS[j])  # sigma y
            RHS[i] *= -1
            RHS[j] *= -1
        # next nearest
        for i, j in self.lattice.grid(nbr=2):
            sigmaz += J[1] * RHS[i] * RHS[j]
            RHS[i] *= -1
            RHS[j] *= -1
            yield RHS, J[1] * (1 - RHS[i] * RHS[j])
            RHS[i] *= -1
            RHS[j] *= -1
        yield RHS, sigmaz


class XXZ(HamiltonianBase):
    """XXZ model"""

    def __init__(self, **params):
        name = 'XXZ'
        super(XXZ, self).__init__(name=name, **params)
        if 'J' not in self.params:
            self.params['J'] = (1.0, 1.0)
        self.J = self.params['J']

    def nnz_iter(self, RHS):
        sigmaz = 0.0
        J = self.J
        for j, k in self.lattice.grid(nbr=self.params['nbr']):
            sigmaz += - J[1] * RHS[j] * RHS[k]
            RHS[j] *= -1
            RHS[k] *= -1
            yield RHS, - J[0] * (1 - RHS[j] * RHS[k])
            RHS[j] *= -1
            RHS[k] *= -1
        yield RHS, sigmaz
