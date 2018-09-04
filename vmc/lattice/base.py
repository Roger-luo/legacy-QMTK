from collections import Iterable
from scipy.sparse.dok import _prod


class LatticeBase(object):
    """lattice base

    Lattice type can be init by the following:

    LatticeBase(2, 3, pbc=True (optional), other parameters...)
    LatticeBase(length=3, pbc=True (optional), other parameters...)
    LatticeBase(shape=(2, 2), pbc=True (optional), other parameters...)
    """

    def __init_shape(self, args, kwargs):
        if args:
            if all(isinstance(n, int) for n in args):
                self.shape = list(args)
                self.dim = len(args)
            else:
                raise TypeError("input shape must be int")
        elif 'length' in kwargs:
            length = kwargs.pop('length')
            if isinstance(length, int):
                self.shape = [length]
                self.dim = 1
            else:
                raise TypeError('length should be int not %s' % type(length))
        elif 'shape' in kwargs:
            shape = kwargs.pop('shape')
            if isinstance(shape, int):
                self.shape = [shape]
                self.dim = 1
            elif isinstance(shape, tuple):
                self.shape = list(shape)
                self.dim = len(shape)
            elif isinstance(shape, list):
                self.shape = shape
                self.dim = len(shape)
            elif isinstance(shape, Iterable) \
                    and all(isinstance(n, int) for n in shape):
                self.shape = list(shape)
                self.dim = len(self.shape)
            else:
                raise TypeError("shape should be int, tuple, list"
                                " or iterable not %s" % type(shape))
        else:
            raise TypeError("Missing shape information")

    def __init_pbc(self, kwargs):
        if 'pbc' in kwargs:
            pbc = kwargs.pop('pbc')
            if isinstance(pbc, bool):
                self.pbc = pbc
            else:
                raise TypeError('keyword pbc only take True or False')
        else:
            self.pbc = False

    def __init__(self, name, *args, **kwargs):
        super(LatticeBase, self).__init__()
        self.name = name
        self.__init_shape(args, kwargs)
        self.__init_pbc(kwargs)
        if kwargs:
            self.params = kwargs
        else:
            self.params = None

    def __str__(self):
        ret = '%s: %s' % (self.name, tuple(self.shape))
        if self.pbc:
            ret += '(periodic bound)'
        if self.params is not None:
            ret += '\n'
            ret += str(self.params)
        return ret

    def size(self):
        return self.shape

    def grid(self, nbr=None):
        """
        grid iterator

        params:
            nbr: int or None, neighbors, default: None

        example:
        lattice = Chain(5, pbc=True)
        for i, j, k in lattice.grid(nbr=1):
            print(i, j, k)

        >>> 0 1
        >>> 1 2
        >>> 2 3
        >>> 3 4
        >>> 4 0
        """
        pass

    def numel(self):
        return _prod(self.shape)

    def __len__(self):
        return self.numel()
