from vmc.data import FixedBasis
from vmc.ham import J1J2, TFI
from vmc.utils import ed


def generate_j1j2(n, size):
    print('generating J1-J2 on %s' % n)
    h = J1J2(length=4, pbc=True)
    _, states = ed(h.mat())

    for i in range(5):
        FixedBasis(states[:, i], ham=h, len=size, level=i)


def generate_tfi(n, size):
    print('generating TFI')

    h = TFI(length=4, pbc=True)
    _, states = ed(h.mat())

    for i in range(5):
        FixedBasis(states[:, i], ham=h, len=size, level=i)


if __name__ == '__main__':

    for i in range(4, 11):
        generate_tfi(i, 200000)
        generate_j1j2(i, 200000)

print('finished')
