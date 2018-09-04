import torch

import scipy.sparse as sp
from scipy.sparse.dok import _prod
from scipy.sparse.linalg import eigsh
import numpy as np

from .consts import iden
from .decorators import parse_multimatrix

from torch.autograd import Variable
from vmc.configs import IterateAll

from collections import Iterable

__all__ = [
    'bin',
    'shift',
    'randspin',
    'ed',
    'kronprod',
    'kronsum',
    'hash_grid',
    'nlocal',
    'eloc',
    'exact_energy',
    'norm',
    'normalize',
    'ground',
]


def bin(x):
    flatten_x = x.view(x.numel())
    # print(storage)
    ret = 0
    for i, each in enumerate(flatten_x):
        ret += (each + 1) / 2 * 2**i
    return int(ret)


def shift(tensor):
    storage = tensor.storage()
    for i, each in enumerate(storage):
        if each == 1:
            storage[i] = -1
        else:
            storage[i] = 1
            break
    return tensor


# TODO:
#   * this does not actually needs torch?
#     make it work for non-torch envs
def randspin(size, states=2):
    if isinstance(size, int):
        ret = torch.FloatTensor(size)
    elif isinstance(size, tuple):
        ret = torch.FloatTensor(*size)
    elif isinstance(size, list):
        size = tuple(size)
        ret = torch.FloatTensor(*size)
    else:
        raise TypeError('Invalid Type')
    ret = 2 * ret.random_(0, to=2) - 1
    return ret


def ed(mat, k=1):
    """
    Exact diagnolization
    """
    if _prod(mat.shape) > 20:
        if isinstance(mat, sp.spmatrix):
            mat = mat.toarray()
        return np.linalg.eigh(mat)
    else:
        return eigsh(mat, k, which='SA')


@parse_multimatrix
def kronprod(gen):
    """
    Kronnecker product
        calculates multiple inputs' kronnecker product
    Example:
    like: sigmax \otimes sigmax \otimes iden
    >>> kronprod(sigmax, sigmax, iden)
    or you can use list comprehension (or a generator)
    >>> kronprod(sigmax for i in range(4)) # product of four sigmax
    """
    res = sp.kron(next(gen), next(gen))
    for each in gen:
        res = sp.kron(res, each)
    return res


@parse_multimatrix
def kronsum(gen):
    """
    Kronnecker sum

    example:
    """
    res = next(gen)
    for each in gen:
        res = sp.kronsum(res, each)
    return res


def hash_grid(index, size):
    if isinstance(index, int) and isinstance(size, int):
        return index
    elif isinstance(index, tuple) and isinstance(size, tuple):
        strides = [1]
        for i in size[0: -1]:
            strides.append(i)
        return sum(inds * j for inds, j in zip(index, strides))
    else:
        raise TypeError('index and size should be tuple')


# TODO: lattice API may need to change to support k-local
# hamiltonians, eg. for i, j, k in lattice.grid(nbr=[1, 2])
def nlocal(op, lattice, nbr):
    """
    construct n-local hamiltonian with given operator

    params:
    - op: scipy.sparse matrix, eg. lil_matrix, csc_matrix
    - lattice: an instance of lattice
    - nbr: order of neighbor, must be greater than 0,
            eg. 1 is the nearest neighbor
    """
    h = sp.lil_matrix((2 ** lattice.numel(), 2 **
                       lattice.numel()), dtype='complex128')
    for inds in lattice.grid(nbr=nbr):
        mats = []
        for k in lattice.grid(nbr=0):
            if k in inds:
                mats.append(op)
            else:
                mats.append(iden)
        ret = mats[0]
        for ind in range(1, len(mats)):
            ret = sp.kron(ret, mats[ind])
        h += ret
    return h


def eloc(x, ansatz, hamiltonian):
    ret = sum(val * ansatz(Variable(config))
              for config, val in hamiltonian.nnz(x))
    return ret / ansatz(Variable(x))


def exact_energy(ansatz, hamiltonian):
    energy = sum(torch.abs(ansatz(Variable(config))) ** 2 * eloc(config)
                 for config in IterateAll(size=hamiltonian.size))
    return energy


def norm(state):
    from math import sqrt

    if isinstance(state, np.ndarray):
        return np.linalg.norm(state)
    elif torch.is_tensor(state):
        return torch.norm(state)
    elif isinstance(state, Iterable):
        return sqrt(sum(abs(each) ** 2 for each in state))


def normalize(state):
    from math import sqrt

    if isinstance(state, np.ndarray):
        return state / np.linalg.norm(state)
    elif torch.is_tensor(state):
        return state / torch.norm(state)
    elif isinstance(state, Iterable):
        n = sqrt(sum(abs(each) ** 2 for each in state))
        return [each / n for each in state]
    else:
        raise TypeError("state should be numpy.array"
                        "or torch.tensor or iterable "
                        "got %s" % type(state))


def ground(hamiltonian):
    """gets hamiltonian's ground state
    """
    from vmc.ham import isham
    if isham(hamiltonian):
        h = hamiltonian.mat()

    energy, state = ed(h)
    return energy[0], state[:, 0]

