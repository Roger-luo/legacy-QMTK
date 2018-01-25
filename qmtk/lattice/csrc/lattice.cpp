#include<tuple>
#include<pybind11/pybind11.h>
#include<pybind11/stl.h>

#define SQUARE(x) (x) * (x)
#define MOD(x, m) (((x) % (m)) + m) % m

namespace py = pybind11;


class Chain
{
public:
  using site = int;
  using bond = std::tuple<int, int>;

  Chain(): length(0) {};
  Chain(int shape): length(shape) {};

  std::vector<site> sites() {
    std::vector<int> res;
    for(int i=0;i<length;i++) {
      res.push_back(i);
    }
    return res;
  };

  std::vector<bond> bonds(int nbr) {
    std::vector<bond> res;

    for(int i=0;i<length - nbr; i++)
    {
      res.push_back(std::make_tuple(i, i + nbr));
    }
    return res;
  }

  std::vector<bond> neighbors(int nbr) {
    std::vector<bond> res;

    // begin
    for(int i=0;i<nbr;i++)
      res.push_back(std::make_tuple(i, i + nbr));
    // middle
    for(int i=nbr;i<length - nbr; i++)
    {
      res.push_back(std::make_tuple(i, i - nbr));
      res.push_back(std::make_tuple(i, i + nbr));
    }

    for(int i=length - nbr; i<length; i++)
    {
      res.push_back(std::make_tuple(i, i - nbr));
    }
    return res;
  }

  inline std::tuple<int> get_shape() {
    return std::make_tuple(length);
  }

  inline void set_shape(int n) {
    length = n;
  }

  inline int nElement() {
    return length;
  }

  int length;
};


class PBCChain: public Chain
{
public:
  PBCChain() : Chain() {};
  PBCChain(int shape) : Chain(shape) {};

  std::vector<bond> bonds(int nbr) {
    std::vector<bond> res;

    for(int i=0;i<length; i++)
    {
      res.push_back(std::make_tuple(i, MOD(i + nbr, length)));
    }
    return res;
  }

  std::vector<bond> neighbors(int nbr) {
    std::vector<bond> res;

    for(int i=0;i<length; i++)
    {
      res.push_back(std::make_tuple(i, MOD(i - nbr, length)));
      res.push_back(std::make_tuple(i, MOD(i + nbr, length)));
    }

    return res;
  }
};

class Square
{
public:
  using site = std::tuple<int, int>;
  using bond = std::tuple<site, site>;

  Square()
    :width(0), height(0) {};

  Square(int x, int y)
    :width(x), height(y) {};

  std::vector<site> sites() {
    std::vector<site> res;

    for(int i=0;i<width;i++)
    {
      for(int j=0;j<height;j++)
      {
        res.push_back(std::make_tuple(i, j));
      }
    }
    return res;
  }

  // nbr = 2 * k - 1
  inline std::vector<bond> odd_bonds(int k) {
    std::vector<bond> res;

    for(int i=0;i<width;i++)
    {
      for(int j=0;j<height-k;j++)
        res.push_back(create_bond(i, j, i, j+k));
    }

    for(int j=0;j<height;j++)
    {
      for(int i=0;i<width - k;i++)
        res.push_back(create_bond(i, j, i+k, j));
    }
    return res;
  }

  // nbr = 2 * k
  inline std::vector<bond> even_bonds(int k) {
    std::vector<bond> res;

    for(int i=0;i<width-k;i++) {
      for(int j=0;j<height-k;j++) {
        res.push_back(create_bond(i, j, i+k, j+k));
        res.push_back(create_bond(i, j+k, i+k, j));
      }
    }

    return res;
  }

  std::vector<bond> bonds(int nbr) {
    if(nbr%2==0) //even
      return even_bonds(nbr/2);
    else
      return odd_bonds((nbr+1)/2);
  }

  inline bond create_bond(int x1, int y1, int x2, int y2) {
    return std::make_tuple(
      std::make_tuple(x1, y1), std::make_tuple(x2, y2));
  }

  inline std::vector<bond> odd_neighbors(int k) {
    std::vector<bond> res;

    for(int i=0;i<width;i++) {
      for(int j=0;j<height;j++) {
        if(i+k<width)
          res.push_back(create_bond(i, j, i+k, j));
        if(i-k>=0)
          res.push_back(create_bond(i, j, i-k, j));
        if(j+k<height)
          res.push_back(create_bond(i, j, i, j+k));
        if(j-k>=0)
          res.push_back(create_bond(i, j, i, j-k));
      }
    }
    return res;
  }

  inline std::vector<bond> even_neighbors(int k) {
    std::vector<bond> res;

    for(int i=0;i<width;i++) {
      for(int j=0;j<height;j++) {
        if(i+k<width && j+k<height)
          res.push_back(create_bond(i, j, i+k, j+k));
        if(i-k>=0 && j+k<height)
          res.push_back(create_bond(i, j, i-k, j+k));
        if(i+k<width && j-k>=0)
          res.push_back(create_bond(i, j, i+k, j-k));
        if(i-k>=0 && j-k>=0)
          res.push_back(create_bond(i, j, i-k, j-k));
      }
    }
    return res;
  }

