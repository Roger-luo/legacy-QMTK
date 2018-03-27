#include "shape.h"

namespace qmtk {

shape::shape()
{
  _sizes = nullptr;
  _strides = nullptr;
  _ndim = 0;
  total_size = 0;
}

shape::shape(const index_t *sizes, const index_t *strides, dim_t ndim)
{
  // get total size
  total_size = 1;
  for(int i=0;i<ndim;i++)
    total_size *= sizes[i];
  _ndim = ndim;

  _sizes = (index_t *)std::malloc(sizeof(index_t) * ndim);
  _strides = (index_t *)std::malloc(sizeof(index_t) * ndim);
  if(_sizes==nullptr || _strides==nullptr)
    throw std::bad_alloc();

  // size could be null
  if(sizes!=nullptr)
  {
    for (int i = 0; i < ndim; i++)
      _sizes[i] = sizes[i];
  }    

  // strides could be null
  if(strides!=nullptr)
  {
    for(int i=0;i<ndim;i++)
      _strides[i] = strides[i];
  }
  else // calculate stride
  {
    _strides[0] = 1;
    for(int i=1;i<ndim;i++)
      _strides[i] = _sizes[i-1];
  }
}

shape::shape(index_t i0)
  :shape(nullptr, nullptr, 1)
{
  _sizes[0] = i0; _strides[0] = 1;
}

shape::shape(index_t i0, index_t i1)
  :shape(nullptr, nullptr, 2)
{
  _sizes[0] = i0; _strides[0] = 1;
  _sizes[1] = i1; _strides[1] = i0;
}

shape::shape(index_t i0, index_t i1, index_t i2)
  :shape(nullptr, nullptr, 3)
{
  _sizes[0] = i0; _strides[0] = 1;
  _sizes[1] = i1; _strides[1] = i0;
  _sizes[2] = i2; _strides[2] = i1;
}

shape::shape(index_t i0, index_t i1, index_t i2, index_t i3)
  :shape(nullptr, nullptr, 4)
{
  _sizes[0] = i0; _strides[0] = 1;
  _sizes[1] = i1; _strides[1] = i0;
  _sizes[2] = i2; _strides[2] = i1;
  _sizes[3] = i3; _strides[3] = i2;
}

shape::shape(const shape &other)
  : shape(other._sizes, other._strides, other._ndim) {}

shape::shape(shape &&other) {
  _sizes = other._sizes;
  _strides = other._strides;
  _ndim = other._ndim;
  total_size = other.total_size;

  other._sizes = nullptr;
  other._strides = nullptr;
  other._ndim = 0;
  other.total_size = 0;
}

shape::~shape() {
  std::free(_sizes);
  std::free(_strides);
}

dim_t shape::size() const {
  return total_size;
}

dim_t shape::ndim() const {
  return _ndim;
}

const index_t& shape::operator[](dim_t index) const {
  return _sizes[index];
}

bool operator==(const shape &lhs, const shape &rhs) {
  if(lhs.size() != rhs.size())
    return false;

  if(lhs.ndim() != rhs.ndim())
    return false;

  for(int i=0;i<rhs.ndim();i++)
  {
    if (lhs[i] != rhs[i])
      return false;
  }
  return true;
}

bool operator!=(const shape &lhs, const shape &rhs) {
  return !(lhs == rhs);
}

} // namespace qmtk
