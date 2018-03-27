#ifndef BS_TYPE_TRAIT
#define BS_TYPE_TRAIT

#include "general.hpp"

namespace type
{

template <typename dtype>
struct trait
{
};

#define REGISTER_TYPE_INFO(TYPE, NAME) \
  template <>                          \
  struct trait<TYPE>                   \
  {                                    \
    static const std::string name;     \
  };                                   \
  const std::string trait<TYPE>::name = NAME;

// numerical types
REGISTER_TYPE_INFO(int8_t, "i8")
REGISTER_TYPE_INFO(int16_t, "i16")
REGISTER_TYPE_INFO(int32_t, "i32")
REGISTER_TYPE_INFO(int64_t, "i64")
REGISTER_TYPE_INFO(double, "f64")
REGISTER_TYPE_INFO(float, "f32")
REGISTER_TYPE_INFO(std::complex<float>, "c64")
REGISTER_TYPE_INFO(std::complex<double>, "c128")

} // namespace type
#endif // BS_TYPE_TRAIT