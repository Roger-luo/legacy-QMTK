"""2-local hamiltonians
"""

from vmc.ham.base import HamiltonianBase


class Local2(HamiltonianBase):
    """local-2 hamiltonian"""

    def __init__(self, **params):
        # choose neighbor
        if 'nbr' in params:
            self.nbr = params['nbr']
            params['neighbor'] = params.pop('nbr')
        elif 'neighbor' in params:
            self.nbr = params['neighbor']
        else:
            self.nbr = 1
        # choose name
        if 'name' in params:
            name = params.pop('name')
        else:
            name = '2-local'
        super(Local2, self).__init__(name, **params)

    def nnz(self, LHS, local, recover):
        RHS = LHS.clone()
        if self.dim is not LHS.dim():
            raise ValueError('config size should meets hamiltonian')
        for i, j in self.lattice.grid(nbr=self.nbr):
            yield local(RHS, i, j)
            recover(RHS, i, j)


class SigmaX(Local2):
    """2-local sigma x hamiltonian"""

    def __init__(self, **params):
        name = '2-local sigma x'
        super(SigmaX, self).__init__(name=name, **params)

    def nnz(self, LHS):
        def local(config, i, j):
            config[i] *= -1
            config[j] *= -1
            return config, 1

        def recover(config, i, j):
            config[i] *= -1
            config[j] *= -1

        return Local2.nnz(self, LHS, local, recover)


class SigmaY(Local2):
    """2-local sigma y hamiltonian"""

    def __init__(self, **params):
        name = '2-local sigma y'
        super(SigmaY, self).__init__(name=name, **params)

    def nnz(self, LHS):
        def local(config, i, j):
            config[i] *= -1
            config[j] *= -1
            return config, -1 * config[i] * config[j]

        def recover(config, i, j):
            config[i] *= -1
            config[j] *= -1

        return Local2.nnz(self, LHS, local, recover)


class SigmaZ(Local2):
    """2-local sigma z hamiltonian"""

    def __init__(self, **params):
        name = '2-local sigma z'
        super(SigmaZ, self).__init__(name=name, **params)

    def nnz(self, config):
        RHS = config.clone()
        yield RHS, sum(RHS[i] * RHS[j]
                       for i, j in self.lattice.grid(nbr=self.nbr))
