#include "shape.hpp"

namespace bs
{

inline void shape::init(index_t padding, const index_t *ids, const index_t *sizes, const index_t *strides, dim_t ndim)
{
  _ndim = ndim;
  _offset = padding;
  minMissingId = -1;

  _ids = (index_t *)std::malloc(sizeof(index_t) * ndim);
  _sizes = (index_t *)std::malloc(sizeof(index_t) * ndim);
  _strides = (index_t *)std::malloc(sizeof(index_t) * ndim);
  if (_sizes == nullptr || _strides == nullptr)
    throw std::bad_alloc();

  // if ids is null, we will asign it
  // by order.
  if (ids == nullptr)
  {
    for (int i = 0; i < ndim; i++)
      _ids[i] = i;
  }
  else
  {
    for (int i = 0; i < ndim; i++)
      _ids[i] = ids[i];
  }

  // size could be null
  if (sizes != nullptr)
  {
    for (int i = 0; i < ndim; i++)
      _sizes[i] = sizes[i];

    // get total size
    totalSize = 1;
    for (int i = 0; i < ndim; i++)
      totalSize *= sizes[i];
  }

  // strides could be null
  if (strides != nullptr)
  {
    for (int i = 0; i < ndim; i++)
      _strides[i] = strides[i];
  }
  else // calculate stride
  {
    _strides[0] = 1;
    for (int i = 1; i < ndim; i++)
      _strides[i] = _sizes[i - 1] * _strides[i - 1];
  }
}

inline void shape::copy(const shape &other)
{
  init(other._offset, other._ids, other._sizes, other._strides, other._ndim);
}

inline void shape::move(shape &&other)
{
  _offset = other._offset;
  _ids = other._ids;
  _sizes = other._sizes;
  _strides = other._strides;
  _ndim = other._ndim;
  totalSize = other.totalSize;
  minMissingId = other.minMissingId;

  other._ids = nullptr;
  other._sizes = nullptr;
  other._strides = nullptr;
  other._ndim = 0;
  other._offset = 0;
  other.totalSize = 0;
  other.minMissingId = -1;
}

shape::shape()
{
  _offset = 0;
  _ids = nullptr;
  _sizes = nullptr;
  _strides = nullptr;
  _ndim = 0;
  totalSize = 0;
  minMissingId = -1;
}

shape::shape(const index_t *ids, const index_t *sizes, const index_t *strides, dim_t ndim)
{
  init(0, ids, sizes, strides, ndim);
}

shape::shape(index_t i0)
{
  index_t sizes[1] = {i0};
  init(0, nullptr, sizes, nullptr, 1);
}

shape::shape(index_t i0, index_t i1)
{
  index_t sizes[2] = {i0, i1};
  init(0, nullptr, sizes, nullptr, 2);
}

shape::shape(index_t i0, index_t i1, index_t i2)
{
  index_t sizes[3] = {i0, i1, i2};
  init(0, nullptr, sizes, nullptr, 3);
}

shape::shape(index_t i0, index_t i1, index_t i2, index_t i3)
    : shape(nullptr, nullptr, nullptr, 4)
{
  index_t sizes[4] = {i0, i1, i2, i3};
  init(0, nullptr, sizes, nullptr, 4);
}

shape::shape(const shape &other)
    : shape(other._ids, other._sizes, other._strides, other._ndim) {}

shape::shape(shape &&other)
{
  move(std::move(other));
}

shape::~shape()
{
  std::free(_ids);
  std::free(_sizes);
  std::free(_strides);
}

shape &shape::operator=(const shape &other)
{
  copy(other);
  return *this;
}

shape &shape::operator=(shape &&other)
{
  move(std::move(other));
  return *this;
}

index_t shape::offset() const
{
  return _offset;
}

index_t shape::offset(index_t *index) const
{
  index_t padding = _offset;
  for (int i = 0; i < _ndim; i++)
    padding += index[i] * _strides[i];
  return padding;
}

index_t shape::offset(std::vector<index_t> &index) const
{
  runtime_assert(index.size() == _ndim, "dimension mismatch");
  index_t padding = _offset;
  for (int i = 0; i < _ndim; i++)
    padding += index[i] * _strides[i];
  return padding;
}

index_t shape::offset(index_t i0) const
{
  runtime_assert(_ndim == 1, "dimension mismatch");
  return _offset + i0 * _strides[0];
}

index_t shape::offset(index_t i0, index_t i1) const
{
  runtime_assert(_ndim == 2, "dimension mismatch");
  return _offset + i0 * _strides[0] + i1 * _strides[1];
}

index_t shape::offset(index_t i0, index_t i1, index_t i2) const
{
  runtime_assert(_ndim == 3, "dimension mismatch");
  return _offset + i0 * _strides[0] + i1 * _strides[1] + i2 * _strides[2];
}

index_t shape::offset(index_t i0, index_t i1, index_t i2, index_t i3) const
{
  runtime_assert(_ndim == 4, "dimension mismatch");
  return _offset + i0 * _strides[0] + i1 * _strides[1] + i2 * _strides[2] + i3 * _strides[3];
}

// accessors

const dim_t &shape::size() const
{
  return totalSize;
}

const dim_t &shape::ndim() const
{
  return _ndim;
}

const index_t &shape::id(dim_t index) const
{
  return _ids[index];
}

const index_t &shape::size(dim_t index) const
{
  return _sizes[index];
}

const index_t &shape::stride(dim_t index) const
{
  return _strides[index];
}

bool shape::iscontiguous() const
{
  if (minMissingId < 0) // no id is missing
    return true;
  return false;
}

const index_t &shape::operator[](dim_t index) const
{
  return _sizes[index];
}

index_t &shape::id(dim_t index)
{
  return _ids[index];
}

index_t &shape::size(dim_t index)
{
  return _sizes[index];
}

index_t &shape::stride(dim_t index)
{
  return _strides[index];
}

// transpose methods

void shape::reOrder(index_t *src, index_t *temp, const index_t *index)
{
  memcpy(temp, src, _ndim * sizeof(index_t));
#pragma simd
  for (int i = 0; i < _ndim; i++)
    src[i] = temp[index[i]];
}

shape &shape::transpose(const index_t *index)
{
  index_t temp[_ndim];
  reOrder(_ids, temp, index);
  reOrder(_sizes, temp, index);
  reOrder(_strides, temp, index);
  return *this;
}

shape &shape::transpose(index_t i0, index_t i1)
{
  index_t index[_ndim];
  index[0] = i0;
  index[1] = i1;
  transpose(index);
  return *this;
}

shape &shape::transpose(index_t i0, index_t i1, index_t i2)
{
  index_t index[_ndim];
  index[0] = i0;
  index[1] = i1;
  index[2] = i2;
  transpose(index);
  return *this;
}

shape &shape::transpose(index_t i0, index_t i1, index_t i2, index_t i3)
{
  index_t index[_ndim];
  index[0] = i0;
  index[1] = i1;
  index[2] = i2;
  index[3] = i3;
  transpose(index);
  return *this;
}

shape &shape::transpose(const std::vector<index_t> &index)
{
  runtime_assert(index.size() == _ndim, "dimension mismatch");
  transpose(index.data());
  return *this;
}

shape &shape::narrow(dim_t dim, index_t firstIndex, index_t size)
{
  runtime_assert((dim >= 0) && (dim < _ndim), "out of range");
  runtime_assert((firstIndex >= 0) && (firstIndex < _sizes[dim]), "out of range");
  runtime_assert((size > 0) && (firstIndex <= _sizes[dim] - size), "out of range");

  if (firstIndex > 0)
    _offset += firstIndex * _strides[dim];

  _sizes[dim] = size;
  return *this;
}

shape &shape::select(dim_t dim, index_t sliceIndex)
{
  runtime_assert(_ndim > 1, "cannot select on a vector");
  runtime_assert((dim >= 0) && (dim < _ndim), "out of range");
  runtime_assert((sliceIndex >= 0) && (sliceIndex < _sizes[dim]), "out of range");

  narrow(dim, sliceIndex, 1);
  minMissingId = _ids[dim];
  for (dim_t d = dim; d < _ndim - 1; d++)
  {
    _ids[d] = _ids[d + 1];
    _sizes[d] = _sizes[d + 1];
    _strides[d] = _strides[d + 1];
  }
  _ndim--;
  return *this;
}

// compare methods

bool operator==(const shape &lhs, const shape &rhs)
{
  if (lhs.size() != rhs.size())
    return false;

  if (lhs.ndim() != rhs.ndim())
    return false;

  for (int i = 0; i < rhs.ndim(); i++)
  {
    if (lhs[i] != rhs[i])
      return false;
  }
  return true;
}

bool operator!=(const shape &lhs, const shape &rhs)
{
  return !(lhs == rhs);
}

// output stream

// for analysis
std::ostream &operator<<(std::ostream &os, shape &s)
{
  for (int i = 0; i < s.ndim(); i++)
  {
    os << s[i];
    if (i != s.ndim() - 1)
      os << ", ";
  }
  return os;
}

// repr
std::ostream &repr(std::ostream &os, shape &s)
{
  os << "shape(";
  for (int i = 0; i < s.ndim(); i++)
  {
    os << s[i];
    if (i != s.ndim() - 1)
      os << ", ";
  }
  os << ")";
  return os;
}

// operations

// transpose
shape transpose(const shape &s, index_t i0, index_t i1)
{
  shape output(s);
  output.transpose(i0, i1);
  return output;
}

shape transpose(const shape &s, index_t i0, index_t i1, index_t i2)
{
  shape output(s);
  output.transpose(i0, i1, i2);
  return output;
}

shape transpose(const shape &s, index_t i0, index_t i1, index_t i2, index_t i3)
{
  shape output(s);
  output.transpose(i0, i1, i2, i3);
  return output;
}

shape transpose(const shape &s, const index_t *index)
{
  shape output(s);
  output.transpose(index);
  return output;
}

shape transpose(const shape &s, const std::vector<index_t> &index)
{
  shape output(s);
  output.transpose(index);
  return output;
}

shape narrow(const shape &s, dim_t dim, index_t firstIndex, index_t size)
{
  shape output(s);
  output.narrow(dim, firstIndex, size);
  return output;
}

} // namespace bs
