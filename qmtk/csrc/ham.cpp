#define FORCE_IMPORT_ARRAY

#include "pybind11/pybind11.h"
#include "xtensor-python/pycontainer.hpp"
#include "xtensor-python/pyvectorize.hpp"
#include <numeric>
#include <cmath>

namespace py = pybind11;

double scalar_func(double i, double j)
{
  return std::sin(i) - std::cos(j);
}

PYBIND11_MODULE(_ham, m)
{
  xt::import_numpy();
  m.doc() = "Test module for xtensor python bindings";

  m.def("vectorized_func", xt::pyvectorize(scalar_func), "");
}