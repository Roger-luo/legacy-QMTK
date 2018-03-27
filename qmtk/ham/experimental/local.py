import re


class LocalRules:
    block = re.compile(r'([\w_]+)[\s,]*')
    underline = re.compile(r'(\w+)_(\w+)')


class LocalHamiltonParser(object):
    """local hamiltonian
    """

    OP = []
    default_rules = ['block', 'underline']

    def __init__(self, rules=None):
        if rules is None:
            self.rules = LocalRules()

    def collect(self, **kwargs):
        self.OP.append(kwargs)

    def parse(self, text, nbrs, rules=None):
        text = text.rstrip('\n')
        self.OP.clear()
        if not rules:
            rules = list(self.default_rules)

        while text:
            pattern = getattr(self.rules, 'block')
            m = re.match(pattern, text)
            if m is not None:
                self.parse_expr(m.group(1), nbrs)
                text = text[len(m.group(0)):]
            else:
                print(text)
                break

        self.map2obj()

    def parse_underline(self):
        for each in self.expr:
            self.parse_ops(each)

    def parse_expr(self, text, nbrs):
        pattern = getattr(self.rules, 'underline')
        m = re.match(pattern, text)
        if m is not None:
            token = m.group(1)
            pos = m.group(2)
            if pos.isdigit():
                pos = int(pos)
                self.collect(token=token, pos=pos)
        else:
            self.collect(token=text, pos=nbrs.pop())


lc = LocalHamiltonParser()
lc.parse("X_0,Y_2,Z", [3])
print(lc.OP)
