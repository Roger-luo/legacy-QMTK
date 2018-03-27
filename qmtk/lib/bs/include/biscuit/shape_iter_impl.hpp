#include "shape_iter.hpp"

namespace bs
{

namespace iter
{

index::index(const shape &s)
    : _shape(s){};

const iterator_t<index> index::begin() const
{
  return iterator_t<index>(_shape);
}

const iterator_t<index> index::end() const
{
  iterator_t<index> end_itr(_shape);
  for (int i = 0; i < _shape.ndim(); i++)
  {
    end_itr._data[i] = _shape.size(i) - 1;
  }
  end_itr._count = _shape.size();
  return end_itr;
}

// we assume input s is incontiguous
const shape inner(const shape &s)
{
  dim_t ndim = s.ndim();
  index_t sizes[ndim];
  index_t strides[ndim];
  index_t inner_contiguous_size = 1;
  int k = 1;
  for (int i = 0; i < s.ndim(); i++)
  {
    if (s.id(i) < s.missing())
    {
      inner_contiguous_size *= s.size(i);
      ndim--;
    }
    else
    {
      sizes[k] = s.size(i);
      strides[k] = s.stride(i);
      k++;
    }
  }
  sizes[0] = inner_contiguous_size;
  strides[0] = 1;

  return shape(nullptr, sizes, strides, ndim + 1);
}

iterator_t<index>::iterator_t(const shape &s) : _shape(s), _count(0)
{
  _data = (index_t *)std::calloc(_shape._ndim, sizeof(index_t));
  if (_data == nullptr)
    throw std::bad_alloc();
};

iterator_t<index>::iterator_t(const iterator_t &itr) : iterator_t(itr._shape)
{
  for (int i = 0; i < _shape.ndim(); i++)
    _data[i] = itr._data[i];
}

iterator_t<index>::iterator_t(iterator_t &&itr) : _shape(itr._shape)
{
  _data = itr._data;
  _count = itr._count;
  itr._data = nullptr;
}

iterator_t<index>::~iterator_t()
{
  std::free(_data);
}

iterator_t<index> &iterator_t<index>::operator=(const iterator_t<end> &ends)
{
  for (int i = 0; i < _shape.ndim(); i++)
    _data[i] = _shape.size(i) - 1;
  return *this;
}

index_t iterator_t<index>::operator*()
{
  index_t output = 0;
  for (int i = 0; i < _shape.ndim(); i++)
    output += _shape.offset() + _data[i] * _shape.stride(i);
  return output;
}

iterator_t<index> &iterator_t<index>::operator+=(index_t offset)
{
  _count += offset;
  for (int i = 0; i < _shape.ndim(); i++)
  {
    if (_data[i] + offset < _shape.size(i))
    {
      _data[i] += offset;
      break;
    }
    else
    {
      offset -= (_shape.size(i) - _data[i] - 1);
      _data[i] = 0;
    }

    if (!offset)
      break;
  }
  return *this;
}

iterator_t<index> &iterator_t<index>::operator-=(index_t offset)
{
  _count -= offset;
  for (int i = 0; i < _shape.ndim(); i++)
  {
    if (_data[i] - offset >= 0)
    {
      _data[i] -= offset;
      break;
    }
    else
    {
      offset -= _data[i];
      _data[i] = _shape.size(i) - 1;
    }

    if (!offset)
      break;
  }
  return *this;
}

iterator_t<index> &iterator_t<index>::operator++()
{
  operator+=(1);
  return *this;
}

iterator_t<index> iterator_t<index>::operator++(int)
{
  operator+=(1);
  return *this;
}

iterator_t<index> &iterator_t<index>::operator--()
{
  operator-=(1);
  return *this;
}

iterator_t<index> iterator_t<index>::operator--(int)
{
  operator-=(1);
  return *this;
}

bool operator==(const iterator_t<index> &lhs, const iterator_t<index> &rhs)
{
  return lhs._count == rhs._count;
}

/**
 * @brief worst case is different, therefore we do not use
 * !(lhs == rhs) here.
 */
bool operator!=(const iterator_t<index> &lhs, const iterator_t<index> &rhs)
{
  return !(lhs == rhs);
}

bool operator==(const iterator_t<index> &lhs, const iterator_t<bs::end> &rhs)
{
  return lhs._count == lhs._shape.size();
}

/**
 * @brief this is usually used in loops with i != iter.end()
 * in most evaluations _data[i] is not the same with _shape.size
 * therefore we return false directly.
 */
bool operator!=(const iterator_t<index> &lhs, const iterator_t<bs::end> &rhs)
{
  return !(lhs == rhs);
}

bool operator==(const iterator_t<bs::end> &lhs, const iterator_t<index> &rhs)
{
  return rhs == lhs;
}

bool operator!=(const iterator_t<bs::end> &lhs, const iterator_t<index> &rhs)
{
  return rhs != lhs;
}

std::ostream &operator<<(std::ostream &os, iterator_t<index> &self)
{
  for (int i = 0; i < self._shape.ndim(); i++)
  {
    os << self._data[i];
    if (i != self._shape.ndim())
      os << ", ";
  }
  return os;
}

} // namespace iter

iter::index make_index(const shape &s)
{
  if (s.iscontiguous())
    return iter::index(shape(s.size()));
  else
    return iter::index(iter::inner(s));
}

} // namespace bs
