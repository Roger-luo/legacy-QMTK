#include "general.hpp"

TEST(TestTensor, Init) {
  bs::tensor<double> a(bs::shape(4, 4));
  bs::tensor<double> b(bs::shape(4, 4));
  bs::tensor<bool> flag(bs::shape(4, 4));

  EXPECT_EQ(a._shape, b._shape);
  EXPECT_EQ(a._shape, flag._shape);
}

TEST(TestTensor, Reshape)
{
  bs::tensor<double> a(bs::shape(1000, 1000));
  EXPECT_EQ(a._shape, bs::shape(1000, 1000));

  a.reshape(bs::shape(10000, 20000));
  EXPECT_EQ(a._shape, bs::shape(10000, 20000));
}

TEST(TestTensor, FillDouble)
{
  bs::tensor<double> a(bs::shape(100, 200));
  a.fill(1.01234);

  bs::iter::index test_index = bs::make_index(bs::shape(100, 200));
  for (auto i = test_index.begin(); i != test_index.end(); i++)
  {
    EXPECT_DOUBLE_EQ(a[i], 1.01234);
  }
}

TEST(TestTensor, FillFloat)
{
  bs::tensor<float> a(bs::shape(100, 200));
  a.fill(1.01234);

  bs::iter::index test_index = bs::make_index(bs::shape(100, 200));
  for (auto i = test_index.begin(); i != test_index.end(); i++)
  {
    EXPECT_FLOAT_EQ(a[i], 1.01234);
  }
}

TEST(TestTensor, FillC128)
{
  bs::tensor<std::complex<double>> a(bs::shape(100, 200));
  a.fill(1.01234);

  bs::iter::index test_index = bs::make_index(bs::shape(100, 200));
  for (auto i = test_index.begin(); i != test_index.end(); i++)
  {
    EXPECT_FLOAT_EQ(std::abs(a[i] - 1.01234), 0.0);
  }
}

TEST(TestTensor, FillC64)
{
  bs::tensor<std::complex<float>> a(bs::shape(100, 200));
  a.fill(1.01234);

  bs::iter::index test_index = bs::make_index(bs::shape(100, 200));
  for (auto i = test_index.begin(); i != test_index.end(); i++)
  {
    EXPECT_FLOAT_EQ(std::abs(a[i] - 1.01234f), 0.0);
  }
}

TEST(TestTensor, Math)
{
  bs::tensor<double> a(bs::shape(100, 200));
  bs::tensor<double> ans(bs::shape(100, 200));
  a.fill(1.01234);

  bs::sin(ans, a);
  std::cout << ans << std::endl;
}
