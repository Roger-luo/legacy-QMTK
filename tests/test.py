import torch
from vmc.data import TOMO
from vmc.ham import J1J2


tomo = TOMO(root='./data/', prefix='J1J2',
            hamiltonian=J1J2(length=4, pbc=False, J=(1.0, 0.5)))

dataloader = torch.utils.data.DataLoader(tomo, batch_size=100,
                                         shuffle=True)


for idx, (config, basis) in enumerate(dataloader):
    print(config.size(), basis.size())
    noise = torch.randn(100, 8)
    print(torch.cat((basis, noise), 1).size())
