import numpy as np
from types import GeneratorType
from scipy.sparse import lil_matrix
from vmc.utils import kronprod, alias


__all__ = [
    'OpBase',
    'BlochOp',
    'MBOp',
    'sigmax',
    'sigmay',
    'sigmaz',
]


class OpBase(object):
    """base type for quantum operators"""

    def __init__(self):
        super(OpBase, self).__init__()

    def __str__(self):
        return 'Operator'

    def __repr__(self):
        return self.__str__()

    def __list__(self):
        """ list of operator elements (on sigma z basis).

        this methods should be overloaded and returns a list,
        if this operator's elements on sigma z basis has exact form
        """
        raise NotImplementedError

    def __eigen__(self):
        """ eigen vectors (on sigma z basis).

        this method should be overloaded and returns a list,
        if this operator's eigen vectors has analytical form
        """
        raise NotImplementedError

    def __u__(self):
        """ transformation matrix to sigma z basis.

        this method should be overloaded and returns a list,
        if this operator's linear space has analytical form
        """
        raise NotImplementedError

    def __invu__(self):
        """inverse of transformation matrix to sigma z basis.

        this method should be overloaded and returns a list,
        if this operator's linear space has analytical form
        """
        raise NotImplementedError

    def mat(self):
        return np.array(self.__list__(), dtype='complex128')

    def spmat(self):
        return lil_matrix(self.__list__(), dtype='complex128')

    def eig(self, i):
        return np.array(self.__eigen__(i))

    def speig(self, i):
        return lil_matrix(self.__eigen__(i))

    def u(self):
        return np.array(self.__u__())

    def invu(self):
        return np.array(self.__invu__())

    def spu(self):
        return lil_matrix(self.__u__())

    def spinvu(self):
        return lil_matrix(self.__invu__())

    def sptrans(self, state):
        return self.spu().dot(state)

    def spinvtrans(self, state):
        return self.spinvu().dot(state)

    def trans(self, state):
        """transform state on this operator's basis to sigmaz

        transform a state on basis given `op` basis to sigma_z by doing

        >>> matmul(op.u(), state)
        """
        return np.matmul(self.u(), state)

    def invtrans(self, state):
        """tranform state on sigmaz to this operator's basis

        transform a state on sigma_z by doing

        >>> matmul(op.invu(), state)
        """
        return np.matmul(self.invu(), state)


class BlochOp(OpBase):
    """single particle operator on bloch sphere

    This class offers methods related to operators on bloch sphere
    """

    def __init__(self, theta, phi, name=None):
        super(BlochOp, self).__init__()
        self.theta = theta
        self.phi = phi
        if name is None:
            self.name = 'Bloch Op (theta=%s, phi=%s)' % (theta, phi)
        else:
            self.name = name

    def __str__(self):
        return self.name

    def __list__(self):
        t = self.theta
        p = self.phi
        return [[np.cos(2 * t), np.sin(2 * t) * np.exp(-1.j * p)],
                [np.sin(2 * t) * np.exp(1.j * p), -np.cos(2 * t)]]

    def __eigen__(self, i):
        t = self.theta
        p = self.phi
        if i is 0:
            return [np.cos(t), np.sin(t) * np.exp(1.j * p)]  # 1
        else:
            return [- np.sin(t) * np.exp(-1.j * p), np.cos(t)]  # -1

    def __u__(self):
        t = self.theta
        p = self.phi
        return [[np.cos(t), - np.sin(t) * np.exp(-1.j * p)],
                [np.sin(t) * np.exp(1.j * p), np.cos(t)]]

    def __invu__(self):
        t = self.theta
        p = self.phi
        return [[np.cos(t), np.sin(t) * np.exp(-1.j * p)],
                [-np.sin(t) * np.exp(1.j * p), np.cos(t)]]


class MBOp(OpBase):
    """many body operator.

    Examples:

        basis params should be an iteratable object, both list and tuple is OK
        >>> MBOp(3, params=((1, 0), (1, 0), (1, 0)))
        Many-body Basis
        >>> MBOp(3, params=[(1, 0), (1, 0), (1, 0)])
        Many-body Basis
    """

    @alias(params='p')
    def __init__(self, *args, **kwargs):
        super(MBOp, self).__init__()

        self.ops = []

        def convert_gen(l):
            for each in l:
                if isinstance(each, tuple):
                    self.ops.append(BlochOp(*each))
                elif isinstance(each, BlochOp):
                    self.ops.append(each)
                else:
                    raise TypeError("expected tuple or BlochOp"
                                    ", got %s" % type(each))

        def init_ops(x):
            if isinstance(x, int):
                self.ops = [BlochOp(0, 1) for i in range(x)]
            elif isinstance(x, BlochOp):
                self.ops = [x]
            elif isinstance(x, tuple):
                self.ops = [BlochOp(*x)]
            elif isinstance(x, GeneratorType):
                convert_gen(x)
            elif isinstance(x, list):
                convert_gen(x)
            else:
                return False
            return True

        if args:
            if len(args) is 1:
                init_ops(args[0])
            else:
                convert_gen(args)
        elif not self.ops and 'params' in kwargs:
            p = kwargs.pop('params')
            if not init_ops(p):
                convert_gen(p)
        else:
            raise TypeError('Basis definition needed')
        self.n = len(self.ops)

    def __str__(self):
        prefix = 'Many Body Basis:\n'
        basis_name = '\n'.join(str(i) + ': ' +
                               str(each) for i, each in enumerate(self.ops))
        return prefix + basis_name

    def __repr__(self):
        return '\n'.join(str(i) + ': ' +
                         str(each) for i, each in enumerate(self.ops))

    def mat(self):
        return self.spmat().toarray()

    def spmat(self):
        return kronprod(each.spmat() for each in self.ops)

    def spu(self):
        return kronprod(each.u() for each in self.ops)

    def spinvu(self):
        return kronprod(each.invu() for each in self.ops)

    def u(self):
        return self.spu().toarray()

    def invu(self):
        return self.spinvu().toarray()

    # convert sptrans to trans or use u?
    # benchmark needed

    def trans(self, state):
        return np.matmul(self.u(), state)

    def invtrans(self, state):
        return np.matmul(self.invu(), state)

    def params(self):
        return [[each.theta, each.phi] for each in self.ops]


sigmax = BlochOp(np.pi / 4, 0, name='sigma x')
sigmay = BlochOp(np.pi / 4, np.pi / 2, name='sigma y')
sigmaz = BlochOp(0, 1, name='sigma z')
