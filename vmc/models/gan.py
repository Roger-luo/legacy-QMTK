import sys
import os
import errno

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.autograd import Variable
from torch.utils.data import DataLoader
from .config import Configure

from uuid import uuid1
from vmc.data import STDS
from vmc.utils import bin


class GAN(object):
    def __init__(self, filename, generator, discriminator,
                 gpu=0, data=None, log=sys.stdout):
        self.filename = filename
        self.device = gpu
        configs = Configure(filename)

        self.generator = generator(
            configs['nparticles'], configs['noise']['size'])
        self.discriminator = discriminator(
            configs['nparticles'])

        if torch.cuda.is_available():
            self.generator.cuda(self.device)
            self.discriminator.cuda(self.device)

        self.schedule = configs['schedule']

        if data is not None:
            self.data = data
        elif 'data' in configs:
            self.data = STDS(configs['data']['name'],
                             configs['data']['lattice'],
                             configs['nparticles'],
                             pbc=configs['data']['pbc'],
                             level=configs['data']['level'],
                             size=configs['data']['size'],
                             )
        else:
            raise ValueError('data needed')

        print('batch size: %s' % self.schedule['batch_size'])
        self.dataloader = DataLoader(
            self.data, batch_size=self.schedule['batch_size'], shuffle=True)
        print('dataloader: %s' % len(self.dataloader))

        self.optim = {}
        self.optim['g'] = optim.Adam(
            self.generator.parameters(),
            lr=configs['generator']['optimizer']['learning_rate'],
            betas=tuple(configs['generator']['optimizer']['optim_betas'])
        )
        self.optim['d'] = optim.Adam(
            self.generator.parameters(),
            lr=configs['discriminator']['optimizer']['learning_rate'],
            betas=tuple(configs['discriminator']['optimizer']['optim_betas'])
        )

        self.path = {}
        if 'root' in configs['path']:
            root = configs['path']['root']
        else:
            raise ValueError('root needed')

        for name, path in configs['path'].items():
            if name == 'root':
                self.path[name] = root
            else:
                self.path[name] = os.path.join(root, path)

        self.loss = configs['loss']

        self.prefix = str(uuid1())[::-1]
        prefixes = configs['prefix']
        if prefixes[0] == 'fuckstrictyaml':
            configs['prefix'] = [self.prefix]
        else:
            prefixes.append(self.prefix)
            configs['prefix'] = prefixes

        self.infos = {}
        self.configs = configs
        self.logfile = log

    def collect_info(self, key, value):
        if key in self.infos:
            self.infos[key].append(value)
        else:
            self.infos[key] = [value]

    @staticmethod
    def mkdir(path):
        try:
            os.makedirs(path)
        except OSError as e:
            if e.errno == errno.EEXIST:
                pass
            else:
                raise

    def mkpath(self):
        for _, path in self.path.items():
            self.mkdir(path)

    def save(self):
        self.mkpath()

        prefix = self.prefix
        names, paths = {}, {}
        names['g'] = prefix + '.' + self.configs['generator']['suffix']
        names['d'] = prefix + '.' + self.configs['discriminator']['suffix']

        paths['g'] = os.path.join(
            self.path['model'], names['g'])
        paths['d'] = os.path.join(
            self.path['model'], names['d'])

        # save models
        torch.save(self.generator, paths['g'])
        torch.save(self.discriminator, paths['d'])

        # save infos
        for key, val in self.infos.items():
            name = prefix + '.' + key
            torch.save(val, os.path.join(self.path['infos'], name))

        self.configs.save()

    def to_var(self, x):
        if torch.cuda.is_available():
            x = x.cuda(self.device)
        return Variable(x)

    def step(self, i, batch, basis):
        batch_size = self.configs['schedule']['batch_size']
        noise_size = self.configs['noise']['size']
        criterion = self.loss

        real_labels = self.to_var(torch.ones(batch_size))
        fake_labels = self.to_var(torch.zeros(batch_size))

        d_real = self.discriminator(self.to_var(batch))
        d_loss_real = criterion(d_real, real_labels)
        # real_score = d_real

        z = self.to_var(torch.randn(batch_size, noise_size))
        fake_configs = self.generator(z)
        d_fake = self.discriminator(fake_configs)
        d_loss_fake = criterion(d_fake, fake_labels)
        # fake_score = d_fake

        d_loss = d_loss_real + d_loss_fake
        self.discriminator.zero_grad()
        d_loss.backward()
        self.optim['d'].step()

        z = self.to_var(torch.randn(batch_size, noise_size))
        fake_configs = self.generator(z)
        g_fake = self.discriminator(fake_configs)

        g_loss = criterion(g_fake, real_labels)

        self.discriminator.zero_grad()
        self.generator.zero_grad()
        g_loss.backward()
        self.optim['g'].step()
        if i % self.schedule['interval']['dump'] == 0:
            self.collect_info('real', d_real.data.mean())
            self.collect_info('fake', d_fake.data.mean())
            self.collect_info('d_loss', d_loss.data[0])
            self.collect_info('g_loss', g_loss.data[0])

    def logger(self, epoch, i):
        logs = {}
        logs['epoch'] = 'Epoch [%d/%d]' % (epoch, self.schedule['num'])
        logs['step'] = 'Step [%d/%d]' % (i, len(self.dataloader))
        logs['loss'] = 'd_loss: %.4f, g_loss: %.4f' % (
            self.infos['d_loss'][-1], self.infos['g_loss'][-1])
        logs['score'] = 'D(x): %.2f, D(G(z)): %.2f' % (
            self.infos['real'][-1], self.infos['fake'][-1])
        log = ','.join(val for key, val in logs.items())
        self.logfile.write(log + '\n')
        self.logfile.flush()
        return logs

    def compare(self):
        noise_size = self.configs['noise']['size']

        p1 = self.data.state * self.data.state.conj()
        p2 = np.zeros(*self.data.state.shape)
        z = self.to_var(torch.randn(1000, noise_size))
        for each in self.generator(z):
            p2[bin(torch.sign(each.data))] += 1
        p2 = p2 / np.linalg.norm(p2, ord=1)
        dis = np.linalg.norm(p1 - p2)
        self.collect_info('compare', dis)
        print('compare to exact: %s' %
              dis, file=self.logfile)

    def train(self, exact=False):
        if self.loss == 'BCE':
            self.loss = nn.BCELoss()

        num_epochs = self.configs['schedule']['num']

        for epoch in range(num_epochs):
            for i, (configs, _) in enumerate(self.dataloader):
                self.step(i, configs, _)
                if i % self.schedule['interval']['dump'] == 0:
                    self.logger(epoch, i)
                    if exact:
                        self.compare()


class WGAN(GAN):
    """W-GAN"""

    def step(self, i, batch, basis):
        batch_size = self.configs['schedule']['batch_size']
        noise_size = self.configs['noise']['size']

        d_real = self.discriminator(self.to_var(batch))

        z = self.to_var(torch.randn(batch_size, noise_size))
        fake_configs = self.generator(z)
        d_fake = self.discriminator(fake_configs)

        d_loss = torch.mean(d_real) - torch.mean(d_fake)
        self.discriminator.zero_grad()
        d_loss.backward()
        self.optim['d'].step()

        z = self.to_var(torch.randn(batch_size, noise_size))
        fake_configs = self.generator(z)
        g_fake = self.discriminator(fake_configs)

        g_loss = - torch.mean(g_fake)

        self.discriminator.zero_grad()
        self.generator.zero_grad()
        g_loss.backward()
        self.optim['g'].step()

        if i % self.schedule['interval']['dump'] == 0:
            self.collect_info('real', d_real.data.mean())
            self.collect_info('fake', d_fake.data.mean())
            self.collect_info('d_loss', d_loss.data[0])
            self.collect_info('g_loss', g_loss.data[0])
