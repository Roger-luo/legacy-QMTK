from random import choice

from vmc.basis import *
from vmc.utils import ground, bin
from vmc.sampler import STMetropolis
from vmc.ham import isham

import torch
import torch.utils.data as data
import errno
import _pickle as pkl
import os


class TOMO(data.Dataset):
    """generated tomography dataset
    """

    raw_folder = 'raw'
    processed_folder = 'processed'

    def __init__(self, root, prefix=None, train=True, hamiltonian=None,
                 transform=None, basis_transform=None,
                 nbasis=1000, itr=1000, burn=500, thin=1):
        self.root = os.path.expanduser(root)
        self.transform = transform
        self.basis_transform = basis_transform
        self.train = train

        if prefix is None:
            self.training_file = 'training.tomo'
            self.test_file = 'test.tomo'
        else:
            self.training_file = prefix + '_training.tomo'
            self.test_file = prefix + '_test.tomo'

        if self._check_exists():
            print("find data, start loading")
            if self.train:
                path = os.path.join(self.root, self.processed_folder,
                                    self.training_file)
                with open(path, 'rb') as f:
                    self.train_data, self.train_basis = pkl.load(f)
            else:
                path = os.path.join(self.root, self.processed_folder,
                                    self.test_file)
                with open(path, 'rb') as f:
                    self.test_data, self.test_basis = pkl.load(f)
        elif isham(hamiltonian):
            print("cannot find data, start generating")
            if self.train:
                self.train_data, self.train_basis = \
                    self.gen(hamiltonian, itr, nbasis, burn, thin)
            else:
                self.test_data, self.test_basis = \
                    self.gen(hamiltonian, itr, nbasis, burn, thin)
            self.save_gen()
        else:
            raise RuntimeError('Dataset not found.' +
                               ' You can input a hamiltonian to generate it')

    def __getitem__(self, index):
        if self.train:
            config, basis = self.train_data[index], self.train_basis[index]
        else:
            config, basis = self.train_data[index], self.train_basis[index]

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

    def gen(self, ham, itr=1000, nbasis=1000, burn=500, thin=1):
        _, state = ground(ham)
        n = ham.lattice.numel()

        try:
            # os.makedirs(os.path.join(self.root, self.raw_folder))
            os.makedirs(os.path.join(self.root, self.processed_folder))
        except OSError as e:
            if e.errno == errno.EEXIST:
                pass
            else:
                raise

        data = []
        basis = []
        for _ in range(nbasis):
            ops = MBOp(choice([sigmax, sigmay, sigmaz]) for i in range(n))
            _state = ops.invtrans(state)
            sampler = STMetropolis(
                proposal=lambda x: abs(_state[bin(x)]) ** 2, size=ham.size)
            data.extend(sampler.sample(itr=itr, burn=burn, thin=thin))
            basis.extend(torch.FloatTensor(ops.params()).resize_(2 * n)
                         for i in range(len(sampler.collector)))
        return data, basis

    def save_gen(self):
        if self.train:
            filepath = os.path.join(self.root,
                                    self.processed_folder,
                                    self.training_file)
            with open(filepath, 'wb') as f:
                pkl.dump((self.train_data, self.train_basis), f)
        else:
            filepath = os.path.join(self.root,
                                    self.processed_folder,
                                    self.test_file)
            with open(filepath, 'wb') as f:
                pkl.dump((self.test_data, self.test_basis), f)


class FixedTOMO(data.Dataset):
    """generated tomography dataset with fixed basis
    """

    raw_folder = 'raw'
    processed_folder = 'processed'

    def __init__(self, root, prefix=None, train=True, hamiltonian=None,
                 basis=None,
                 transform=None, basis_transform=None,
                 nbasis=1000, itr=1000, burn=500, thin=1):
        self.root = os.path.expanduser(root)
        self.transform = transform
        self.basis_transform = basis_transform
        self.train = train
        self.basis = basis

        if prefix is None:
            self.training_file = 'training.tomo'
            self.test_file = 'test.tomo'
        else:
            self.training_file = prefix + '_training.tomo'
            self.test_file = prefix + '_test.tomo'

        if self._check_exists():
            print("find data, start loading")
            if self.train:
                path = os.path.join(self.root, self.processed_folder,
                                    self.training_file)
                with open(path, 'rb') as f:
                    self.train_data, self.train_basis = pkl.load(f)
            else:
                path = os.path.join(self.root, self.processed_folder,
                                    self.test_file)
                with open(path, 'rb') as f:
                    self.test_data, self.test_basis = pkl.load(f)
        elif isham(hamiltonian):
            print("cannot find data, start generating")
            if self.train:
                self.train_data, self.train_basis = \
                    self.gen(hamiltonian, itr, nbasis, burn, thin)
            else:
                self.test_data, self.test_basis = \
                    self.gen(hamiltonian, itr, nbasis, burn, thin)
            self.save_gen()
        else:
            raise RuntimeError('Dataset not found.' +
                               ' You can input a hamiltonian to generate it')

    def __getitem__(self, index):
        if self.train:
            config, basis = self.train_data[index], self.train_basis[index]
        else:
            config, basis = self.train_data[index], self.train_basis[index]

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

    def gen(self, ham, itr=1000, nbasis=1000, burn=500, thin=1):
        _, state = ground(ham)
        n = ham.lattice.numel()

        try:
            # os.makedirs(os.path.join(self.root, self.raw_folder))
            os.makedirs(os.path.join(self.root, self.processed_folder))
        except OSError as e:
            if e.errno == errno.EEXIST:
                pass
            else:
                raise

        data = []
        basis = []
        if self.basis is not None:
            ops = MBOp(self.basis)
        else:
            ops = MBOp(sigmaz for i in range(n))
        for _ in range(nbasis):
            _state = ops.invtrans(state)
            sampler = STMetropolis(
                proposal=lambda x: abs(_state[bin(x)]) ** 2, size=ham.size)
            data.extend(sampler.sample(itr=itr, burn=burn, thin=thin))
            basis.extend(torch.FloatTensor(ops.params()).resize_(2 * n)
                         for i in range(len(sampler.collector)))
        return data, basis

    def save_gen(self):
        if self.train:
            filepath = os.path.join(self.root,
                                    self.processed_folder,
                                    self.training_file)
            with open(filepath, 'wb') as f:
                pkl.dump((self.train_data, self.train_basis), f)
        else:
            filepath = os.path.join(self.root,
                                    self.processed_folder,
                                    self.test_file)
            with open(filepath, 'wb') as f:
                pkl.dump((self.test_data, self.test_basis), f)
