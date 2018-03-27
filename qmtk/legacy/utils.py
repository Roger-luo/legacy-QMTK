import numpy as np


def n2spin(n, shape):
    """convert a integer to spin.
    """
    size = np.prod(shape)
    spin = np.linspace(0, size - 1, size, dtype=int)

    def shift(i):
        return (n >> i) & 1

    shift = np.vectorize(shift)
    spin = shift(spin)
    spin.resize(shape)
    return spin


def spin2n(spin):
    """convert spin to a integer
    """
    flatten = spin.view()
    flatten.resize(flatten.size)

    ret = 0
    for i, each in enumerate(flatten):
        ret += each * 2 ** i
    return int(ret)
