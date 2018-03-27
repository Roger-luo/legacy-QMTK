#include "space.hpp"

PYBIND11_MODULE(_space, m) {
  m.doc() = "c++11 implementation for qmtk.space";

  py::class_<Spin<int>>(m, "Spin", pybind11::buffer_protocol())
    .def(py::init<const py::tuple&, int, int, unsigned int, float>())
    .def(py::init<const py::tuple&>())
    .def("randflip", &Spin<int>::randflip)
    .def("flip", &Spin<int>::flip)
    .def("rand_offset", &Spin<int>::rand_offset)
    .def("choose", &Spin<int>::choose)
    .def("rand", &Spin<int>::rand)
    .def("shift", &Spin<int>::shift)
    .def("reset", &Spin<int>::reset)
    .def("__iter__", &Spin<int>::iter)
    .def("__next__", &Spin<int>::next)
    // read and write
    .def_readwrite("up", &Spin<int>::_up)
    .def_readwrite("down", &Spin<int>::_down)
    .def_readwrite("nflips", &Spin<int>::_nflips)
    .def_readwrite("p", &Spin<int>::_p)
    // property
    .def_property("shape", &Spin<int>::get_shape,
      (void (Spin<int>::*)(const py::object&))
      &Spin<int>::set_shape)
    // buffer
    .def_buffer([](Spin<int> &space) -> py::buffer_info {
      std::vector<ssize_t> strides;
      strides.push_back(sizeof(int));
      for(unsigned i=0;i<space._shape.size()-1;i++)
      {
        strides.push_back(sizeof(int) * space._shape[i]);
      }

      return py::buffer_info(
        space._data,
        sizeof(int),
        py::format_descriptor<int>::format(),
        space._shape.size(),
        space._shape, strides);
    });
}