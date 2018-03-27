from .base import Preprocessor

import os
from qmtk.utils.abstracts import Iterator


class typecheck(Preprocessor):
    """type check decorator

    check function arguments type and argument numbers
    but won't check the name of keywords, it only check
    input keywords value's types. For checking keyword
    names, please use alias.

    Params:
        args: args check list
        kwargs: kwargs check list

    Examples:
        you can use this decorator to check your argument type
        as following

        ```
        @typecheck(int, Union(str, int), name=str, sex=Union(str, int))
        def foo(number, ID, name="Peter", sex=None):
            pass
        ```

        this decorator will check if the first argument is an `int` (number),
        if the argument (ID) is a `str` or `int`, for keywords name it should
        be a string type `str`, and for keyword sex, it should be a `str` or
        `int`.

    Raises:
        TypeError: this decorator raises TypeError when input value's type is
                   not valid.
    """

    def __init__(self, *args, **kwargs):
        super(typecheck, self).__init__()

        self.CTRL_ENVS['TYPECHECK'] = os.environ.get('QMTK_TYPECHECK', None)

        self.checklist = {
            'args': args,
            'kwargs': kwargs,
        }

    @staticmethod
    def _comparetype(got, expected):
        if isinstance(got, expected):
            return None
        else:
            return "(expected %s, got %s)" % (
                expected.__name__, type(got).__name__)

    def _typechecker(self, got, expected):
        err_msg = None
        if expected is None:
            return err_msg

        if isinstance(expected, type):
            err_msg = self._comparetype(got, expected)
        elif isinstance(expected, Iterator(type)):
            err_msg = self._comparetype(got, type(expected))
            if err_msg is None:
                for i, (g, e) in enumerate(zip(got, expected)):
                    if not isinstance(g, e):
                        err_msg = "(expected %s at [%s], got %s)" % (
                            e.__name__, i, type(g).__name__)

        return err_msg

    def check_args(self, args):
        # check argument numbers
        expected = len(self.checklist['args'])
        got = len(args)
        if got is not expected:
            raise TypeError("missing argument input "
                            "(expect %s, got %s)" % (expected, got))
        # check argument types
        for i, (got, expected) in enumerate(zip(args, self.checklist['args'])):
            err_msg = self._typechecker(got, expected)
            # process error
            if err_msg is not None:
                pos = "invalid type for argument [%s]" % i
                raise TypeError(pos + ' ' + err_msg)

    def check_kwargs(self, kwargs):
        for key, expected in self.checklist['kwargs'].items():
            if key in kwargs:
                err_msg = self._typechecker(kwargs[key], expected)
                # process error
                if err_msg is not None:
                    pos = "invalid type for keyword %s" % key
                    raise TypeError(pos + ' ' + err_msg)


class alias(Preprocessor):
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

    def __init__(self, **kwargs):
        super(alias, self).__init__()
        self.CTRL_ENVS['ALIAS'] = os.environ.get('QMTK_ALIAS', None)

        self.alias_list = {}
        for key, val in kwargs.items():
            self.alias_list[key] = set(val)

    def use(self, realname, alias_list, kwargs):
        nickname = None
        for name in alias_list:
            if name in kwargs:
                if nickname is None:
                    kwargs[realname] = kwargs.pop(name)
                    nickname = name
                elif nickname is not None:
                    raise KeyError("Too many keys for %s, already has %s" %
                                   (realname, nickname))

    def preprocess_kwargs(self, kwargs):
        for realname, aliases in self.alias_list.items():
            if realname not in kwargs:
                self.use(realname, aliases, kwargs)


class require(Preprocessor):
    """check required keywords

    check implicit keywords declared by **kwargs in the function

    Examples:

    @require('shape', pbc=True)
    def foo(**kwargs):
        pass

    This decorator will check if the function `foo` has keyword shape,
    and pbc, if there is no pbc, keyword pbc will be set to True
    """

    def __init__(self, *keys, **kwargs):
        super(require, self).__init__()
        self.CTRL_ENVS['REQUIRE'] = os.environ.get('QMTK_REQUIRE', None)

        self.keys = keys
        self.err_dict = kwargs

    def check_keys(self, kwargs):
        for each in self.keys:
            if each not in kwargs:
                raise KeyError("Missing %s" % each)

        for key, val in self.err_dict.items():
            if key not in kwargs:
                kwargs[key] = val
