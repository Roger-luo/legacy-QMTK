import _pickle as pkl
from random import choice

from vmc.ham import Ham
from vmc.basis import MBOp, sigmax, sigmay, sigmaz
from vmc.sampler import STMetropolis
from vmc.utils import bin, ground


def gen_tomo_data(n, name):
    h = Ham(name, length=n, J=(1.0, 1.0), pbc=True)
    _, state = ground(h)
    ops = MBOp(choice([sigmax, sigmay, sigmaz]) for i in range(n))
    _state = ops.invtrans(state)
    sampler = STMetropolis(proposal=lambda x: _state[bin(x)], size=h.size)
    data = sampler.sample(itr=1000, burn=500, thin=1)
    return [ops.params(), list(data)]


def make_dataset(n, name='J1J2'):
    with open('%s-%s.tomo' % (name, n), 'wb') as file:
        pkl.dump([gen_tomo_data(n, name) for i in range(1000)], file)


if __name__ == '__main__':
    import fire
    fire.Fire(make_dataset)
