from vmc.configs import IterateAll
from vmc.lattice import Lattice, islattice, Chain
import vmc.utils as utils
from scipy.sparse.dok import _prod
from scipy.sparse import lil_matrix


class HamiltonianBase(object):
    """Hamiltonian Base"""

    @staticmethod
    def __has_shape(kwargs):
        return any([
            'size' in kwargs,
            'shape' in kwargs,
            'length' in kwargs
        ])

    @staticmethod
    def __get_lattice_kwargs(kwargs):
        lattice_kwargs = {}
        if 'size' in kwargs:
            lattice_kwargs['shape'] = kwargs.pop('size')
        elif 'shape' in kwargs:
            lattice_kwargs['shape'] = kwargs.pop('shape')
        elif 'length' in kwargs:
            lattice_kwargs['length'] = kwargs.pop('length')
        else:
            raise TypeError("missing shape of the hamiltonian")

        if 'pbc' in kwargs:
            lattice_kwargs['pbc'] = kwargs.pop('pbc')
        if 'lattice_params' in kwargs:
            ltc_params = kwargs.pop('lattice_params')
            if isinstance(ltc_params, dict):
                lattice_kwargs.update(ltc_params)
            else:
                raise ValueError("lattice parameters should be dict"
                                 "not %s" % type(ltc_params))
        return lattice_kwargs

    def __init__(self, name='hamiltonian', **kwargs):
        super(HamiltonianBase, self).__init__()
        # lattice
        if 'lattice' in kwargs:
            ltc = kwargs.pop('lattice')
            if islattice(ltc):
                self.lattice = ltc
            elif isinstance(ltc, dict):
                self.lattice = Lattice(**ltc)
            else:
                lattice_kwargs = self.__get_lattice_kwargs(kwargs)
                self.lattice = Lattice(ltc, **lattice_kwargs)
            self.size = self.lattice.size()
        elif self.__has_shape(kwargs):
            lattice_kwargs = self.__get_lattice_kwargs(kwargs)
            self.lattice = Chain(**lattice_kwargs)
            self.size = self.lattice.size()
            if len(self.size) is not 1:
                raise ValueError("Wrong size, default lattice"
                                 " is chain lattice")
        else:
            self.lattice = None
            self.size = 1
        self.name = name
        self.params = kwargs

    def nnz(self, config):
        """
        return the non-zero values in a hamiltonian H,
        with its related configurations
        """
        RHS = config.clone()
        if self.lattice.dim is not config.dim():
            raise ValueError('config size should meets hamiltonian')
        return self.nnz_iter(RHS)

    def nnz_iter(self, RHS):
        raise NotImplementedError

    def __str__(self):
        ret = '%s:' % (self.name)
        ret += '\n size: %s' % self.size
        for param_key, param_val in self.params.items():
            ret += '\n %s: %s' % (param_key, param_val)
        return ret

    def mat(self):
        """get the matrix form

        Returns:
            hamiltonian matrix: a scipy.sparse.lil_matrix

        Raises:
            Warning: when number of elements in the hamiltonian
            is too large (> 25) a waring will raises.
        """
        numel = 2 ** _prod(self.size)
        if _prod(self.size) > 25:
            raise Warning('this hamiltonian could be too large')
        data = lil_matrix((numel, numel),
                          dtype='complex128')
        for lhs in IterateAll(size=self.size):
            for rhs, val in self.nnz(lhs):
                data[utils.bin(lhs), utils.bin(rhs)] += val
        return data
