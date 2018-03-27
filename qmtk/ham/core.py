from scipy.sparse import lil_matrix
from inspect import getmembers
from qmtk.space import spinlattice
from qmtk.utils.preprocess import alias, require
from qmtk.utils import spin2n


class HamiltonianBase(object):
    """Hamiltonian Base"""

    @alias(lattice=['ltc', 'chain', 'square'])
    @require('lattice')
    def __init__(self, **kwargs):
        self.name = type(self).__name__
        self.lattice = kwargs.pop('lattice')

        # other parameters
        for name, method in getmembers(self):
            if name.startswith('load_'):
                method(kwargs)

    @property
    def shape(self):
        return self.lattice.shape

    @shape.setter
    def shape(self, value):
        self.lattice.shape = value

    @property
    def numel(self):
        return 2 ** self.lattice.numel()

    def nnz(self, rhs):
        """return the non-zero values in a
        hamiltonian with its related rhs configuration
        """
        RHS = rhs.copy()
        return self.nnz_iter(RHS)

    def nnz_iter(self, rhs):
        raise NotImplementedError

    def __repr__(self):
        repr = '%s:' % (self.name)
        repr += '\n shape: %s' % str(self.shape)
        return repr

    def mat(self):
        """get the matrix form

        returns:
            matrix: a sicpy.sparse.lil_matrix object
        """
        if self.lattice.numel() > 25:
            raise Warning('this hamiltonian could be too large')
        data = lil_matrix((self.numel, self.numel), dtype='complex128')
        for lhs in spinlattice(shape=self.shape):
            for rhs, val in self.nnz(lhs):
                data[spin2n(lhs), spin2n(rhs)] += val
            return data


class SpinHBase(HamiltonianBase):

    def load_spin(self, kwargs):
        if 'state' in kwargs:
            self.down, self.up = kwargs.pop('state')
        else:
            self.down, self.up = 0, 1

    def flip(self, x):
        if x == self.up:
            return self.down
        else:
            return self.up
