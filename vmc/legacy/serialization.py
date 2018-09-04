import yaml
import torch.cuda
import datetime
import os
from vmc.lattice import Lattice
from vmc.ham import Ham

PARSER_COUNT = 0


def save(*args, **params):
    """
    Save configurations

    Keywords:

        dir: config file dir. (optional)
        filename: file name to save (should not include .yml suffix currently)
        ham or hamiltonian: a hamiltonian object
        model: ansatz
        figure or figure_path: path for the saved figure. (optional)

    TODO:
        - regex match, to remove suffix .yml if there is one
        - auto-save figure in this function
        - config file dir
        - model file dir
    """

    def dump_lattice(params):
        if 'lattice' in params:
            ltc = vars(params.pop('lattice'))
        else:
            return None

        if not ltc['params']:
            ltc.pop('params')

        return ltc

    def dump_ham(params):
        if 'ham' in params:
            ret = vars(params.pop('ham'))
        elif 'hamiltonian' in params:
            ret = vars(params.pop('hamiltonian'))
        else:
            return None

        ret.pop('size')
        if not ret['params']:
            ret.pop('params')

        if 'lattice' in ret and ret['lattice'] is not None:
            ltc = vars(ret.pop('lattice'))
            ltc.pop('dim')
            if not ltc['params']:
                ltc.pop('params')
            ret['lattice'] = ltc
        return ret

    global PARSER_COUNT
    MAX_FILE_NUM = 10000
    t = datetime.datetime.now()

    owd = os.getcwd()
    if 'dir' in params:
        file_dir = params['dir']
        if not os.path.isdir(file_dir):
            os.mkdir(file_dir)
        os.chdir(file_dir)
    else:
        file_dir = '.'

    signature = None
    for i in range(MAX_FILE_NUM):
        signature = t.strftime("%Y-%m-%d") + '-' + str(PARSER_COUNT)
        if os.path.isfile(signature + '.yml'):
            PARSER_COUNT += 1
        else:
            break
    if signature is None:
        raise ValueError('number of configs is too large in current directory')

    if 'filename' in params:
        # TODO: regex match, to remove suffix .yml if there is one
        file_path = params['filename'] + '.yml'
    elif 'filename' not in params:
        file_path = signature + '.yml'
    else:
        raise ValueError('invalid file path')

    if 'device' in params:
        device = params['device']
    elif torch.cuda.is_available():
        device = 'cuda'
    else:
        device = 'cpu'
    # parse each layer

    ham = dump_ham(params)

    if 'model' in params:
        model_path = signature + '.model'
        torch.save(params['model'], model_path)

    configs = {
        'device': device,
        'hamiltonian': ham,
        'model': {'path': model_path},
    }

    if 'figure' in params:
        configs['figure'] = params['figure']

    with open(file_path, 'w') as outfile:
        yaml.dump(configs, outfile, default_flow_style=False)

    os.chdir(owd)
    PARSER_COUNT += 1


def load(f):

    def merge_params(configs):
        if 'params' in configs:
            params = configs.pop('params')
            configs.update(params)

    owd = os.getcwd()
    os.chdir(os.path.dirname(f))
    filename = os.path.basename(f)

    with open(filename, 'r') as infile:
        configs = yaml.load(infile)
        merge_params(configs)
        ham_configs = configs.pop('hamiltonian')
        merge_params(ham_configs)
        ltc_configs = ham_configs.pop('lattice')
        merge_params(ltc_configs)
        model = torch.load(configs['model']['path'])
        ltc = Lattice(ltc_configs.pop('name'), **ltc_configs)
        ham_configs['lattice/tice'] = ltc
        ham = Ham(ham_configs.pop('name'), **ham_configs)

    os.chdir(owd)
    return model, ham


# if __name__ == '__main__':
#     import vmc.ham as ham
#     import torch.nn as nn

#     model = nn.Sequential(
#         nn.Linear(3, 12),
#         nn.Linear(12, 1)
#     )
#     h = ham.TFI(mag=1.0, lattice='chain', length=3)
#     # save(model=model, ham=h, dir='data')
#     model, ham = load('data/2017-09-19-0.yml')
#     print(model, ham)
