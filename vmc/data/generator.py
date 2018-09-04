from uuid import uuid1
import h5py
import hashlib
import errno
import os
import numpy as np

from tables import *

from vmc.sampler import STDirect
from vmc.basis import MBOp, sigmaz

from tqdm import tqdm
from multiprocessing import current_process

__all__ = [
    'DataGenerator',
    'FixedBasis',
]


class MeasureData(IsDescription):
    name = StringCol(16)
    ham = StringCol(16)
    lattice = StringCol(16)
    shape = Int32Col(shape=(2, ))
    pbc = BoolCol()
    data = StringCol(36)
    exact = BoolCol()
    level = Int32Col()


class DataGenerator(object):
    """ generate measurement data

    this class offers methods to save data in a hdf5 file.

    Keywords:

        hamiltonian, ham: a hamiltonian from vmc.ham should be given
        level: the level of generated state, (0 for ground state)
        name: name for the state
        root: root path
    """

    def __init__(self, state, **kwargs):
        self.state = state / np.linalg.norm(state)
        if 'hamiltonian' in kwargs:
            self.h = kwargs.pop('hamiltonian')
        elif 'ham' in kwargs:
            self.h = kwargs.pop('ham')
        else:
            raise ValueError('hamiltonian needed')

        self.shape = tuple(self.h.size)
        self.n = np.prod(self.shape)

        if 'level' in kwargs:
            self.level = kwargs.pop('level')
        else:
            self.level = 0

        if 'name' in kwargs:
            self.name = kwargs.pop('name')
        else:
            self.name = self.h.name + ' ' + 'level %s' % self.level

        if 'root' in kwargs:
            self.root = kwargs.pop('root')
        else:
            self.root = 'data'

        if 'len' in kwargs:
            self.len = kwargs.pop('len')
        else:
            self.len = 1000

        if 'basis' in kwargs:
            self.basis = kwargs.pop('basis')
        else:
            self.basis = None

        self.path = os.path.join(self.root, self.h.name)
        try:
            os.makedirs(self.path)
        except OSError as e:
            if e.errno == errno.EEXIST:
                pass
            else:
                raise

        self.filename = str(uuid1()) + '.h5'
        self.register_table = os.path.join(self.path, 'check.h5')

        self._generate()

    def _isexists(self):
        if os.path.isfile(self.register_table):
            return True
        else:
            return False

    def mkname(self):
        m = hashlib.md5()
        m.update(self.h.name.encode())
        prefix = hex(int(m.hexdigest(), 16) % (10 ** 8))[2:] + str(self.level)
        shape = ''
        for each in self.shape:
            shape += '-' + str(each)
        prefix += shape
        m.update(self.h.lattice.name.encode())
        prefix += '-' + hex(int(m.hexdigest(), 16) % (10 ** 8))[2:]
        return prefix

    def _generate(self):
        if self._isexists():
            print('find check file')
            h5file = open_file(self.register_table, 'a')
            table = h5file.root.measure
        else:
            print('no check file, creating')
            h5file = open_file(self.register_table, 'w')
            table = h5file.create_table('/', 'measure', MeasureData)
        row = table.row
        row['name'] = self.name
        row['shape'] = list(self.shape)
        row['ham'] = self.h.name
        row['lattice'] = self.h.lattice.name
        row['pbc'] = self.h.lattice.pbc
        row['exact'] = True
        row['data'] = self.filename
        row['level'] = self.level
        row.append()
        table.flush()
        h5file.close()

        filename = os.path.join(self.path, self.filename)
        config_path = os.path.join('data', 'configs')
        basis_path = os.path.join('data', 'basis')
        exact_path = os.path.join('data', 'state')
        data, basis = self.generate()
        with h5py.File(filename, 'w') as f:
            g = f.create_group('data')
            g.attrs['name'] = self.name
            g.attrs['shape'] = self.shape
            g.attrs['h'] = self.h.name
            g.attrs['lattice'] = self.h.lattice.name
            g.attrs['pbc'] = self.h.lattice.pbc
            g.attrs['exact'] = True
            g.attrs['level'] = self.level

            f_exact = f.create_dataset(
                exact_path, (len(self.state), ), 'complex128')
            f_data = f.create_dataset(
                config_path, (self.len, *self.shape), 'float64')
            f_basis = f.create_dataset(
                basis_path, (self.len, *self.shape, 2), 'float64')

            process_id = current_process()._identity
            if process_id:
                pos, = process_id
            else:
                pos = 0
            desc = '%s copying' % self.name
            bar = tqdm(total=2 * self.len,
                       desc=desc, position=pos)
            for i, data in enumerate(data):
                f_data[i] = data.numpy()
                bar.update()

            for i, base in enumerate(basis):
                f_basis[i] = np.array(base)
                bar.update()
            bar.close()

            f_exact[:] = self.state[:]

    def generate(self):
        raise NotImplementedError


class FixedBasis(DataGenerator):

    def generate(self):
        if self.basis is None:
            self.basis = [sigmaz for i in range(self.n)]
        ops = MBOp(self.basis)
        _state = ops.invtrans(self.state)
        desc = '%s sampling' % self.name
        sampler = STDirect(_state * _state.conj(), size=self.shape)
        data = sampler.sample(itr=self.len, desc=desc)['sample']
        basis = list(ops.params() for i in range(len(sampler.collector)))
        return data, basis
