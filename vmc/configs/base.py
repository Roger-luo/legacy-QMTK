class GeneratorBase(object):
    """Base type for generators

    Generators offers methods to generate configurations, it should implement
    at least a `propose` method to propose next generator state
    """

    def __init__(self, name, **params):
        super(GeneratorBase, self).__init__()
        self.name = name
        if 'size' in params:
            self.size = params['size']
        else:
            self.size = None
        self.params = params

    def __str__(self):
        ret = '%s\n' % (self.name)
        for param_key, param_val in self.params.items():
            ret += ' - %s:%s\n' % (param_key, param_val)
        return ret

    def __iter__(self):
        if self.size is None:
            raise ValueError('generator should be initialized with size, \
                try to add keyword in initialization: size')
        return self.__next__()

    def __next__(self):
        raise NotImplementedError

    def propose(self):
        pass
