from vmc.lattice import *
from scipy.sparse import lil_matrix
from numpy import prod
import vmc.utils as utils
from vmc.configs import IterateAll


__all__ = [
    'HamiltonianBase', 'ConstHamiltonian',
    'SigmaX', 'SigmaY', 'SigmaZ', 'Local2',
    'Local1SigmaX', 'Local1SigmaY', 'Local1SigmaZ',
    'Local2SigmaX', 'Local2SigmaY', 'Local2SigmaZ',
    'isham',
]


class HamiltonianBase(object):
    """Hamiltonian Base"""

    def __init__(self, name='hamiltonian', **params):
        super(HamiltonianBase, self).__init__()
        # TODO: initialize with a subtype of HamiltonainBase
        # shape
        # periodic bound
        if 'pbc' in params:
            self.pbc = params['pbc']
            params['periodic bound'] = params.pop('pbc')
        elif 'periodic bound' in params:
            self.pbc = params['periodic bound']
        else:
            self.pbc = False
        # lattice
        if 'lattice' in params:
            lattice = params.pop('lattice')
            if isinstance(lattice, str) and 'size' in params:
                try:
                    self.lattice = __lattice__[lattice](
                        params['size'], pbc=params['pbc'])
                except TypeError:
                    raise TypeError('size only takes list, int \
                        or tuple, not : %s' % (str(size)))
            elif isinstance(lattice, LatticeBase):
                self.lattice = lattice
                self.pbc = lattice.pbc
            else:
                raise ValueError('lattice should be either \
                    string or an instance of lattice, \
                    not: %s' % (type(lattice)))
            self.size = self.lattice.size()
            self.dim = self.lattice.dim
        elif 'size' in params:
            try:
                self.lattice = Chain(params['size'], pbc=self.pbc)
            except TypeError:
                raise TypeError('size only takes list, int \
                        or tuple, not : %s' % (str(size)))
            self.size = self.lattice.size()
            self.dim = self.lattice.dim
        else:
            self.lattice = None
            self.size = None
            self.dim = None
        self.name = name
        self.params = params

    def nnz(self, config):
        """
        return the non-zero values in a hamiltonian H,
        with its related configurations
        """
        raise NotImplementedError

    def __str__(self, param_list=[]):
        ret = '%s:' % (self.name)
        ret += '\n size: %s' % self.size
        for param_key, param_val in self.params.items():
            ret += '\n %s: %s' % (param_key, param_val)
        return ret

    def mat(self):
        numel = 2 ** prod(self.size)
        if prod(self.size) > 25:
            raise Warning('this hamiltonian could be too large')
        data = lil_matrix((numel, numel),
                          dtype='complex128')
        for lhs in IterateAll(size=self.size):
            for rhs, val in self.nnz(lhs):
                data[utils.bin(lhs), utils.bin(rhs)] += val
        return data


def isham(h):
    return isinstance(h, HamiltonianBase)


class ConstHamiltonian(HamiltonianBase):
    """Const Hamiltonian"""

    def __init__(self, name='const hamiltonian'):
        super(ConstHamiltonian, self).__init__(name)


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


class Local1SigmaX(HamiltonianBase):
    """1-local sigma_x hamiltonian"""

    def __init__(self, **params):
        name = '1-local sigma x'
        super(Local1SigmaX, self).__init__(name, **params)

    def nnz(self, config):
        RHS = config.clone()
        for i in self.lattice.grid(nn=0):
            RHS[i] *= -1
            yield RHS, 1
            RHS[i] *= -1


class Local1SigmaY(HamiltonianBase):
    """1-local sigma_y hamiltonian"""

    def __init__(self, **params):
        name = '1-local sigma y'
        super(Local1SigmaY, self).__init__(name, **params)

    def nnz(self, config):
        RHS = config.clone()
        for i in self.lattice.grid(nn=0):
            RHS[i] *= -1
            yield RHS, -1.j * RHS[i]
            RHS[i] *= -1


class Local1SigmaZ(HamiltonianBase):
    """1-local sigma z hamiltonian"""

    def __init__(self, **params):
        name = '1-local sigma z'
        super(Local1SigmaZ, self).__init__(name, **params)

    def nnz(self, config):
        RHS = config.clone()
        ret = 0.0
        for i in self.lattice.grid(nn=0):
            ret += RHS[i]
        yield RHS, ret


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


class Local2SigmaX(Local2):
    """2-local sigma x hamiltonian"""

    def __init__(self, **params):
        name = '2-local sigma x'
        super(Local2SigmaX, self).__init__(name=name, **params)

    def nnz(self, LHS):
        def local(config, i, j):
            config[i] *= -1
            config[j] *= -1
            return config, 1

        def recover(config, i, j):
            config[i] *= -1
            config[j] *= -1

        return Local2.nnz(self, LHS, local, recover)


class Local2SigmaY(Local2):
    """2-local sigma y hamiltonian"""

    def __init__(self, **params):
        name = '2-local sigma y'
        super(Local2SigmaY, self).__init__(name=name, **params)

    def nnz(self, LHS):
        def local(config, i, j):
            config[i] *= -1
            config[j] *= -1
            return RHS, -1 * RHS[i] * RHS[j]

        def recover(config, i, j):
            RHS[i] *= -1
            RHS[j] *= -1

        return Local2.nnz(self, LHS, local, recover)


class Local2SigmaZ(Local2):
    """2-local sigma z hamiltonian"""

    def __init__(self, **params):
        name = '2-local sigma z'
        super(Local2SigmaZ, self).__init__(name=name, **params)

    def nnz(self, config):
        RHS = config.clone()
        yield RHS, sum(RHS[i] * RHS[j]
                       for i, j in self.lattice.grid(nbr=self.nbr))
