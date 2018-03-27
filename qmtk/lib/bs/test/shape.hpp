#include "general.hpp"

TEST(TestShape, Main) {
  bs::shape s1(2);
  bs::shape s2(2, 2);
  bs::shape s3(2, 2, 2);
  bs::shape s4(2, 2, 2, 2);
  bs::shape s5(s2);
  bs::shape s6(std::move(s3));

  // std::cout<< s6 << std::endl;
}