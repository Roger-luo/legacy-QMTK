import os
import sys
from functools import wraps

try:
    from colored import fg, attr
except ModuleNotFoundError:
    def blank(x):
        return ''
    fg, attr = blank, blank


VERBOSE = os.environ.get('QMTK_VERBOSE', None)


def log(msg, c=11):
    msg = fg(c) + attr('bold') + '[LOG]:' + attr('reset') + msg

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if VERBOSE is not None:
                print(msg, file=sys.stdout)
            return func(*args, **kwargs)
        return wrapper
    return decorator
