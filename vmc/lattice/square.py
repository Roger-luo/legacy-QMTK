from .base import LatticeBase


class Square(LatticeBase):
    """square lattice"""

    def __init__(self, *args, **kwargs):
        super(Square, self).__init__('Square', *args, **kwargs)

    def grid(self, nbr=None):
        if nbr is None or nbr is 0:
            for i in range(self.shape[0]):
                for j in range(self.shape[1]):
                    yield i, j
        elif nbr is 1:
            if self.pbc:
                for j in range(self.shape[1]):
                    for i in range(self.shape[0]):
                        yield (i, j), ((i + 1) % self.shape[0], j)
                        yield (i, j), (i, (j + 1) % self.shape[1])
            else:
                for j in range(self.shape[1]):
                    for i in range(self.shape[0] - 1):
                        yield (i, j), (i + 1, j)
                for i in range(self.shape[0]):
                    for j in range(self.shape[1] - 1):
                        yield (i, j), (i, j + 1)
        elif nbr is 2:
            if self.pbc:
                for j in range(self.shape[1]):
                    for i in range(self.shape[0]):
                        yield (i, j), \
                            ((i + 1) % self.shape[0],
                                (j + 1) % self.shape[1])
                        yield (i, j), \
                            ((i + 1) % self.shape[0],
                                (j - 1) % self.shape[1])
            else:
                for j in range(self.shape[1] - 1):
                    for i in range(self.shape[0] - 1):
                        yield (i, j), (i + 1, j + 1)
                for j in range(self.shape[1] - 1):
                    for i in range(self.shape[0] - 1):
                        yield (i + 1, j), (i, j + 1)

