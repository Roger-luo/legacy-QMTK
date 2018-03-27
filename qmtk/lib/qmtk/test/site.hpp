#ifndef QMTK_TEST_SITE
#define QMTK_TEST_SITE

#include "general.hpp"

TEST(SiteTest, MainTest) {
  qmtk::site a(2, 2, 2);
  qmtk::site b(3, 2, 1);
  qmtk::site minus(-1, 0, 1);
  qmtk::site plus(5, 4, 3);

  EXPECT_EQ(plus, a + b);
  EXPECT_EQ(minus, a - b);
}

TEST(SiteTest, ScalarTest) {
  qmtk::site a(2);
  qmtk::site b(3, 1, 2, 4);
  qmtk::site ans(2, 0, 1, 3);

  EXPECT_EQ(a + 3, 5);
  EXPECT_EQ(a - 3, -1);
  
  EXPECT_EQ(b - 1, ans);
}

#endif