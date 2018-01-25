from collections import Iterable


__all__ = [
    'Union',
    'Iterator',
    'List',
    'Tuple',
]


class Union(type):
    """Union type.

    Example:
        Union is a metaclass which combines different types in type checks
        >>> isinstance(2, Union(int, float))
        True
        >>> isinstance(1.2, Union(int, float))
        True

        Types in a union will be unique, which means
        Union(int, int, float) equals to Union(int, float)

        >>> isinstance(2, Union(int, int, float))
        True
        >>> isinstance(1.2, Union(int, int, float))
        True
    """

    def __init__(self, *types):
        self.types = set(types)

    def __new__(mcls, *types):
        name = 'Union{'
        if len(types) < 5:
            type_names = [each.__name__ for each in types]
            name += ','.join(type_names) + '}'
        else:
            name += ','.join([types[0].__name__, '...',
                              types[-1].__name__]) + '}'
        cls = super(Union, mcls).__new__(mcls, name, (object, ), {})
        return cls

    def __str__(cls):
        name = 'Union'
        type_names = [each.__name__ for each in cls.types]
        if len(cls.types) < 5:
            name += '{' + ','.join(type_names) + '}'
        else:
            name += ':\n'
            name += '\n'.join(['  ' + each for each in type_names])
        return name

    def __instancecheck__(cls, instance):
        return any(isinstance(instance, each) for each in cls.types)


class Iterator(type):
    """abstract type for Iterator
    """

    def __init__(self, dtype):
        self.dtype = dtype

    def __new__(mcls, dtype):
        cls = super(Iterator, mcls).__new__(mcls, 'Iterator{%s}' %
                                            dtype.__name__, (object, ), {})
        return cls

    def __str__(cls):
        return 'Iterator{%s}' % cls.dtype.__name__

    def __instancecheck__(cls, instance):
        if isinstance(instance, Iterable):
            return all(isinstance(each, cls.dtype) for each in instance)
        return False


class List(Iterator):
    """abstract list
    """
    def __str__(cls):
        return 'List{%s}' % cls.dtype.__name__

    def __instancecheck__(cls, instance):
        if isinstance(instance, list):
            return all(isinstance(each, cls.dtype) for each in instance)
        return False


class Tuple(Iterator):
    """abstract tuple
    """
    def __str__(cls):
        return 'Tuple{%s}' % cls.dtype.__name__

    def __instancecheck__(cls, instance):
        if isinstance(instance, tuple):
            return all(isinstance(each, cls.dtype) for each in instance)
        return False
