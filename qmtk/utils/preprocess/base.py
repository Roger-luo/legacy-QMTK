import os
import inspect
from functools import wraps
from collections import OrderedDict

try:
    from colored import fg, attr
except ModuleNotFoundError:
    def blank(x):
        return ''
    fg, attr = blank, blank

VERBOSE = os.environ.get('QMTK_VERBOSE', None)


class Preprocessor(object):
    """Base type for argument preprocessors

    preprocess methods is extended by adding methods begin with
    'check_' or 'preprocess_' in subclass.
    """
    CTRL_ENVS = OrderedDict()
    CTRL_ENVS['PREPROCESS'] = os.environ.get('QMTK_PREPROCESS', None)

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for name, method in inspect.getmembers(self):
                if name.startswith('check_'):
                    self.execute(method, func, args, kwargs)
                elif name.startswith('preprocess_'):
                    self.execute(method, func, args, kwargs)
            return func(*args, **kwargs)

        preprocess = None
        for key, val in self.CTRL_ENVS.items():
            if val is not None:
                preprocess = val
                break

        if VERBOSE is not None:
            title = fg(11) + attr('bold') + \
                'entering decorator ' + attr('reset') + \
                fg(99) + attr('bold') + type(self).__name__ + attr('reset')
            print(title)
            print('Preprocessing Enviroment Variables:')
            for key, val in self.CTRL_ENVS.items():
                print('    %s: %s' % (key, val))

        if preprocess is None:
            return wrapper
        else:
            return func

    def execute(self, method, func, args, kwargs):
        argsspec = inspect.signature(method).parameters
        traits = {'func': func, 'args': args, 'kwargs': kwargs}
        inputs = tuple(traits[each] for each in argsspec)
        method(*inputs)
