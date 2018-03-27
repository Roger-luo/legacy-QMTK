#ifndef QMTK_UTILS_INC
#define QMTK_UTILS_INC

#include "general.hpp"

template<typename T>
void n2spin(int n, py::array_t<T> &out) {
  for(int i=0;i<out.size();i++)
    *(out.mutable_data()+i) = (n >> i) & 1;
}

template<typename T>
int spin2n(py::array_t<T> &out) {
  int ret = 0;
  for(int i=0;i<out.size();i++)
    ret += *(out.mutable_data()+i) * (1 << i);
  return ret;
}

#endif // QMTK_UTILS_INC