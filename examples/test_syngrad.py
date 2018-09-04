import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.autograd import Variable

from vmc.configs import IterateAll
from vmc.sampler import STMetropolis
from vmc.collector import *
from vmc.ham import TFI
from vmc.lattice import Chain
from vmc.syn import syn_grad


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


model = MLP(3, 12, 12, 1)
lattice = Chain(3, pbc=True)
hamiltonian = TFI(mag=1.0, lattice=lattice)


def eloc(x):
    ret = sum(val * model(Variable(config))
              for config, val in hamiltonian.nnz(x))
    return ret / model(Variable(x))


def exact_energy():
    return sum(torch.abs(model(Variable(config))) ** 2 * eloc(config))


def proposal(x):
    amp = model(Variable(x))
    return abs(amp.data[0])**2


collector = STCollector(merge=True, params=model.parameters())
sampler = STMetropolis(proposal=proposal, size=3, collector=collector)
optimizer = optim.Adam(model.parameters())
energy_cache = []

for epoch in range(1000):
    collector.clear()
    configs = sampler.sample(itr=1000, burn=500, thin=1)
    energy = 0.0
    for config in configs:
        loc = eloc(config)
        energy += loc
        collector.zero_grad()
        psi = model(Variable(config))
        psi.backward()
        collector.collect(gradient, eloc=loc)
        # or
        # collector.collect(gradient)
    syn_grad(collector)
    # or
    # syn_sr(collector)

    optimizer.step()

    if epoch % 10 == 0:
        collector.clear()
        sampler.sample(itr=1000, burn=500, thin=1)
        count = 0
        energy = 0.0
        for config in collector:
            count += 1
            loss = eloc(config)
            energy += loss
        energy = energy / 1000
        energy_cache.append(energy.data[0])
        print(energy)
