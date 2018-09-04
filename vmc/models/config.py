from strictyaml import load, Map, Int, Str, \
    Float, Optional, Seq, Bool


class Configure(object):

    noise_schema = \
        Map({'size': Int(), 'type': Str()})

    optim_schema = \
        Map({
            'learning_rate': Float(),
            'optim_betas': Seq(Float()),
        })

    model_schema = \
        Map({
            'suffix': Str(),
            'optimizer': optim_schema,
        })

    sche_schema = \
        Map({
            'num': Int(),
            'batch_size': Int(),
            'interval': Map({
                'dump': Int(),
            })
        })

    path_schema = \
        Map({
            'root': Str(),
            'model': Str(),
            'infos': Str(),
            'logs': Str(),
        })

    data_schema = \
        Map({
            'name': Str(),
            'lattice': Str(),
            'size': Int(),
            'pbc': Bool(),
            'level': Int(),
        })

    main_schema = Map({
        'nparticles': Int(),
        'data': data_schema,
        'noise': noise_schema,
        'generator': model_schema,
        'discriminator': model_schema,
        'loss': Str(),
        'schedule': sche_schema,
        'path': path_schema,
        Optional('prefix'): Seq(Str()),
    })

    def __init__(self, filename):
        super(Configure, self).__init__()
        self.filename = filename
        self.raw_yaml = self.load()
        self.data = self.raw_yaml.data

    def load(self):
        with open(self.filename, 'r') as f:
            raw = f.read()
        raw_yaml = load(raw, self.main_schema)
        return raw_yaml

    def save(self):
        with open(self.filename, 'w') as f:
            f.write(self.raw_yaml.as_yaml())

    def __setitem__(self, index, value):
        self.raw_yaml[index] = value

    def __getitem__(self, index):
        return self.data[index]

    def __contains__(self, value):
        return self.data.__contains__(value)
