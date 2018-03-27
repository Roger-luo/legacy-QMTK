#include <biscuit/bs.h>
#include <gtest/gtest.h>

class TensorTest : public ::testing::Test {
protected:
  void SetUp()
  {
    large = bs::shape(1000000, 2000000);
    small = bs::shape(100, 100);

    t0.reshape(large);
    t1.reshape(large);
  }

  bs::tensor<double> t0;
  bs::tensor<double> t1;
  bs::tensor<double> t2;

  bs::shape large;
  bs::shape small;
};

TEST_F(TensorTest, TestInitial)
{
  EXPECT_EQ(t0._shape, bs::shape(1000, 1000));
}

TEST_F(TensorTest, TestFill)
{
  t0.fill(1.23094);

  bs::iter::index index = bs::make_index(large);
  for(auto i=index.begin(); i!=index.end(); i++)
  {
    EXPECT_DOUBLE_EQ(t0[i], 1.23094);
  }
}

int main(int argc, char **argv)
{
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}