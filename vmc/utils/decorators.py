from functools import wraps
from collections import Iterable
import types
import scipy.sparse as sp


__all__ = [
    'make_instance',
    'parse_multimatrix',
    'typecheck',
    'alias',
]


def make_instance(func):
    @wraps(func)
    def wrapper(x, **kwargs):
        flag_func_name = 'is' + func.__name__.lower()
        isfunc = globals[flag_func_name]
        traits = globals['__traits__']
        if isfunc(x):
            return x
        elif isinstance(x, str):
            return traits[x](**kwargs)
        else:
            err_msg = func.__name__ + \
                'only takes instance of' + \
                func.__name__.lower() + \
                's not %s' % type(x)
            raise TypeError(err_msg)


def parse_multimatrix(func):
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


def get_ltc_kwargs(kwargs):
    """get lattice keywords

    Params:
        kwargs: a python dict, legal inputs
            lattice shape: shape, size, length
            pbc: True or False
            lattice_params: for other params

    Returns:
        A dict contains lattice parameters.

    Raises:
        TypeError when there is no shape information
        in the keywords.
    """
    ltc_kwargs = {}
    if 'size' in kwargs:
        ltc_kwargs['shape'] = kwargs.pop('size')
    elif 'shape' in kwargs:
        ltc_kwargs['shape'] = kwargs.pop('shape')
    elif 'length' in kwargs:
        ltc_kwargs['length'] = kwargs.pop('length')
    else:
        raise TypeError("missing shape")

    if 'pbc' in kwargs:
        ltc_kwargs['pbc'] = kwargs.pop('pbc')
    if 'lattice_params' in kwargs:
        ltc_params = kwargs.pop('lattice_params')
        if isinstance(ltc_params, dict):
            ltc_kwargs.update(ltc_params)
        else:
            raise ValueError("lattice parameters should be dict"
                             "not %s" % type(ltc_params))
    return ltc_kwargs


def has_shape(kwargs):
    """has shape infos

    check if keywords include shape information
    Params:
        kwargs: a dict

    Returns:
        True or False
    """
    return any([
        'size' in kwargs,
        'shape' in kwargs,
        'length' in kwargs,
    ])


# def parse_lattice_params(cls_name):
#     """parse lattice params

#     parse lattice input parameter for object
#     with lattice class


#     """
#     def lattice(func):
#         wraps(func)

#         def wrapper(*args, **kwargs):
#             if 'lattice' in kwargs:
#                 ltc = kwargs.pop('lattice')
#                 if islattice(ltc):
#                     pass
#                 elif isinstance(ltc, dict):
#                     ltc = Lattice(**ltc)
#                 else:
#                     ltc_kwargs = get_ltc_kwargs(kwargs)
#                     ltc = Lattice(ltc, **ltc_kwargs)
#             elif has_shape(kwargs):
#                 ltc_kwargs = get_ltc_kwargs(kwargs)
#                 ltc = Chain(**ltc_kwargs)
#             elif args:
#                 ltc = Chain(*args)
#             kwargs['lattice'] = ltc
#             return func(*args, **kwargs)


def typecheck(*checkargs, **checkkwargs):
    """type check

    check function arguments type. This decorator will check arguments numbers
    but won't check keywords, it only checks input keywords types

    Params:
        checkargs: args check list
        checkkwargs: kwargs check list

    Examples:
        you can use this decorator to check your argument type as following

        @typecheck(int, (str, int), name=str, sex=(str, int))
        def foo(number, ID, name="Peter", sex=None):
            pass

        this decorator will check if the first argument is an `int` (number),
        if the argument (ID) is a `str` or `int`, for keywords name it should
        be a string type `str`, and for keyword sex, it should be a `str`
        or `int`.

    Raises:
        TypeError: when an argument is not provided type
    """

    def convert_list(type_list):
        if isinstance(type_list, type):
            return [type_list]
        elif isinstance(type_list, list):
            return type_list
        else:
            return list(type_list)

    # convert to list
    checkargs = tuple(convert_list(each) for each in checkargs)
    for key in checkkwargs:
        checkkwargs[key] = convert_list(checkkwargs[key])

    def match(arg, cls_group):
        return any([isinstance(arg, _)
                    for _ in cls_group])

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # check length
            if len(args) is not len(checkargs):
                raise TypeError('missing argument input (expected %s, got %s)'
                                % (len(args), len(checkargs)))

            for key, cls_group in checkkwargs.items():
                if key in kwargs and not match(kwargs[key], cls_group):
                    err_msg = "keyword %s " % key
                    err_msg += "is one of %s " % cls_group
                    err_msg += "not a %s" % type(kwargs[key])
                    raise TypeError(err_msg)

            for i, (each, cls_group) in enumerate(zip(args, checkargs)):
                if not match(each, cls_group):
                    err_msg = "argument [%s] " % i
                    err_msg = "is one of %s" % cls_group
                    err_msg = "not a %s" % type(each)
                    raise TypeError(err_msg)
            return func(*args, **kwargs)
        return wrapper
    return decorator


def alias(**alias_dict):
    """keyword argument alias

    use alias for keyword arguements

    Examples:

    @alias(name='n', year=['y', 'yr'])
    def foo(name='Sam', year=2017):
        print(name, year)

    >>> foo(n='Tom', yr=1997)
    Tom, 1997
    >>> foo(n='John', y=2012)
    John, 2012

    Raises:

    ValueError: multiple aliases is used in one function call, eg.

    >>> foo(n='Tom', y=2011, yr=2012)
    ValueError

    but if there is a keyword value is allowed

    >>> foo(n='Tom', year=2011, y=2012, yr=2013)
    Tom, 2011
    """
    for key in alias_dict:
        alias_dict[key] = list(alias_dict[key])

    def use_real_name(realname, aliases, kwargs):
        prv_alias = None
        for each in aliases:
            if each in kwargs:
                if prv_alias is None:
                    prv_alias = each
                    kwargs[realname] = kwargs.pop(each)
                else:
                    raise ValueError('too much input for keyword %s \
                        , already has %s' % (realname, prv_alias))

    def decorator(func):
        @wraps(func)

        def wrapper(*args, **kwargs):
            for realname, aliases in alias_dict.items():
                if realname not in kwargs:
                    use_real_name(realname, aliases, kwargs)
            return func(*args, **kwargs)
        return wrapper
    return decorator
