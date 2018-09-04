import torch
from torch.autograd import Variable
from numbers import Number

gradient = object()

try:
    from numpy import ndarray
except ImportError:
    raise ImportWarning("Can't import numpy"
                        "name ndarray is set to be an object")
    ndarray = object()


class CollectorBase(object):
    """Base type for collectors

    Base type for collectors. Collectors aims to collect samples
    from samplers and offer measurement methods. By default gradient
    will be collected in the memory.

    Subclasses should implement:
        init methods:
        init sample collector: for allocating sample database,
        `__init_sample_collector__(self, sample, accept)`

        following collect methods:
        sample collect methods:
            `collect_sample(self, sample, accept)`
        gradient collect methods:
            `collect_grads(self)`
        arbitrary collect methods:
            `collect_(**kwargs)`

        iteration methods: iterate through samples
        `__next__`

        clear method: clear all the data, or the given key's data
        `clear(self, key=None)`
    """

    def __init__(self, device='cpu', merge=False, params=None):
        super(CollectorBase, self).__init__()
        self.data = None
        self.device = device
        self.length = 0
        self.merge = merge
        if params is not None:
            self.__init_params__(params)
        else:
            self.param_groups = None

    def __init_sample_collector__(self, sample, accept=None):
        raise NotImplementedError

    def __init_params__(self, params):
        if isinstance(params, Variable) or torch.is_tensor(params):
            raise TypeError("params argument given to the optimizer should be "
                            "an iterable of Variables or dicts, but got " +
                            torch.typename(params))
        self.param_groups = list(params)
        if len(self.param_groups) == 0:
            self.param_groups = None
            return
        if not isinstance(self.param_groups[0], dict):
            self.param_groups = [{'params': self.param_groups}]

        param_set = set()
        for group in self.param_groups:
            if isinstance(group['params'], torch.autograd.Variable):
                group['params'] = [group['params']]
            else:
                group['params'] = list(group['params'])
            group_set = set(group['params'])
            if not param_set.isdisjoint(group_set):
                raise ValueError('some parameters appear in '
                                 'more than one parameter group')
            param_set.update(group_set)

        for group in self.param_groups:
            for param in group['params']:
                if not isinstance(param, Variable):
                    raise TypeError('collector can only collect Variables, '
                                    'but one of the params is ' +
                                    torch.typename(param))
                if not param.requires_grad:
                    raise ValueError("collecting a parameter that doesn't"
                                     "require gradients")
                if not param.is_leaf:
                    raise ValueError("can't collect a non-leaf Variable")

        self.grad_groups = []
        for group in self.param_groups:
            grads = []
            for param in group['params']:
                grads.append([])
            self.grad_groups.append(grads)

    def get(self, key):
        raise NotImplementedError

    def __len__(self):
        return self.length

    def __iter__(self):
        return self.__next__()

    def __call__(self, *args, **kwargs):
        return self.collect(*args, **kwargs)

    def __next__(self):
        raise NotImplementedError

    def grads(self):
        return iter(self.grad_groups)

    def collect_sample(self, sample, accept):
        """
        collect samples
        """
        raise NotImplementedError

    def collect_grads(self):
        """
        collect models parameters
        """
        raise NotImplementedError

    def collect_(self, **kwargs):
        """
        general methods for collecting data
        """
        raise NotImplementedError

    def collect(self, *args, **kwargs):
        """
        collect given kwargs, if no inputs or has key word grads to be True,
        then collect model's parameters gradients

        Params:
            sample
            accept
            grads

        """
        if gradient in args:
            self.collect_grads()
        elif not kwargs:
            self.collect_grads()
        elif 'grads' in kwargs:
            kwargs.pop('grads')
            self.collect_grads()

        if 'sample' in kwargs:
            sample = kwargs.pop('sample')
            if 'accept' in kwargs:
                accept = kwargs.pop('accept')
                self.collect_sample(sample, accept=accept)
            else:
                self.collect_sample(sample)
        elif torch.is_tensor(args[0]) and isinstance(args[1], Number):
            self.collect_sample(args[0], accept=args[1])
        else:
            for each in args:
                if torch.is_tensor(each) or isinstance(each, ndarray):
                    self.collect_sample(each, accept=None)
                elif not args:
                    raise ValueError("collector only collects"
                                     " torch.Tensor or numpy.ndarray")
        if kwargs:
            self.collect_(**kwargs)

    def measure(self, op, requires_grad=False, params=None):
        """measure collected samples

        Params:
            op: operator to measure
        """
        return sum(op(each) for each in
                   self.__iter__()) / self.length

    def syn_grad(self):
        pass

    def zero_grad(self):
        """assign grads to zero
        """
        for group in self.param_groups:
            for p in group['params']:
                if p.grad is not None:
                    if p.grad.volatile:
                        p.grad.data.zero_()
                    else:
                        data = p.data.data
                        p.grad = Variable(data.new().resize_as_(data).zero_())

    def clear(self, key=None):
        raise NotImplementedError

    def save(self, filename):
        raise NotImplementedError

    def load(self, filename):
        raise NotImplementedError
