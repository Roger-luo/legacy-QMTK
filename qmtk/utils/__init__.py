# from torch import zeros

# __all__ = [
#     'n2tensor',
#     'tensor2n',
# ]


# def n2tensor(n, shape):
#     """convert integer to bit tensor
#     """
#     t = zeros(*shape)
#     storage = t.storage()
#     for i in range(t.numel()):
#         storage[i] = (n >> i) & 1
#     return t


# def tensor2n(t):
#     """convert bit tensor to integer
#     """
#     flatten = t.view(t.numel())
#     ret = 0
#     for i, each in enumerate(flatten):
#         ret += (each) / 2 * 2 ** i
#     return int(ret)
