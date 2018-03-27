#ifndef QMTK_LATTICE_INC
#define QMTK_LATTICE_INC

#include "general.hpp"

class Lattice {};

template<typename SiteType>
class LatticeBase: public Lattice {
public:
  using site = SiteType;
  using bond = std::tuple<site, site>;
  std::vector<site> site_cache;
  std::vector<bond> bond_cache;

  virtual std::vector<site>
    sites() = 0;
  virtual std::vector<bond>
    bonds(int nbr) = 0;
  virtual std::vector<bond>
    neighbors(int nbr) = 0;
  virtual std::vector<site>
    neighbors(const site &pos, int nbr) = 0;

  std::vector<site> grid() {
    if(site_cache.size()>0)
      return site_cache;
    else
      site_cache = sites();
  }

  std::vector<bond> grid(int nbr) {
    if(bond_cache.size()>0)
      return bond_cache;
    else
      site_cache = bonds(nbr);
  }

  void clear_cache(int cmd) {
    switch(cmd)
    {
      case 0: site_cache.clear();
      case 1: bond_cache.clear();
      default: return;
    }
  }
};

class Chain : public LatticeBase<int>
{
public:
  using site = Chain::site;
  using bond = Chain::bond;

  Chain(): length(0) {};
  Chain(int shape): length(shape) {};
  Chain(py::tuple &shape): length(py::cast<int>(shape[0])) {};

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

  std::vector<site> neighbors(const site &pos, int nbr) {
    std::vector<int> res;
    if(pos - nbr >= 0)
      res.push_back(pos - nbr);
    if(pos + nbr < length)
      res.push_back(pos + nbr);
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
  PBCChain(py::tuple &shape): Chain(shape) {};

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

  std::vector<site> neighbors(const site &pos, int nbr) {
    std::vector<int> res;
    res.push_back(MOD(pos - nbr, length));
    res.push_back(MOD(pos + nbr, length));
    return res;
  }
};

class Square : public LatticeBase<std::tuple<int, int>>
{
public:

  using site = typename Square::site;
  using bond = typename Square::bond;

  Square()
    :width(0), height(0) {};
  Square(int x, int y)
    :width(x), height(y) {};
  Square(py::tuple &shape)
    : Square(py::cast<int>(shape[0]), py::cast<int>(shape[1])) {};

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

  inline site create_site(int x, int y) {
    return std::make_tuple(x, y);
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

  std::vector<site> even_neighbors(int x, int y, int k) {
    std::vector<site> res;

    if(x+k<width && y+k<height)
      res.push_back(create_site(x+k, y+k));
    if(x-k>=0 && y+k<height)
      res.push_back(create_site(x-k, y+k));
    if(x+k<width && y-k>=0)
      res.push_back(create_site(x+k, y-k));
    if(x-k>=0 && y-k>=0)
      res.push_back(create_site(x-k, y-k));

    return res;
  }

  std::vector<site> odd_neighbors(int x, int y, int k) {
    std::vector<site> res;
    if(x+k<width)
      res.push_back(create_site(x+k, y));
    if(x-k>=0)
      res.push_back(create_site(x-k, y));
    if(y+k<height)
      res.push_back(create_site(x, y+k));
    if(y-k>=0)
      res.push_back(create_site(x, y-k));

    return res;
  }

  std::vector<site> neighbors(const site &s, int nbr) {
    if(nbr%2==0) //even
      return even_neighbors(std::get<0>(s), std::get<1>(s), nbr/2);
    else
      return odd_neighbors(std::get<0>(s), std::get<1>(s), (nbr+1)/2);
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
  PBCSquare(py::tuple &shape): Square(shape) {};

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

  std::vector<site> even_neighbors(int x, int y, int k) {
    std::vector<site> res;

    res.push_back(create_site(MOD(x+k, width), MOD(y+k, height)));
    res.push_back(create_site(MOD(x-k, width), MOD(y+k, height)));
    res.push_back(create_site(MOD(x+k, width), MOD(y-k, height)));
    res.push_back(create_site(MOD(x-k, width), MOD(y-k, height)));
    return res;
  }

  std::vector<site> odd_neighbors(int x, int y, int k) {
    std::vector<site> res;

    res.push_back(create_site(MOD(x+k, width), y));
    res.push_back(create_site(MOD(x-k, width), y));
    res.push_back(create_site(x, MOD(y+k, height)));
    res.push_back(create_site(x, MOD(y-k, height)));
    return res;
  }

  std::vector<site> neighbors(const site &s, int nbr) {
    if(nbr%2==0) //even
      return even_neighbors(std::get<0>(s), std::get<1>(s), nbr/2);
    else
      return odd_neighbors(std::get<0>(s), std::get<1>(s), (nbr+1)/2);
  }
};

#endif // QMTK_LATTICE_INC