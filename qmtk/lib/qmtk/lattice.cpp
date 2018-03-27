#include "lattice.h"

namespace qmtk {

site_list Chain::sites() {
  site_list res;
#pragma simd
  for (int i = 0; i < length; i++)
    res.push_back(site(i));
  return res;
}

bond_list Chain::bonds(int nbr) {
  bond_list res;
  for (int i = 0; i < length - nbr; i++)
    res.push_back(make_bond(i, i + nbr));
  return res;
}

bond_list Chain::neighbors(int nbr) {
  bond_list res;
  // begin
  for (int i = 0; i < nbr; i++)
    res.push_back(make_bond(i, i + nbr));
  // middle
  for (int i = nbr; i < length - nbr; i++)
  {
    res.push_back(make_bond(i, i - nbr));
    res.push_back(make_bond(i, i + nbr));
  }

  for(int i=length-nbr;i<length;i++)
    res.push_back(make_bond(i, i - nbr));
  return res;
}

site_list Chain::neighbors(const site &pos, int nbr) {
  site_list res;
  if(pos[0] - nbr >= 0)
    res.push_back(site(pos[0] - nbr));
  if(pos[0] + nbr < length)
    res.push_back(site(pos[0] + nbr));
  return res;
}

int Chain::nElement() const {
  return length;
}

bond_list PBCChain::bonds(int nbr) {
  bond_list res;
  for(int i=0;i<length;i++)
    res.push_back(make_bond(i, MOD(i + nbr, length)));
  return res;
}

bond_list PBCChain::neighbors(int nbr) {
  bond_list res;
  for(int i=0;i<length;i++)
  {
    res.push_back(make_bond(i, MOD(i - nbr, length)));
    res.push_back(make_bond(i, MOD(i + nbr, length)));
  }
  return res;
}

site_list PBCChain::neighbors(const site &pos, int nbr) {
  site_list res;
  res.push_back(site(MOD(pos[0] - nbr, length)));
  res.push_back(site(MOD(pos[0] + nbr, length)));
  return res;
}

site_list Square::sites() {
  site_list res;
  for(int i=0;i<width;i++)
  {
    for(int j=0;j<height;j++)
      res.push_back(site(i, j));
  }
  return res;
}

// nbr = 2 * k - 1
bond_list Square::odd_bonds(int k)
{
  bond_list res;

  for(int i=0;i<width;i++)
  {
    for(int j=0;j<height;j++)
      res.push_back(make_bond(i, j, i, j+k));
  }

  for(int j=0;j < height;j++)
  {
    for(int i=0; i < width - k; i++)
      res.push_back(make_bond(i, j, i+k, j));
  }
  return res;
}

bond_list Square::even_bonds(int k)
{
  bond_list res;
  for(int i=0;i<width-k;i++)
  {
    for(int j=0;j<height - k;j++)
    {
      res.push_back(make_bond(i, j, i+k, j+k));
      res.push_back(make_bond(i, j+k, i+k, j));
    }
  }

  return res;
}

bond_list Square::bonds(int nbr)
{
  if(nbr%2 == 0) // even
    return even_bonds(nbr/2);
  else
    return odd_bonds((nbr+1) / 2);
}

bond_list Square::odd_neighbors(int k) {
  bond_list res;
  for(int i=0;i<width;i++)
  {
    for(int j=0;j<height;j++)
    {
      if (i + k < width)
        res.push_back(make_bond(i, j, i + k, j));
      if (i - k >= 0)
        res.push_back(make_bond(i, j, i - k, j));
      if (j + k < height)
        res.push_back(make_bond(i, j, i, j + k));
      if (j - k >= 0)
        res.push_back(make_bond(i, j, i, j - k));
    }
  }

  return res;
}

bond_list Square::even_neighbors(int k)
{
  bond_list res;
  for(int i=0;i<width;i++)
  {
    for(int j=0;j<height;j++)
    {
      if (i + k < width && j + k < height)
        res.push_back(make_bond(i, j, i + k, j + k));
      if (i - k >= 0 && j + k < height)
        res.push_back(make_bond(i, j, i - k, j + k));
      if (i + k < width && j - k >= 0)
        res.push_back(make_bond(i, j, i + k, j - k));
      if (i - k >= 0 && j - k >= 0)
        res.push_back(make_bond(i, j, i - k, j - k));
    }
  }
  return res;
}


bond_list Square::neighbors(int nbr) {
  if(nbr%2==0)
    return even_neighbors(nbr/2);
  else
    return odd_neighbors((nbr+1)/2);
}

site_list Square::even_neighbors(const site &pos, int k)
{
  site_list res;
  if (pos[0] + k < width && pos[1] + k < height)
    res.push_back(site(pos[0] + k, pos[1] + k));
  if (pos[0] - k >= 0 && pos[1] + k < height)
    res.push_back(site(pos[0] - k, pos[1] + k));
  if (pos[0] + k < width && pos[1] - k >= 0)
    res.push_back(site(pos[0] + k, pos[1] - k));
  if (pos[0] - k >= 0 && pos[1] - k >= 0)
    res.push_back(site(pos[0] - k, pos[1] - k));
  return res;
}

site_list Square::odd_neighbors(const site &pos, int k)
{
  site_list res;
  if (pos[0] + k < width)
    res.push_back(site(pos[0] + k, pos[1]));
  if (pos[0] - k >= 0)
    res.push_back(site(pos[0] - k, pos[1]));
  if (pos[1] + k < height)
    res.push_back(site(pos[0], pos[1] + k));
  if (pos[1] - k >= 0)
    res.push_back(site(pos[0], pos[1] - k));

  return res;
}

site_list Square::neighbors(const site &s, int nbr)
{
  if (nbr % 2 == 0) //even
    return even_neighbors(s, nbr / 2);
  else
    return odd_neighbors(s, (nbr + 1) / 2);
}

int Square::nElement() const {
  return width * height;
}

bond_list PBCSquare::odd_bonds(int k)
{
  bond_list res;
  for(int i=0;i<width;i++)
  {
    for(int j=0;j<height;j++)
    {
      res.push_back(make_bond(i, j, MOD(i+k, width), j));
      res.push_back(make_bond(i, j, i, MOD(j+k, height)));
    }
  }
  return res;
}

bond_list PBCSquare::even_bonds(int k)
{
  bond_list res;
  for(int i=0;i<width;i++)
  {
    for(int j=0;j<height;j++)
    {
      res.push_back(make_bond(i, j, MOD(i+k, width), MOD(j+k, height)));
      res.push_back(make_bond(i, MOD(j+k, height), MOD(i+k, width), j));
    }
  }
  return res;
}

bond_list PBCSquare::odd_neighbors(int k) {
  bond_list res;

  for (int i = 0; i < width; i++)
  {
    for (int j = 0; j < height; j++)
    {
      res.push_back(make_bond(i, j, MOD(i + k, width), j));
      res.push_back(make_bond(i, j, MOD(i - k, width), j));
      res.push_back(make_bond(i, j, i, MOD(j + k, height)));
      res.push_back(make_bond(i, j, i, MOD(j - k, height)));
    }
  }
  return res;
}

bond_list PBCSquare::even_neighbors(int k) {
  bond_list res;

  for(int i=0;i < width;i++)
  {
    for(int j=0;j < height;j++)
    {
      res.push_back(make_bond(i, j, MOD(i + k, width), MOD(j + k, height)));
      res.push_back(make_bond(i, j, MOD(i - k, width), MOD(j + k, height)));
      res.push_back(make_bond(i, j, MOD(i + k, width), MOD(j - k, height)));
      res.push_back(make_bond(i, j, MOD(i - k, width), MOD(j - k, height)));
    }
  }
  return res;
}

site_list PBCSquare::odd_neighbors(const site &pos, int k)
{
  site_list res;
  res.push_back(site(MOD(pos[0] + k, width), MOD(pos[1] + k, height)));
  res.push_back(site(MOD(pos[0] - k, width), MOD(pos[1] + k, height)));
  res.push_back(site(MOD(pos[0] + k, width), MOD(pos[1] - k, height)));
  res.push_back(site(MOD(pos[0] - k, width), MOD(pos[1] - k, height)));
  return res;
}

site_list PBCSquare::even_neighbors(const site &pos, int k)
{
  site_list res;
  res.push_back(site(MOD(pos[0] + k, width), pos[1]));
  res.push_back(site(MOD(pos[0] - k, width), pos[1]));
  res.push_back(site(pos[0], MOD(pos[1] + k, height)));
  res.push_back(site(pos[0], MOD(pos[1] - k, height)));
  return res;
}

} // namespace qmtk
