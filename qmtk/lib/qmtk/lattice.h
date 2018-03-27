#ifndef QMTK_LATTICE_INC
#define QMTK_LATTICE_INC

#include "site.h"

namespace qmtk {

class Lattice {
public:
  site_list site_cache;
  bond_list bond_cache;

  virtual site_list sites() = 0;
  virtual bond_list bonds(int nbr) = 0;
  virtual bond_list neighbors(int nbr) = 0;
  virtual site_list neighbors(const site &pos, int nbr) = 0;
  virtual int nElement() const = 0;

  site_list grid() {
    if(site_cache.size() > 0)
      return site_cache;
    else
      site_cache = sites();
    return site_cache;
  }

  bond_list grid(int nbr) {
    if(bond_cache.size() > 0)
      return bond_cache;
    else
      bond_cache = bonds(nbr);
    return bond_cache;
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

class Chain: public Lattice
{
public:
  int length;

  Chain(): length(0) {};
  Chain(int shape): length(shape) {};

  site_list sites();
  bond_list bonds(int nbr);
  bond_list neighbors(int nbr);
  site_list neighbors(const site &pos, int nbr);

  int nElement() const;
};

class PBCChain: public Chain
{
public:
  PBCChain(): Chain() {};
  PBCChain(int shape): Chain(shape) {};

  bond_list bonds(int nbr);
  bond_list neighbors(int nbr);
  site_list neighbors(const site &pos, int nbr);
};

class Square: public Lattice
{
public:
  int width, height;

  Square(): width(0), height(0) {};
  Square(int x, int y): width(x), height(y) {};

  site_list sites();
  bond_list bonds(int nbr);
  bond_list odd_bonds(int k);
  bond_list even_bonds(int k);

  bond_list neighbors(int nbr);
  bond_list odd_neighbors(int k);
  bond_list even_neighbors(int k);

  site_list neighbors(const site &pos, int nbr);
  site_list odd_neighbors(const site &pos, int k);
  site_list even_neighbors(const site &pos, int k);

  int nElement() const;
};

class PBCSquare: public Square
{
public:

  PBCSquare(): Square() {};
  PBCSquare(int x, int y): Square(x, y) {};

  bond_list odd_bonds(int k);
  bond_list even_bonds(int k);

  bond_list odd_neighbors(int k);
  bond_list even_neighbors(int k);

  site_list odd_neighbors(const site &pos, int k);
  site_list even_neighbors(const site &pos, int k);
};

} // namespace qmtk
#endif