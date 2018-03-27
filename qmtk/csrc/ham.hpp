#ifndef QMTK_HAM_INC
#define QMTK_HAM_INC

#include "lattice.hpp"

template<typename LatticeType>
class Hamiltonian
{
public:
  Hamiltonian(char *name, LatticeType &ltc)
    : _name(name), _lattice(ltc) {};

  char *_name;
  LatticeType _lattice;
};

template<typename LType>
class TFI: public Hamiltonian<LType>
{
public:
  TFI(double mag, LType &ltc)
    : Hamiltonian<LType>("TFI", ltc) {
      lhs = new int[ltc.nElement()];
  };

  ~TFI() {delete []lhs;};

  TFI &iter(py::array &rhs) {
    if(rhs.size() != ltc.nElement())
    {
      std::string msg("configuration size mismatch");
      msg += "expect ";
      ltc.get_shape();
      throw py::value_error(
        "configuration size mismatch"
        "expect "
        );
    }
    for(int i=0;i<rhs.size();i++)
      lhs[i] = *(rhs.data()+i)
  }

  std::tuple<py::array, double> &next() {

  }

  int *lhs;
  double _mag;
};

#endif