#include "site.h"

namespace qmtk {

site::site() {
  _data = nullptr;
  _ndim = 0;
}

site::site(const index_t *data, ssize_t ndim) {
  _data = (index_t *)std::calloc(ndim, sizeof(index_t));
  if (_data == nullptr)
    throw std::bad_alloc();
  _ndim = ndim;

  if(data!=nullptr)
  {
    #pragma simd
    for(ssize_t i=0;i<ndim;i++)
      _data[i] = data[i];
  }
}

site::site(index_t i0)
    : site(nullptr, 1) {
    _data[0] = i0;
}

site::site(index_t i0, index_t i1)
    : site(nullptr, 2) {
    _data[0] = i0;
    _data[1] = i1;
}

site::site(index_t i0, index_t i1, index_t i2)
    : site(nullptr, 3) {
      _data[0] = i0;
      _data[1] = i1;
      _data[2] = i2;
}

site::site(index_t i0, index_t i1, index_t i2, index_t i3)
    : site(nullptr, 4) {
      _data[0] = i0;
      _data[1] = i1;
      _data[2] = i2;
      _data[3] = i3;
}

site::site(const site &other) 
  : site(other._data, other._ndim) {}

site::site(site &&other) {
  _data = other._data;
  _ndim = other._ndim;
  other._data = nullptr;
  other._ndim = 0;
}

site::~site() {std::free(_data);}

site make_site(ssize_t ndim) {
  return site(nullptr, ndim);
}

index_t &site::get(ssize_t index) {
  runtime_assert(index < _ndim, "index out of bound");
  return _data[index];
}

index_t& site::operator[](ssize_t index) {
  return _data[index];
}

const index_t& site::operator[](ssize_t index) const {
  return _data[index];
}

site& site::operator+=(const site &other) {
  // check dimension
  runtime_assert(_ndim==other._ndim, "dimension mismatch");
  #pragma simd
  for(dim_t i=0;i<_ndim;i++)
    _data[i]+=other._data[i];
  return *this;
}

site& site::operator-=(const site &other) {
  // check dimension
  runtime_assert(_ndim==other._ndim, "dimension mismatch");
  #pragma simd
  for(dim_t i=0;i<_ndim;i++)
    _data[i]-=other._data[i];
  return *this;
}

site &site::operator+=(const index_t &other)
{
#pragma simd
  for (dim_t i = 0; i < _ndim; i++)
    _data[i] += other;
  return *this;
}

site &site::operator-=(const index_t &other)
{
#pragma simd
  for (dim_t i = 0; i < _ndim; i++)
    _data[i] -= other;
  return *this;
}

site operator+(const site &lhs, const site &rhs) {
  runtime_assert(lhs._ndim == rhs._ndim, "dimension mismatch");
  site ans = make_site(lhs._ndim);
  #pragma simd
  for(dim_t i=0;i<lhs._ndim;i++)
    ans._data[i] = lhs._data[i] + rhs._data[i];
  return ans;
}

site operator-(const site &lhs, const site &rhs) {
  runtime_assert(lhs._ndim == rhs._ndim, "dimension mismatch");
  site ans = make_site(lhs._ndim);
  #pragma simd
  for (dim_t i = 0; i < lhs._ndim; i++)
    ans._data[i] = lhs._data[i] - rhs._data[i];
  return ans;
}

site operator+(const site &lhs, const index_t &rhs) {
  site ans = make_site(lhs._ndim);
  #pragma simd
  for(dim_t i=0; i< lhs._ndim; i++)
    ans[i] = lhs[i] + rhs;
  return ans;
}

site operator-(const site &lhs, const index_t &rhs) {
  site ans = make_site(lhs._ndim);
#pragma simd
  for (dim_t i = 0; i < lhs._ndim; i++)
    ans[i] = lhs[i] - rhs;
  return ans;
}

site operator+(const index_t &lhs, const site &rhs) {
  return rhs + lhs;
}

site operator-(const index_t &lhs, const site &rhs) {
  return rhs - lhs;
}

bool operator==(const site &lhs, const site &rhs) {
  bool flag = lhs._ndim == rhs._ndim;
  #pragma simd
  for (dim_t i = 0;i < lhs._ndim; i++)
    flag = flag && (lhs._data[i] == rhs._data[i]);
  return flag;
}

bool operator!=(const site &lhs, const site &rhs) {
  return !(lhs==rhs);
}

bool operator==(const site &lhs, const index_t &rhs) {
  bool flag = lhs._ndim == 1;
  return flag && (lhs._data[0] == rhs);
}

bool operator!=(const site &lhs, const index_t &rhs) {
  return !(lhs == rhs);
}

bool operator==(const index_t &lhs, const site &rhs) {
  return rhs == lhs;
}

bool operator!=(const index_t &lhs, const site &rhs) {
  return rhs != lhs;
}

std::ostream &operator<<(std::ostream &os, const site &s) {
  os << "site(";

  for(dim_t i=0;i<s._ndim;i++)
  {
    os << s._data[i];
    if(i!=s._ndim-1)
      os<< ",";
  }
  os << ")";
  return os;
}

} // namespace qmtk