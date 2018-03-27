import numpy as np
from ham import local_hamilton, Hamiltonian
from qmtk.lattice import Square

lc0 = local_hamilton("X Z Z Y", [0, 1, 2, 5])
lc1 = local_hamilton("X,Z,Z,Y", [0, 1, 2, 5])
lc2 = local_hamilton("X_1 Z_2 Z_2 Y_5")

lattice = Square(shape=(5, 5))
configs = np.random.randint(0, high=2, size=lattice)
h = Hamiltonian('X_0,Z_1,Z_2', lattice=lattice)
for val, lhs in h(configs):
    pass
