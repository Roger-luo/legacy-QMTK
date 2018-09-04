import torch
from torch.autograd import Variable


def check_grad(module, input, input_size=None, idtype='float32', loss=None, dx=1e-3):
    traits = {
        'float32': torch.FloatTensor,
        'float64': torch.DoubleTensor,
        'complex64': torch.ZFloatTensor,
        'complex128': torch.ZDoubleTensor,
    }

    if idtype in traits:
        in_tensor = torch.rand(*input_size, out=traits[idtype]())
    else:
        raise TypeError('only check float32, float64, '
                        'complex64, complex128 gradients')

    in_var = Variable(in_tensor)

    if loss is None:
        out_var = module(in_var)
        func = module
        if out_var.numel() is not 1:
            raise ValueError('module output should be a scalar,'
                             'or a loss function is needed')
    else:
        out_var = loss(in_var)
        func = loss

    def assertEqual(a, b, eps=1e-5):
        if abs(a - b) > eps:
            raise ValueError('gradient is not corrent')

    out_var.backward()
    for param in module.parameters():
        param_data = param.data.storage()
        param_grad = param.grad.data.storage()
        for i, each_param in enumerate(param_data):
            param_data[i] += dx
            assertEqual(param_grad[i], (func(
                in_var).data.storage() - out_var.data.storage()) / dx)
            param_data[i] -= dx


if __name__ == '__main__':
    x = Variable(torch.ones(1))
    y = x ** 2

    check_grad(lambda x: x ** 2, input_size=(1, ))
