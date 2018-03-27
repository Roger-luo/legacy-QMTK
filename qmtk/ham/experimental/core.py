# find mask
import re
from itertools import product


class Expr:
    pass


class SigmaX(Expr):
    name = ['X', 'SigmaX', 'sigmax']
    flip = True
    up = 1
    down = 1


class SigmaY(Expr):
    name = ['Y', 'SigmaY', 'sigmay']
    flip = True
    up = -1.j
    down = 1.j


class SigmaZ(Expr):
    name = ['Z', 'SigmaZ', 'sigmaz']
    flip = False
    up = -1
    down = 1


class LocalHamilton(object):

    OP = []

    def __init__(self, text, nbrs=None, state=(0, 1)):
        self.parse(text, nbrs)
        self.down, self.up = state

    def collect(self, **kwargs):
        self.OP.append(kwargs)

    def parse(self, text, nbrs):
        text = text.rstrip('\n')
        self.OP.clear()

        while text:
            m = re.match(r'([\w_]+)[\s,]*', text)
            if m is not None:
                self.parse_expr(m.group(1), nbrs)
                text = text[len(m.group(0)):]
            else:
                print(text)
                break

    def parse_expr(self, text, nbrs):
        m = re.match(r'(\w+)_(\w+)', text)
        if m is not None:
            token = m.group(1)
            pos = m.group(2)
            if pos.isdigit():
                pos = int(pos)
                self.collect(token=token, pos=pos)
        else:
            self.collect(token=text, pos=nbrs.pop())

    def eval_mask(self, mask):
        self.flip = []
        val = 1
        for each, c in zip(self.OP, mask):
            val *= self.eval_op(each, c)
        return self.flip, val

    def eval_op(self, op, c):
        for each in Expr.__subclasses__():
            if op['token'] in each.name:
                self.flip.append(each.flip)
                if c == self.down:
                    return each.down
                else:
                    return each.up


class Hamiltonian(object):
    """hamiltonian
    """

    def __init__(self, expr, lattice, nbrs=None, state=(0, 1)):
        super(Hamiltonian, self).__init__()
        self.local = LocalHamilton(expr, nbrs=nbrs, state=state)
        self.lattice = lattice
        self.state = state

        self.nbrs = []
        for each in self.local.OP:
            self.nbrs.append(each['pos'])

        if self.nbrs[0] != 0:
            self.nbrs = [each - self.nbrs[0] for each in self.nbrs]

        self.nbrs = self.nbrs[1:]

    def local_mask(self, site, configs):
        all_nbrs = tuple(lattice.neighbors(site, nbr) for nbr in self.nbrs)
        itr = product(*all_nbrs)
        for neighbors in itr:
            index = [site] + list(neighbors)
            mask = [configs[each] for each in index]
            yield index, mask

    def mask(self, configs):
        for site in self.lattice.sites():
            for index, mask in self.local_mask(site, configs):
                yield index, mask

    def eval(self, configs):
        lhs = configs.copy()
        for index, mask in self.mask(configs):
            flips, val = self.local.eval_mask(mask)
            for i, each in zip(index, flips):
                if each:
                    if lhs[i] == self.state[0]:
                        lhs[i] = self.state[1]
                    else:
                        lhs[i] = self.state[0]
                yield lhs, val


if __name__ == '__main__':
    from qmtk.lattice import PBCSquare, Square
    import numpy as np

    lattice = Square(shape=(2, 2))
    h = Hamiltonian("X_0,X_1", lattice)

    configs = np.random.randint(0, 2, size=lattice.shape)
    print(configs)
    count = 0
    for lhs, v in h.eval(configs):
        print(lhs, v)
        count += 1
    print(count)
