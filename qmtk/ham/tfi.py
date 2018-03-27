from .core import SpinHBase


class TFI(SpinHBase):
    """traverse field Ising Model
    """

    def load_mag(self, kwargs):
        self.mag = kwargs.pop('mag')

    def nnz_iter(self, rhs):
        for i in self.lattice.grid(nbr=0):
            rhs[i] = self.flip(rhs[i])
            yield rhs, - self.mag
            rhs[i] = self.flip(rhs[i])
        sigmaz = 0.0
        for i, j in self.lattice.grid(nbr=1):
            sigmaz += rhs[i] * rhs[j]
        yield rhs, - sigmaz
