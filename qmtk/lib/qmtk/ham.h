#ifndef QMTK_HAM_INC
#define QMTK_HAM_INC

#include "lattice.h"

namespace qmtk {

class Hamiltonian
{
public:
  Lattice lattice;

  Hamiltonian(Lattice ltc) : lattice(ltc) {};
};

class TFI: public Hamiltonian
{
public:

  double mag;

  TFI(double h, Lattice ltc): Hamiltonian(ltc), mag(h) {};
};

}

#endif