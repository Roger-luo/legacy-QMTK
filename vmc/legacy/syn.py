from functools import wraps
import torch
from torch.autograd import Variable
import numbers


def check_haskey(key):
    def decorator(func):
        wraps(func)

        def wrapper(collector):
            if collector.haskey(key):
                return func(collector)
            else:
                raise ValueError('need key: %s')
        return wrapper
    return decorator


def mean(itr):
    return sum(itr) / len(itr)


def scalar(number):
    if isinstance(number, Variable):
        number = number.data

    if torch.is_tensor(number) and number.numel() == 1:
        return number.storage()[0]
    elif isinstance(number, numbers.Number):
        return number
    else:
        raise ValueError('input is not a scalar, but a %s' % type(number))


# @check_haskey('eloc')
def syn_grad(collector):
    energy = scalar(mean(collector.data['eloc']))
    for g_group, p_group in zip(collector.grad_groups, collector.param_groups):
        for grad, params in zip(g_group, p_group['params']):
            if params.grad is not None:
                params.grad.data += mean(grad) * energy - mean(
                    [g * scalar(eloc) for g, eloc in
                     zip(grad, collector.data['eloc'])])
