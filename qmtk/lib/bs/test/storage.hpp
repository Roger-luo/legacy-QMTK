#include "general.hpp"

TEST(TestStorage, Main) {
  bs::storage<double> storage(10);

  for(int i=0;i<10;i++)
  {
    storage[i] = i;
  }

  for(int i=0;i<10;i++)
    EXPECT_EQ(storage[i], i);

  storage.resize(20);

  EXPECT_EQ(storage.size(), 20);
}
