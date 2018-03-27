#ifndef QMTK_GENERAL_INC
#define QMTK_GENERAL_INC

#include <tuple>
#include <vector>
#include <set>
#include <random>
#include <cstdlib>
#include <string>
#include <iostream>

#include <pybind11/pybind11.h>
#include <pybind11/pytypes.h>
#include <pybind11/numpy.h>
#include <pybind11/cast.h>
#include <pybind11/stl.h>

namespace py = pybind11;

#define SQUARE(x) (x) * (x)
#define MOD(x, m) (((x) % (m)) + m) % m


#endif // QMTK_GENERAL_INC