import numpy as np
import qmtk._utils as _utils


def n2spin(n, shape):
    """convert a integer to spin.
    """
    spin = np.zeros(shape)
    _utils.n2spin(n, spin)
    return spin


spin2n = _utils.spin2n
