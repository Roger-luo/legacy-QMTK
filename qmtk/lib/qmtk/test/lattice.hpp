#ifndef QMTK_TEST_LATTICE
#define QMTK_TEST_LATTICE

#include "general.hpp"

TEST(LatticeTest, TestChainSites) {
  qmtk::Chain chain(10);
  qmtk::site_list test_site_list = chain.sites();
  int k = 0;
  for (auto i = test_site_list.begin(); i != test_site_list.end(); i++, k++)
    EXPECT_EQ((*i)[0], k);
}

TEST(LatticeTest, TestChainBonds) {
  qmtk::Chain chain(10);
  qmtk::bond_list test_bond_list = chain.bonds(1);
  int k = 0;
  for (auto i = test_bond_list.begin(); i != test_bond_list.end(); i++, k++)
    EXPECT_EQ(*i, qmtk::make_bond(k, k + 1));
}

#endif