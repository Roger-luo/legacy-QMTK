#ifndef BS_OPERATORS_INC
#define BS_OPERATORS_INC

#include "general.hpp"

namespace  op {

struct base {
};

/**
 * @brief operators that assign to dst.
 * 
 */
struct saver: public base {
  template <typename dtype>
  BS_XINLINE static void to(dtype &dst, const dtype &src) {};
};

namespace sv {

struct assign: public saver {
  template <typename dtype>
  BS_XINLINE static void to(dtype &dst, const dtype &src)
  {
    dst = src;
  }
};

struct add: public saver {
  template <typename dtype>
  BS_XINLINE static void to(dtype &dst, const dtype &src)
  {
    dst += src;
  }
};

struct minus: public saver {
  template <typename dtype>
  BS_XINLINE static void to(dtype &dst, const dtype &src)
  {
    dst -= src;
  }
};

struct mul: public saver {
  template <typename dtype>
  BS_XINLINE static void to(dtype &dst, const dtype &src)
  {
    dst *= src;
  }
};

struct div: public saver {
  template <typename dtype>
  BS_XINLINE static void to(dtype &dst, const dtype &src)
  {
    dst /= src;
  }
};

} // namespace sv

/**
 * @brief binary operators, operators that can assign
 * to and map to. has to methods
 * 
 * static dtype map
 */
struct binary: public base {
  template <typename dtype>
  BS_XINLINE dtype map(dtype &a, dtype &b) {};
};

namespace bi {

struct add: public binary {
  template <typename dtype>
  BS_XINLINE dtype map(dtype &a, dtype &b)
  {
    return a + b;
  }
};

struct minus: public binary {
  template <typename dtype>
  BS_XINLINE dtype map(dtype &a, dtype &b)
  {
    return a - b;
  }
};

struct mul: public binary {
  template <typename dtype>
  BS_XINLINE dtype map(dtype &a, dtype &b)
  {
    return a * b;
  }
};

struct div: public binary {
  template <typename dtype>
  BS_XINLINE dtype map(dtype &a, dtype &b)
  {
    return a / b;
  }
};

struct eq: public binary {
  template <typename dtype>
  BS_XINLINE bool map(dtype &a, dtype &b)
  {
    return a == b;
  }
};

struct neq: public binary {
  template <typename dtype>
  BS_XINLINE bool map(dtype &a, dtype &b)
  {
    return a != b;
  }
};

struct ge: public binary {
  template <typename dtype>
  BS_XINLINE bool map(dtype &a, dtype &b)
  {
    return a > b;
  }
};

struct le: public binary {
  template <typename dtype>
  BS_XINLINE bool map(dtype &a, dtype &b)
  {
    return a < b;
  }
};

struct geq: public binary {
  template <typename dtype>
  BS_XINLINE bool map(dtype &a, dtype &b)
  {
    return a >= b;
  }
};

struct leq: public binary {
  template <typename dtype>
  BS_XINLINE bool map(dtype &a, dtype &b)
  {
    return a <= b;
  }
};

} // namespace bi

/**
 * @brief mapper operators, operators that maps source value
 * to target value. including all functions with one dependencies.
 * 
 * static dtype map(dtype &src);
 */
struct mapper: public base {
  template <typename dtype>
  BS_XINLINE static dtype map(dtype &src) {};
};

#define IMPLEMENT_BASIC_MATH(CFUNC)               \
  struct CFUNC : public mapper                    \
  {                                               \
    template <typename dtype>                     \
    BS_XINLINE static dtype map(const dtype &src) \
    {                                             \
      return std::CFUNC(src);                     \
    };                                            \
  };

IMPLEMENT_BASIC_MATH(cos)
IMPLEMENT_BASIC_MATH(sin)
IMPLEMENT_BASIC_MATH(tan)
IMPLEMENT_BASIC_MATH(acos)
IMPLEMENT_BASIC_MATH(asin)
IMPLEMENT_BASIC_MATH(atan)
IMPLEMENT_BASIC_MATH(atan2) // real only

// Hyperbolic functions
IMPLEMENT_BASIC_MATH(cosh)
IMPLEMENT_BASIC_MATH(sinh)
IMPLEMENT_BASIC_MATH(tanh)
IMPLEMENT_BASIC_MATH(acosh)
IMPLEMENT_BASIC_MATH(asinh)
IMPLEMENT_BASIC_MATH(atanh)

// Exponential and logarithmic functions
IMPLEMENT_BASIC_MATH(exp)
IMPLEMENT_BASIC_MATH(log)
IMPLEMENT_BASIC_MATH(log10)
IMPLEMENT_BASIC_MATH(modf)
IMPLEMENT_BASIC_MATH(exp2)
IMPLEMENT_BASIC_MATH(expm1)
IMPLEMENT_BASIC_MATH(log1p)
IMPLEMENT_BASIC_MATH(log2)
IMPLEMENT_BASIC_MATH(sqrt)

// partial

// complex
struct abs: public mapper
{
  template <typename dtype>
  BS_XINLINE static dtype map(dtype &src)
  {
    return abs(src);
  }

  template <typename dtype>
  BS_XINLINE static dtype map(std::complex<dtype> &src)
  {
    return abs(src);
  }
};
} // namespace op

#endif // BS_OPERATORS_INC