#include "general.hpp"

TEST(TestIndex, ContiguousLoop) {
  bs::iter::index test_index = bs::make_index(bs::shape(3, 4));

  int k = 0;
  for (auto i = test_index.begin(); i != test_index.end(); i++, k++)
  {
    EXPECT_EQ(k, *i);
  }

  // transpose dose not break memory block
  bs::iter::index test_trans = bs::make_index(bs::shape(3, 4).transpose(1, 0));
  k = 0;
  for (auto i = test_trans.begin(); i != test_trans.end(); i++, k++)
  {
    EXPECT_EQ(k, *i);
  }

  // narrow does not break memory block
  bs::iter::index test_narrow = bs::make_index(bs::shape(5, 6, 7).narrow(1, 0, 2));
  k = 0;
  for (auto i = test_narrow.begin(); i != test_narrow.end(); i++, k++)
    EXPECT_EQ(k, *i);
}

TEST(TestIndex, Break) {
  bs::shape break_shape(5, 6, 7);
  int offsets[35] = {
    0, 1, 2, 3, 4, 30, 31, 32, 33, 34, 60, 61, 62, 63, 64,
    90, 91, 92, 93, 94, 120, 121, 122, 123, 124, 150, 151,
    152, 153, 154, 180, 181, 182, 183, 184
  };

  break_shape.select(1, 0);
  bs::iter::index index = bs::make_index(break_shape);

  int k=0;
  for (auto i = index.begin(); i != index.end(); ++i, ++k)
  {
    EXPECT_EQ(offsets[k], *i);
  }

  --k;
  for (auto i = index.end(); i != index.begin(); --i, --k)
  {
    EXPECT_EQ(offsets[k], *i);
  }
}
