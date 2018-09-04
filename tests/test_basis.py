import unittest
import numpy as np
from numpy.random import rand
from vmc.basis import BlochOp, MBOp


def checkequal(m, l):
    return np.linalg.norm(m - np.array(l)) < 1e-15


class TestBlochOp(unittest.TestCase):

    def test_pauli(self):
        sigmax = BlochOp(np.pi / 4, 0)
        sigmay = BlochOp(np.pi / 4, np.pi / 2)
        sigmaz = BlochOp(0, 1)

        self.assertTrue(checkequal(sigmax.mat(), [[0, 1], [1, 0]]))
        self.assertTrue(checkequal(sigmay.mat(), [[0., -1.j], [1.j, 0.]]))
        self.assertTrue(checkequal(sigmaz.mat(), [[1., 0.], [0., -1.]]))

        self.assertTrue(checkequal(sigmax.eig(
            0), [1 / np.sqrt(2), 1 / np.sqrt(2)]))
        self.assertTrue(checkequal(sigmax.eig(
            1), [-1 / np.sqrt(2), 1 / np.sqrt(2)]))

        self.assertTrue(checkequal(sigmay.eig(
            0), [1 / np.sqrt(2), 1.j / np.sqrt(2)]))
        self.assertTrue(checkequal(sigmay.eig(
            1), [1.j / np.sqrt(2), 1 / np.sqrt(2)]))

        self.assertTrue(checkequal(sigmaz.eig(0), [1, 0]))
        self.assertTrue(checkequal(sigmaz.eig(1), [0, 1]))

        self.assertTrue(checkequal(
            sigmax.invtrans(sigmaz.eig(1)), sigmax.eig(1)))
        self.assertTrue(checkequal(
            sigmax.invtrans(sigmaz.eig(0)), sigmax.eig(0)))

        self.assertTrue(checkequal(
            sigmay.invtrans(sigmaz.eig(1)), sigmay.eig(1)))
        self.assertTrue(checkequal(
            sigmay.invtrans(sigmaz.eig(0)), sigmay.eig(0)))

        self.assertTrue(checkequal(
            sigmaz.invtrans(sigmaz.eig(1)), sigmaz.eig(1)))
        self.assertTrue(checkequal(
            sigmaz.invtrans(sigmaz.eig(0)), sigmaz.eig(0)))

        self.assertTrue(checkequal(sigmaz.trans(sigmaz.eig(0)), sigmaz.eig(0)))
        self.assertTrue(checkequal(sigmaz.trans(sigmaz.eig(1)), sigmaz.eig(1)))

        self.assertTrue(checkequal(sigmax.trans(sigmaz.eig(0)), sigmax.eig(0)))
        self.assertTrue(checkequal(sigmax.trans(sigmaz.eig(1)), sigmax.eig(1)))

        self.assertTrue(checkequal(sigmay.trans(sigmaz.eig(0)), sigmay.eig(0)))
        self.assertTrue(checkequal(sigmay.trans(sigmaz.eig(1)), sigmay.eig(1)))

    def test_rand(self):
        opa = BlochOp(rand(), rand())
        sigmaz = BlochOp(0, 1)

        self.assertTrue(checkequal(opa.trans(sigmaz.eig(0)), opa.eig(0)))
        self.assertTrue(checkequal(opa.trans(sigmaz.eig(1)), opa.eig(1)))


class TestMBOp(unittest.TestCase):

    def test_init(self):
        MBOp(2, params=[(np.pi / 4, 0), (0, 1)])
        MBOp(2, p=[(np.pi / 4, 0), (0, 1)])
        MBOp(2)

    def test_state(self):
        # sigmax \otimes sigmaz
        op = MBOp(2, params=[(np.pi / 4, 0), (0, 1)])
        self.assertTrue(checkequal(op.mat(), [[0, 0, 1, 0], [0, 0, 0, -1],
                                              [1, 0, 0, 0], [0, -1, 0, 0]]))


if __name__ == '__main__':
    unittest.main()
