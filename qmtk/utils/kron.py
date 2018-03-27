import types
import scipy.sparse as sp
from functools import wraps

__all__ = ['prod', 'sum']


def matrix2gen(func):
    @wraps(func)
    def wrapper(*args, **params):
        if len(args) is 1:
            if isinstance(args[0], types.GeneratorType):
                gen = args[0]
            elif isinstance(args[0], sp.spmatrix):
                return args[0]
            else:
                try:
                    gen = iter(args[0])
                except Exception:
                    raise TypeError('incompatible type of argument')
        else:
            gen = iter(args)
        return func(gen)
    return wrapper


@matrix2gen
def prod(gen):
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


@matrix2gen
def sum(gen):
    """
    Kronnecker sum

    example:
    """
    res = next(gen)
    for each in gen:
        res = sp.kronsum(res, each)
    return res
