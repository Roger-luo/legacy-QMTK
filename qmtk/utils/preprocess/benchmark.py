"""decorator for measuring execution time of function.
"""


from functools import wraps
import time
import timeit
import numpy as np


__all__ = [
    'tmeasure',
]


class tmeasure(object):
    def __init__(self, number=10000, repeat=7,
                 timer=time.perf_counter, verbose=True):
        self.number = number
        self.repeat = repeat
        self.timer = timer
        self._verbose = verbose
        self.data = []

    def verbose(self):
        mean_t = self.timestamp(np.mean(self.data))
        std_t = self.timestamp(np.std(self.data))
        msg = '%s ± %s per loop ' % (mean_t, std_t)
        msg += '(mean ± std. dev. of %s runs, ' % self.repeat
        msg += '%s loops each)' % self.number
        print(msg)

    @staticmethod
    def timestamp(t):
        if t < 1e-1 and t > 1e-3:
            return '%.3g ms' % (t * 1e3)
        elif t < 1e-3 and t > 1e-6:
            return '%.3g µs' % (t * 1e6)
        elif t < 1e-6:
            return '%.3g ns' % (t * 1e9)
        else:
            return '%.3g s' % t

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            def pack_f():
                func(*args, **kwargs)
            self.data = timeit.repeat(
                stmt=pack_f,
                number=self.number,
                repeat=self.repeat)
            if self._verbose:
                self.verbose()
            return np.mean(self.data)
        return wrapper

    @staticmethod
    def time(func):
        return tmeasure()(func)
