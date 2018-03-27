#include "lattice.hpp"


#define IMPLEMENT_LATTICE(CLASS, PyNAME) \
    py::class_<CLASS>(m, PyNAME) \
      .def(py::init<>()) \
      .def(py::init<py::tuple &>()) \
      .def("sites", &CLASS::sites) \
      .def("bonds", &CLASS::bonds) \
      .def("neighbors", \
        (std::vector<CLASS::bond> (CLASS::*)(int)) \
        &CLASS::neighbors) \
      .def("neighbors", \
        (std::vector<CLASS::site> (CLASS::*)(const CLASS::site &, int)) \
        &CLASS::neighbors) \
      .def_property("shape", &CLASS::get_shape, &CLASS::set_shape) \
      .def("numel", &CLASS::nElement);


PYBIND11_MODULE(_lattice, m) {
    m.doc() = "quantum lattice c++ module";

    IMPLEMENT_LATTICE(Chain, "ChainBase")
    IMPLEMENT_LATTICE(PBCChain, "PBCChainBase")
    IMPLEMENT_LATTICE(Square, "SquareBase")
    IMPLEMENT_LATTICE(PBCSquare, "PBCSquareBase")
}