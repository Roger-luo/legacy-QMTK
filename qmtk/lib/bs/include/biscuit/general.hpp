#ifndef BS_GENERAL
#define BS_GENERAL

#include <iostream>
#include <iomanip>
#include <sstream>
#include <string>
#include <vector>
#include <cassert>
#include <memory>
#include <stdexcept>
#include <complex>

#include <cmath>
#include <cstddef>
#include <cstdint>
#include <cstdlib>
#include <cstring>

#define BS_REPR_WIDTH 8
#define BS_REPR_PRECISION 3

#define BSMIN(X, Y) ((X) < (Y) ? (X) : (Y))
#define BSMAX(X, Y) ((X) > (Y) ? (X) : (Y))

#ifdef BS_XINLINE
#error "BS_XINLINE must not be defined"
#endif
#ifdef _MSC_VER
#define BS_FORCE_INLINE __forceinline
#pragma warning(disable : 4068)
#else
#define BS_FORCE_INLINE inline __attribute__((always_inline))
#endif

#ifdef __CUDACC__
#define BS_XINLINE BS_FORCE_INLINE __device__ __host__
#else
#define BS_XINLINE BS_FORCE_INLINE
#endif

#define BS_CINLINE BS_FORCE_INLINE

typedef int64_t index_t;
typedef std::ptrdiff_t dim_t;

inline void runtime_assert(bool cond, std::string msg)
{
  if (!cond)
    throw std::runtime_error(msg.c_str());
}

#ifdef _OPENMP

#include <omp.h>

#ifndef _WIN32
#define PRAGMA(P) _Pragma(#P)
#else
#define PRAGMA(P) __pragma(P)
#endif

#define BS_OMP_OVERHEAD_THRESHOLD 100000

#endif // _OPENMP

#endif