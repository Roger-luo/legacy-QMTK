import torch
from .base import GeneratorBase


class IterateAll(GeneratorBase):
    """iterate all configurations

    keyword size is needed if use it as an iterator, e.g.

    for config in IterateAll(size=[2, 2]):
        print(config)
    """

    def __init__(self, **kwargs):
        super(IterateAll, self).__init__('iterate all', **kwargs)

    def shift(self, data):
        """binary add one to configurations on {-1, 1}
        """
        storage = data.storage()
        for i, each in enumerate(storage):
            if each == 1:
                storage[i] = -1
            else:
                storage[i] = 1
                break
        return data

    def propose(self, data):
        cand = data.clone()
        self.shift(cand)
        return cand

    def __next__(self):
        data = torch.zeros(
            *self.size, out=torch.LongTensor()) - 1
        yield data
        for i in range(2 ** data.numel() - 1):
            yield self.shift(data)
        return 1
