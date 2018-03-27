import re
import numpy as np
from qmtk.utils import kron


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
        self.vals = []
        for each, c in zip(self.OP, mask):
            self.eval_op(each, c)
        return self.flip, self.vals

    def eval_op(self, op, c):
        for each in Expr.__subclasses__():
            if op['token'] in each.name:
                self.flip.append(each.flip)
                if c == self.down:
                    self.vals.append(each.down)
                else:
                    self.vals.append(each.up)


h = LocalHamilton('X_1,Y_2,Z_5')
print(h.OP)
print(h.eval([0, 0, 0]))
