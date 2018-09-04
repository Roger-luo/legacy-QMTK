# TODO:
# * transform configs from {-1, 1} to {0, 1}
# * syn fake state by sampling
# * maximum likelihood

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.autograd import Variable

from vmc.data import FixedTOMO
from vmc.ham import J1J2
from vmc.utils import ground, bin
from vmc.basis import MBOp, sigmaz

# for 4 sites
nparticles = 10
noise_size = 5
batch_size = 100
d_learning_rate = 2e-4
g_learning_rate = 2e-4
optim_betas = (0.9, 0.999)
num_epochs = 50
print_interval = 300

nbasis = 100
itr = 1000
burn = 500
thin = 1

h = J1J2(length=nparticles, pbc=False, J=(1.0, 0.5))
print('generating exact ground state')
_, exact_state = ground(h)


def to_var(x):
    if torch.cuda.is_available():
        x = x.cuda()
    return Variable(x)


def sample_state(Gen, op, itr):
    p = np.zeros(2 ** nparticles)
    for i in range(itr // batch_size):
        noise = torch.randn(batch_size, noise_size)
        z = to_var(noise)
        fakes = Gen(z)
        for each_fake in fakes:
            index = bin(torch.sign(each_fake.data))
            p[index] += 1.0
    return p / sum(p)


def estimate_score(Gen, nbasis, itr):
    ret = 0.0
    op = MBOp(sigmaz for i in range(nparticles))
    for i in range(nbasis):
        p_gen = sample_state(Gen, op, itr)
        p_real = abs(exact_state) ** 2
        ret += np.linalg.norm(p_gen - p_real)
    return ret / nbasis


tomo = FixedTOMO(root='./data/', prefix='J1J2',
                 hamiltonian=h)

dataloader = torch.utils.data.DataLoader(tomo, batch_size=batch_size,
                                         shuffle=True)


# Discriminator
D = nn.Sequential(
    nn.Linear(nparticles, 20),
    nn.LeakyReLU(0.2),
    nn.Linear(20, 32),
    nn.LeakyReLU(0.2),
    nn.Linear(32, 1),
    nn.Sigmoid())

# Generator
G = nn.Sequential(
    nn.Linear(noise_size, 8),
    nn.LeakyReLU(0.2),
    nn.Linear(8, 32),
    nn.LeakyReLU(0.2),
    nn.Linear(32, 8),
    nn.LeakyReLU(0.2),
    nn.Linear(8, nparticles),
    nn.Tanh())


if torch.cuda.is_available():
    D.cuda()
    G.cuda()

criterion = nn.BCELoss()
d_optimizer = optim.Adam(D.parameters(), lr=d_learning_rate, betas=optim_betas)
g_optimizer = optim.Adam(G.parameters(), lr=g_learning_rate, betas=optim_betas)
estimates = []

for epoch in range(num_epochs):
    for i, (configs, _) in enumerate(dataloader):

        # Create the labels which are later used as input for the BCE loss
        real_labels = to_var(torch.ones(batch_size))
        fake_labels = to_var(torch.zeros(batch_size))
        # if i % 100 == 0:
        # Train the discriminator
        # Compute BCE_Loss using real configs where
        # BCE_Loss(x, y): - y * log(D(x)) - (1-y) * log(1 - D(x))
        # Second term of the loss is always zero since real_labels == 1
        if i % 100 == 0:
            # architecture A: input D with configs and basis (concated)
            d_real = D(to_var(configs))
            d_loss_real = criterion(d_real, real_labels)
            real_score = d_real

            noise = torch.randn(batch_size, noise_size)
            z = to_var(noise)
            fake_configs = G(z)
            # TODO: normalization
            d_fake = D(to_var(torch.sign(fake_configs.data)))
            d_loss_fake = criterion(d_fake, fake_labels)
            fake_score = d_fake

            # Backprop + Optimize
            d_loss = d_loss_real + d_loss_fake
            # d_loss = torch.mean(d_real) - torch.mean(d_fake)
            D.zero_grad()
            d_loss.backward()
            d_optimizer.step()

        # Train the generator
        # comput loss with fake configs
        noise = torch.randn(batch_size, noise_size)
        z = to_var(noise)
        fake_configs = G(z)
        d_fake = D(to_var(torch.sign(fake_configs.data)))

        # We train G to maximize log(D(G(z))
        # instead of minimizing log(1-D(G(z)))
        # For the reason, see the last paragraph
        # of section 3. https://arxiv.org/pdf/1406.2661.pdf
        g_loss = criterion(d_fake, real_labels)
        # g_loss = -torch.mean(d_fake)

        D.zero_grad()
        G.zero_grad()
        g_loss.backward()
        g_optimizer.step()

        if (i + 1) % print_interval == 0:
            print('Epoch [%d/%d], Step[%d/%d], d_loss: %.4f, '
                  'g_loss: %.4f, D(x): %.2f, D(G(z)): %.2f'
                  % (epoch, num_epochs, i + 1, len(dataloader),
                     d_loss.data[0], g_loss.data[0],
                     real_score.data.mean(), fake_score.data.mean()))
            estimates.append(estimate_score(G, 1, 500))
            print("estimate score: %s" % estimates[-1])

# Save the trained parameters
torch.save(G.state_dict(), './generator.pkl')
torch.save(D.state_dict(), './discriminator.pkl')
torch.save(estimates, './estimates.pkl')
