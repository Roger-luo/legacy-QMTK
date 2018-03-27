#ifndef QMTK_GENERAL_INC
#define QMTK_GENERAL_INC

#include <tuple>
#include <vector>
#include <set>
#include <random>
#include <string>
#include <iostream>
#include <new>
#include <function>

#include <cstdint>
#include <cstdlib>
#include <cstring>

#define SQUARE(x) (x) * (x)
#define MOD(x, m) (((x) % (m)) + m) % m

namespace qmtk {

typedef int64_t index_t;
typedef std::ptrdiff_t dim_t;

inline void runtime_assert(bool cond, std::string msg) {
  if(!cond) throw std::runtime_error(msg.c_str());
}

}
#endif // QMTK_GENERAL_INC