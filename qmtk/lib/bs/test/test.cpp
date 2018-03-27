#include "general.hpp"

#include "shape.hpp"
#include "index.hpp"
#include "container.hpp"
#include "storage.hpp"
#include "tensor.hpp"

int main(int argc, char **argv) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}