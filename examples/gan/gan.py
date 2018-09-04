import torch.nn as nn
from vmc.models import GAN


def G(n, noise):
    return nn.Sequential(
        nn.Linear(noise, 256),
        nn.LeakyReLU(0.2),
        nn.Linear(256, 256),
        nn.LeakyReLU(0.2),
        nn.Linear(256, n),
        nn.Tanh())


def D(n):
    return nn.Sequential(
        nn.Linear(n, 256),
        nn.LeakyReLU(0.2),
        nn.Linear(256, 256),
        nn.LeakyReLU(0.2),
        nn.Linear(256, 1),
        nn.Sigmoid())


gan = GAN('config.yml', G, D)
gan.train(exact=True)
gan.save()
