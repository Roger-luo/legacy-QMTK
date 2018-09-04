from .base import LatticeBase


class Chain(LatticeBase):
    """chain"""

    def __init__(self, *args, **kwargs):
        super(Chain, self).__init__('Chain', *args, **kwargs)

    def grid(self, nbr=None):
        length = self.shape[0]
        if nbr is None or nbr is 0:
            for i in range(length):
                yield i
        else:
            for i in range(length):
                if not self.pbc and i + nbr is length:
                    break
                yield i, (i + nbr) % length
