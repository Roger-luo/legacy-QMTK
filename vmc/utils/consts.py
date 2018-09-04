from scipy.sparse import lil_matrix

__all__ = [
    'sigmax',
    'sigmay',
    'sigmaz',
    'iden',
    'sigma',
]

sigmax = lil_matrix([[0, 1], [1, 0]], dtype='complex128')
sigmay = lil_matrix([[0., -1.j], [1.j, 0.]], dtype='complex128')
sigmaz = lil_matrix([[1., 0.], [0., -1.]], dtype='complex128')
iden = lil_matrix([[1., 0.], [0., 1.]], dtype='complex128')

sigma = [iden, sigmax, sigmay, sigmaz]
