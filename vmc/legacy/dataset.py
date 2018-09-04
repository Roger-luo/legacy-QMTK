from random import choice
from numpy import log2

import torch
import torch.utils.data as data
import errno
import os

from vmc.utils import ground, bin
from vmc.sampler import PseudoRandom, STMetropolis
from vmc.basis import MBOp, sigmax, sigmay, sigmaz


class DataBase(data.Dataset):
    """base type for tomography data

    Attributes:

        state: an object with __getitem__
    """

    raw_folder = 'raw'
    processed_folder = 'processed'
    training_file = 'training.tomo'
    test_file = 'test.tomo'

    def __init__(self, kwargs):
        super(DataBase, self).__init__()
        self.root = os.path.expanduser(kwargs.pop('root'))
        if 'transform' in kwargs:
            self.transform = kwargs.pop('transform')
        else:
            self.transform = None

        if 'basis_transform' in kwargs:
            self.basis_transform = kwargs.pop('basis_transform')
        else:
            self.basis_transform = None

        if 'train' in kwargs:
            self.train = kwargs.pop('train')
        else:
            self.train = True

        if 'prefix' in kwargs:
            prefix = kwargs.pop('prefix')
            self.training_file = prefix + '_' + self.training_file
            self.test_file = prefix + '_' + self.test_file

        if 'hamiltonian' in kwargs:
            h = kwargs.pop('hamiltonian')
        elif 'ham' in kwargs:
            h = kwargs.pop('ham')
        else:
            h = None

        self.state = None
        if self._check_exists():
            print('find data, start loading')
            self.load()
        else:
            print('cannot find data, start generating')
            if 'state' in kwargs:
                print('find given state')
                self.state = kwargs.pop('state')
                self.n = int(log2(len(self.state)))
                self.size = kwargs.pop('size')
            elif h is not None:
                print('find hamiltonian, start calculating ground state')
                self.n = h.lattice.numel()
                _, self.state = ground(h)
                self.size = h.size
            else:
                raise ValueError("need a state, keyword"
                                 "state or hamiltonian needed")
            self.training_file = str(self.n) + self.training_file
            self.test_file = str(self.n) + self.test_file
            self.gen()

    def __getitem__(self, index):
        if self.train:
            config, basis = self.train_data[index], self.train_basis[index]
        else:
            config, basis = self.test_data[index], self.test_basis[index]

        if self.transform is not None:
            config = self.transform(config)

        if self.basis_transform is not None:
            basis = self.basis_transform(basis)

        return config, basis

    def __len__(self):
        if self.train:
            return len(self.train_data)
        else:
            return len(self.test_data)

    def _check_exists(self):
        if self.train:
            return os.path.exists(
                os.path.join(
                    self.root,
                    self.processed_folder,
                    self.training_file
                ))
        else:
            return os.path.exists(
                os.path.join(
                    self.root,
                    self.processed_folder,
                    self.test_file
                ))

    def load(self):
        if self.train:
            path = os.path.join(self.root, self.processed_folder,
                                self.training_file)
            self.train_data, self.train_basis = torch.load(path)
        else:
            path = os.path.join(self.root, self.processed_folder,
                                self.test_file)
            self.test_data, self.test_basis = torch.load(path)

    def generate(self):
        raise NotImplementedError

    def gen(self):
        try:
            os.makedirs(os.path.join(self.root, self.processed_folder))
        except OSError as e:
            if e.errno == errno.EEXIST:
                pass
            else:
                raise

        if self.train:
            self.train_data, self.train_basis = self.generate()
            path = os.path.join(self.root,
                                self.processed_folder,
                                self.training_file)
            torch.save((self.train_data, self.train_basis), path)
        else:
            self.test_data, self.test_basis = self.generate()
            path = os.path.join(self.root,
                                self.processed_folder,
                                self.test_file)
            torch.save((self.test_data, self.test_basis), path)


class RandPauli(DataBase):
    """random pauli operator
    """

    def __init__(self, **kwargs):
        self.nbasis = kwargs.pop('nbasis') if 'nbasis' in kwargs else 100
        self.itr = kwargs.pop('itr') if 'itr' in kwargs else 1000
        self.burn = kwargs.pop('burn') if 'burn' in kwargs else 500
        self.thin = kwargs.pop('thin') if 'thin' in kwargs else 1

        super(RandPauli, self).__init__(kwargs)

    def generate(self):
        data = []
        basis = []
        for _ in range(self.nbasis):
            ops = MBOp(choice([sigmax, sigmay, sigmaz]) for i in range(self.n))
            _state = ops.invtrans(self.state)
            sampler = STMetropolis(
                proposal=lambda x: abs(_state[bin(x)]) ** 2, size=self.size)
            data.extend(sampler.sample(
                itr=self.itr, burn=self.burn, thin=self.thin))
            basis.extend(torch.FloatTensor(ops.params()).resize_(2 * self.n)
                         for i in range(len(sampler.collector)))
        return data, basis


class FixedPauli(DataBase):
    """Fixed pauli operator"""

    def __init__(self, **kwargs):
        kwargs['prefix'] = 'fixed_pauli'
        self.nbasis = kwargs.pop('nbasis') if 'nbasis' in kwargs else 100
        self.itr = kwargs.pop('itr') if 'itr' in kwargs else 1000
        self.burn = kwargs.pop('burn') if 'burn' in kwargs else 500
        self.thin = kwargs.pop('thin') if 'thin' in kwargs else 1

        if 'basis' in kwargs:
            self.basis = kwargs.pop('basis')
        else:
            self.basis = None

        super(FixedPauli, self).__init__(kwargs)

    def generate(self):
        if self.basis is None:
            self.basis = [sigmaz for i in range(self.n)]
        ops = MBOp(self.basis)
        _state = ops.invtrans(self.state)
        sampler = PseudoRandom(_state * _state.conj(), size=self.size)
        # sampler = STMetropolis(
        #     proposal=lambda x: abs(_state[bin(x)]) ** 2, size=self.size)
        # data = list(sampler.sample(
        #     itr=self.itr, burn=self.burn, thin=self.thin))
        data = list(sampler.sample(itr=self.itr))
        basis = list(torch.FloatTensor(ops.params()).resize_(2 * self.n)
                     for i in range(len(sampler.collector)))
        return data, basis
