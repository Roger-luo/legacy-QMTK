import torch
import numpy as np
import os
from tables import *
import h5py
import torch.utils.data as data

from vmc.utils import bin

__all__ = [
    'STDS',
]


class STDS(data.Dataset):
    """Simulated tomography data set

    Params:
    ham: hamiltonian name
    lattice: lattice name
    shape: shape of the lattice
    pbc: periodic boundary condition
    exact: is generated from exact solution
    """

    root = 'data'

    def __init__(self, ham, lattice, length, pbc=True, level=0, exact=True,
                 transform=None, basis_transform=None, train=True, size=1000):
        super(STDS, self).__init__()
        self.transform = transform
        self.basis_transform = basis_transform
        self.train = train
        path = os.path.join(self.root, ham, 'check.h5')
        h5file = open_file(path)
        table = h5file.root.measure
        prefix = None
        for each in table:
            flag = all([
                each['lattice'].decode() == lattice,
                each['shape'][0] == length,
                each['level'] == level,
                each['pbc'] == pbc,
                each['exact'] == exact,
            ])
            if flag:
                prefix = each['data'].decode()
        h5file.close()
        if prefix is None:
            raise ValueError('cannot find this data')

        filename = prefix + '.h5'
        filepath = os.path.join(self.root, ham, filename)
        with h5py.File(filepath, 'r') as f:
            self.data = torch.FloatTensor(f['data/configs'][:size])
            self.basis = torch.FloatTensor(f['data/basis'][:size])
            self.state = np.array(f['data/state'])
        train_size = int(0.6 * size)
        # test_size = int(0.4 * len(self.data))
        self.train_data = self.data[:train_size]
        self.test_data = self.data[train_size:]
        self.train_basis = self.basis[:train_size]
        self.test_basis = self.basis[train_size:]

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

    def check(self):
        p1 = self.state * self.state.conj()
        p2 = np.zeros(*self.state.shape)
        for each in self.train_data:
            p2[bin(each)] += 1
        p2 /= np.linalg.norm(p2, ord=1)
        print('nornmalized frequency sum (should be 1): %s' % sum(p2))
        print('distance to exact (should be 0): %s' % np.linalg.norm(p2 - p1))
