#include "general.hpp"

TEST(TestContainer, Main) {
  bs::container<double> X0(bs::shape(2, 2));
  bs::container<double> X1(bs::shape(2, 2));

  X0.reshape(bs::shape(4, 4));
  EXPECT_EQ(X0._shape, bs::shape(4, 4));
}
