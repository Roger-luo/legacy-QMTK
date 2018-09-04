from vmc.lattice import Chain, Square
import scipy.sparse as sp
import unittest
from vmc.utils import *
import torch
import torch.nn as nn
from torch.autograd import Variable


def J1J2(lattice, J=(1, 0.5)):
    h = J[0] * (nlocal(sigmax, lattice, 1) +
                nlocal(sigmay, lattice, 1) +
                nlocal(sigmaz, lattice, 1)) + \
        J[1] * (nlocal(sigmax, lattice, 2) +
                nlocal(sigmay, lattice, 2) +
                nlocal(sigmaz, lattice, 2))
    return h


def TFI(lattice, mag=1.0):
    sum_sigmax = kronsum(sigmax for k in lattice.grid(nbr=0))
    sum_sigmaz = nlocal(sigmaz, lattice, 1)
    return - mag * sum_sigmax - sum_sigmaz


def assertEqualSparse(self, A, B):
    self.assertEqual((A != B).nnz, 0)


class FakeModel(nn.Module):
    """Fake Model"""

    def __init__(self, ham):
        super(FakeModel, self).__init__()
        eigs, vecs = ed(ham.mat())
        self.ground = eigs[0]
        self.state = torch.Tensor(vecs[:, 0], dtype='complex128')
        self.state = self.state / torch.norm(self.state) ** 2
        self.state = Variable(self.state)

    def forward(self, x):
        if not isinstance(x, Variable):
            raise ValueError('Inputs should be torch.autograd.Variable')
        return self.state[bin(x.data)]


class TestTools(unittest.TestCase):
    def _test_chain(self, op, k):
        gen = nlocal(op, Chain(3, pbc=True), k)
        exact = sp.kron(sp.kron(op, op), iden) + \
            sp.kron(sp.kron(op, iden), op) + \
            sp.kron(sp.kron(iden, op), op)
        self.assertEqual((gen != exact).nnz, 0)

    def _test_square(self, op, k):
        gen = nlocal(op, Square((2, 2), pbc=False), k)
        if k is 1:
            exact = sp.kron(sp.kron(sp.kron(op, op), iden), iden) + \
                sp.kron(sp.kron(sp.kron(iden, iden), op), op) + \
                sp.kron(sp.kron(sp.kron(op, iden), op), iden) + \
                sp.kron(sp.kron(sp.kron(iden, op), iden), op)
        elif k is 2:
            exact = sp.kron(sp.kron(sp.kron(op, iden), iden), op) + \
                sp.kron(sp.kron(sp.kron(iden, op), op), iden)
        self.assertEqual((gen != exact).nnz, 0)

    def test_nlocal(self):
        for k in range(1, 3):
            self._test_chain(sigmax, k)
            self._test_chain(sigmay, k)
            self._test_chain(sigmaz, k)
        # test square
        for k in range(1, 3):
            self._test_square(sigmax, k)
            self._test_square(sigmay, k)
            self._test_square(sigmaz, k)
        # test J1J2
        gen = J1J2(Chain(3, pbc=True))

        def local(op, J=(1.0, 0.5)):
            return J[0] * (kronprod(op, op, iden) +
                           kronprod(iden, op, op) +
                           kronprod(op, iden, op)) + \
                J[1] * (kronprod(op, iden, op) +
                        kronprod(op, op, iden) +
                        kronprod(iden, op, op))
        exact = local(sigmax) + local(sigmay) + local(sigmaz)
        self.assertEqual((gen != exact).nnz, 0)

    def test_kronprod(self):
        test = kronprod(sigmax, sigmax, iden)
        exact = sp.kron(sp.kron(sigmax, sigmax), iden)
        self.assertEqual((test != exact).nnz, 0)

    def test_tfi(self):
        test = TFI(Chain(3, pbc=True), mag=1.0)
        exact = - kronsum(sigmax, sigmax, sigmax) -\
            kronprod(sigmaz, sigmaz, iden) - \
            kronprod(sigmaz, iden, sigmaz) - \
            kronprod(iden, sigmaz, sigmaz)
        self.assertEqual((test != exact).nnz, 0)

    def test_kronsum(self):
        test = kronsum(sigmax, sigmax, iden)
        exact = sp.kronsum(
            sp.kronsum(sigmax, sigmax), iden)
        self.assertEqual((test != exact).nnz, 0)


if __name__ == '__main__':
    unittest.main()
