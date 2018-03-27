#include "utils.hpp"


PYBIND11_MODULE(_utils, m) {
  m.doc() = "utils in c++11";

  m.def("n2spin", &n2spin<int>);
  m.def("n2spin", &n2spin<long>);
  m.def("n2spin", &n2spin<float>);
  m.def("n2spin", &n2spin<double>);

  m.def("spin2n", &spin2n<int>);
  m.def("spin2n", &spin2n<long>);
  m.def("spin2n", &spin2n<float>);
  m.def("spin2n", &spin2n<double>);
}