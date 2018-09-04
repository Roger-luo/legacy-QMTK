import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.autograd import Variable

from vmc.sampler import STMetropolis
from vmc.collector import *
from vmc.ham import TFI
from vmc.lattice import Chain
from vmc.utils import ed

import matplotlib.pyplot as plt
import datetime
import numpy as np

import yaml


t = datetime.datetime.now()
signature = t.strftime("%d-%m-%Y") + '-' + str(np.random.randint(0, 2000))
# configurations

model = {'name': 'MLP', 'size': [3, 12, 12, 1]}
hamiltonain = {'name': 'TFI', 'mag': 1.0, 'lattice': {'size': 3, 'pbc': True}}
optimizer = {'name': 'Adam'}
label = {'name': signature, 'figure': 'mlp-%s.png' % signature}
train_sampler = {'itr': 1000, 'burn': 200, 'thin': 1}
test_sampler = {'itr': 1000, 'burn': 200, 'thin': 1}

if torch.cuda.is_available():
    device = 'cuda'
else:
    device = 'cpu'

configurations = {
    'device': device,
    'model': model,
    'hamiltonian': hamiltonain,
    'sampler': {'train': train_sampler, 'test': test_sampler},
    'label': label
}

with open('%s.yml' % label['name'], 'w') as outfile:
    yaml.dump(configurations, outfile, default_flow_style=False)


class MLP(nn.Module):
    """multiple layer neural network"""

    def __init__(self, *sizes):
        super(MLP, self).__init__()
        self.sizes = sizes
        self.layers = nn.ModuleList([nn.Linear(x, y)
                                     for x, y in zip(sizes[0:-1], sizes[1:])])

    def forward(self, x):
        for i, layer in enumerate(self.layers):
            if i is not len(self.layers) - 1:
                x = F.relu(layer(x))
        x = self.layers[-1](x)
        return x


lattice = configurations['hamiltonian']['lattice']
size = configurations['hamiltonian']['lattice']['size']

model = MLP(*tuple(model['size']))
lattice = Chain(lattice['size'], pbc=lattice['pbc'])
hamiltonian = TFI(hamiltonain['mag'], lattice=lattice)
# model = FakeModel(hamiltonian)

# TODO: cuda support
# if device == 'cuda':
#     model.cuda()

eigs, vecs = ed(hamiltonian.mat())
print(eigs[0])


def eloc(x):
    ret = sum(val * model(Variable(config))
              for config, val in hamiltonian.nnz(x))
    return ret / model(Variable(x))


def proposal(x):
    amp = model(Variable(x))
    return abs(amp.data[0])**2


collector = STCollector(merge=True, params=model.parameters())
sampler = STMetropolis(proposal=proposal, size=size, collector=collector)
optimizer = optim.Adam(model.parameters())


energy_cache = []

for epoch in range(1000):
    print('epoch %s' % epoch)
    collector.clear()
    sampler.sample(**train_sampler)
    energy = 0.0
    for config in collector:
        loss = -eloc(config)
        energy += -loss
        loss.backward()
        optimizer.step()

    if epoch % 10 == 0:
        collector.clear()
        sampler.sample(**test_sampler)
        count = 0
        energy = 0.0
        for config in collector:
            count += 1
            loss = eloc(config)
            energy += loss
        energy = energy / 1000
        energy_cache.append(energy.data[0])
        print(energy)

print(energy_cache)
plt.plot(energy_cache)
plt.savefig(label['figure'])