  std::vector<bond> neighbors(int nbr) {
    if(nbr%2==0) //even
      return even_neighbors(nbr/2);
    else
      return odd_neighbors((nbr+1)/2);
  }

  inline std::tuple<int, int> get_shape() {
    return std::make_tuple(width, height);
  }

  inline void set_shape(const std::tuple<int, int> &shape) {
    width = std::get<0>(shape);
    height = std::get<1>(shape);
  }

  inline int nElement() {
    return width * height;
  }

  int width;
  int height;
};


class PBCSquare: public Square
{
public:
  PBCSquare(): Square() {};
  PBCSquare(int x, int y): Square(x, y) {};

  // nbr = 2 * k - 1
  inline std::vector<bond> odd_bonds(int k) {
    std::vector<bond> res;

    for(int i=0;i<width;i++)
    {
      for(int j=0;j<height;j++)
      {
        res.push_back(create_bond(i, j, MOD(i+k, width), j));
        res.push_back(create_bond(i, j, i, MOD(j+k, height)));
      }
    }

    return res;
  }

  // nbr = 2 * k
  inline std::vector<bond> even_bonds(int k) {
    std::vector<bond> res;

    for(int i=0;i<width;i++) {
      for(int j=0;j<height;j++) {
        res.push_back(create_bond(i, j, MOD(i+k, width), MOD(j+k, height)));
        res.push_back(create_bond(i, MOD(j+k, height), MOD(i+k, width), j));
      }
    }

    return res;
  }

  std::vector<bond> bonds(int nbr) {
    if(nbr%2==0) //even
      return even_bonds(nbr/2);
    else
      return odd_bonds((nbr+1)/2);
  }

  inline std::vector<bond> odd_neighbors(int k) {
    std::vector<bond> res;

    for(int i=0;i<width;i++) {
      for(int j=0;j<height;j++) {
        res.push_back(create_bond(i, j, MOD(i+k, width), j));
        res.push_back(create_bond(i, j, MOD(i-k, width), j));
        res.push_back(create_bond(i, j, i, MOD(j+k, height)));
        res.push_back(create_bond(i, j, i, MOD(j-k, height)));
      }
    }
    return res;
  }

  inline std::vector<bond> even_neighbors(int k) {
    std::vector<bond> res;

    for(int i=0;i<width;i++) {
      for(int j=0;j<height;j++) {
        res.push_back(create_bond(i, j, MOD(i+k, width), MOD(j+k, height)));
        res.push_back(create_bond(i, j, MOD(i-k, width), MOD(j+k, height)));
        res.push_back(create_bond(i, j, MOD(i+k, width), MOD(j-k, height)));
        res.push_back(create_bond(i, j, MOD(i-k, width), MOD(j-k, height)));
      }
    }
    return res;
  }

  std::vector<bond> neighbors(int nbr) {
    if(nbr%2==0) //even
      return even_neighbors(nbr/2);
    else
      return odd_neighbors((nbr+1)/2);
  }
};


PYBIND11_MODULE(_lattice, m) {
    m.doc() = "quantum lattice c++ module";

    py::class_<Chain>(m, "ChainBase")
      .def(py::init<>())
      .def(py::init<int>())
      .def_readwrite("shape", &Chain::length)
      .def("sites", &Chain::sites)
      .def("bonds", &Chain::bonds)
      .def("neighbors", &Chain::neighbors)
      .def_property("shape", &Chain::get_shape, &Chain::set_shape)
      .def("numel", &Chain::nElement);

    py::class_<PBCChain>(m, "PBCChainBase")
      .def(py::init<>())
      .def(py::init<int>())
      .def_readwrite("shape", &PBCChain::length)
      .def("sites", &PBCChain::sites)
      .def("bonds", &PBCChain::bonds)
      .def("neighbors", &PBCChain::neighbors)
      .def_property("shape", &PBCChain::get_shape, &PBCChain::set_shape)
      .def("numel", &PBCChain::nElement);

    py::class_<Square>(m, "SquareBase")
      .def(py::init<>())
      .def(py::init<int, int>())
      .def_readwrite("width", &Square::width)
      .def_readwrite("height", &Square::height)
      .def("sites", &Square::sites)
      .def("bonds", &Square::bonds)
      .def("neighbors", &Square::neighbors)
      .def_property("shape", &Square::get_shape, &Square::set_shape)
      .def("numel", &Square::nElement);

    py::class_<PBCSquare>(m, "PBCSquareBase")
      .def(py::init<>())
      .def(py::init<int, int>())
      .def_readwrite("width", &PBCSquare::width)
      .def_readwrite("height", &PBCSquare::height)
      .def("sites", &PBCSquare::sites)
      .def("bonds", &PBCSquare::bonds)
      .def("neighbors", &PBCSquare::neighbors)
      .def_property("shape", &PBCSquare::get_shape, &PBCSquare::set_shape)
      .def("numel", &PBCSquare::nElement);
}