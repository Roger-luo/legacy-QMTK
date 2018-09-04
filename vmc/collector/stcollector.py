from .base import CollectorBase


class STCollector(CollectorBase):
    """native single thread collector

    This is a simple implementation of collector, the single thread collector
    collects samples to a python dict in the cpu memory on a single thread
    """

    def __init__(self, device='cpu', merge=False, accept=True, params=None):
        super(STCollector, self).__init__(device, merge, params=params)
        self.data = dict()
        self.data['sample'] = []
        self.state = dict()
        self.state['merge'] = merge
        self.state['accept'] = accept
        if accept:
            self.data['accept'] = []
        if merge:
            self.data['count'] = []

    def __getitem__(self, ind):
        if isinstance(ind, str):
            return self.data[ind]

        if 'sample' in self.data:
            ret = [self.data['sample'][ind]]
            if self.accept:
                ret.append(self.data['accept'][ind])

            if self.merge:
                ret.append((self.data['count'][ind]))
        else:
            raise ValueError("No samples collected yet")
        return tuple(ret)

    def merge_sample(self, sample):
        for i, each in enumerate(self.data['sample']):
            if each.equal(sample):
                self.data['count'][i] += 1
                return True
        return False

    def collect_sample(self, sample, accept=None):
        if self.merge and self.merge_sample(sample):
            pass
        else:
            self.data['sample'].append(sample)
            if self.state['merge']:
                self.data['count'].append(1)
            if self.state['accept']:
                self.data['accept'].append(accept)
        self.length += 1

    def collect_grads(self):
        for g_group, p_group in zip(self.grad_groups, self.param_groups):
            for grad, params in zip(g_group, p_group['params']):
                if params.grad is not None:
                    grad.append(params.grad.data.clone())

    def collect_(self, **kwargs):
        for key, val in kwargs.items():
            if key in self.data:
                self.data[key].append(val)
            else:
                self.data[key] = [val]

    def __iter__(self):
        if self.state['merge']:
            return self.__merged_iter__()
        elif 'sample' in self.data:
            return self.data['sample'].__iter__()
        else:
            return self.grad_groups

    def __merged_iter__(self):
        for i, sample in enumerate(self.data['sample']):
            for j in range(self.data['count'][i]):
                yield sample

    def clear(self, keys=None):
        if keys is None:
            self.data.clear()
            self.data['sample'] = []
            if self.state['merge']:
                self.data['count'] = []
            if self.state['accept']:
                self.data['accept'] = []
        else:
            for each in keys:
                self.data[each].clear()
