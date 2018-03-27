#include "tensor.hpp"

namespace bs
{

template <typename dtype>
template <typename saver, typename ta>
inline tensor<dtype> &tensor<dtype>::fmap(const ta &scalar)
{
  iter::index index = make_index(this->_shape);
  index_t size = this->_shape.size();

#pragma omp parallel if (size > BS_OMP_OVERHEAD_THRESHOLD)
  {
#pragma omp for
    for (auto i = index.begin(); i != index.end(); i++)
    {
      saver::template to<ta>(this->_storage[*i], scalar);
    }
  }
  return *this;
}

template <typename dtype>
template <typename saver, typename ta>
inline tensor<dtype> &tensor<dtype>::fmap(const tensor<ta> &src)
{
  runtime_assert(this->_shape == src._shape, "shape mismatch");
  iter::index index = make_index(this->_shape);
  index_t size = this->_shape.size();

#pragma omp parallel if (size > BS_OMP_OVERHEAD_THRESHOLD)
  {
#pragma omp for
    for (auto i = index.begin(); i != index.end(); i++)
    {
      saver::template to<ta>(this->_storage[*i], src[i]);
    }
  }

  return *this;
}

template <typename dtype>
template <typename binary, typename ta>
tensor<dtype> &tensor<dtype>::fmap(const tensor<ta> &a, const tensor<ta> &b)
{
  runtime_assert(a._shape == b._shape, "shape mismatch");
  runtime_assert(this->_shape == a._shape, "shape mismatch");
  iter::index index = make_index(this->_shape);
  index_t size = this->_shape.size();

#pragma omp parallel if (size > BS_OMP_OVERHEAD_THRESHOLD)
  {
#pragma omp for
    for (auto i = index.begin(); i != index.end(); i++)
    {
      this->_storage[*i] = binary::template map<ta>(a[i], b[i]);
    }
  }
}

template <typename dtype>
template <typename binary, typename ta>
tensor<dtype> &tensor<dtype>::fmap(const tensor<ta> &a, const ta &b)
{
  runtime_assert(this->_shape == a._shape, "shape mismatch");
  iter::index index = make_index(this->_shape);
  index_t size = this->_shape.size();

#pragma omp parallel if (size > BS_OMP_OVERHEAD_THRESHOLD)
  {
#pragma omp for
    for (auto i = index.begin(); i != index.end(); i++)
    {
      this->_storage[*i] = binary::template map<ta>(a[i], b);
    }
  }
}

template <typename dtype>
template <typename binary, typename ta>
tensor<dtype> &tensor<dtype>::fmap(const ta &a, const tensor<ta> &b)
{
  runtime_assert(this->_shape == b._shape, "shape mismatch");
  iter::index index = make_index(this->_shape);
  index_t size = this->_shape.size();

#pragma omp parallel if (size > BS_OMP_OVERHEAD_THRESHOLD)
{
  #pragma omp for
  for (auto i = index.begin(); i != index.end(); i++)
  {
    this->_storage[*i] = binary::template map<ta>(a, b[i]);
  }
}
}

template <typename mapper, typename dtype, typename ta>
inline tensor<dtype> &fmap(tensor<dtype> &dst, const tensor<ta> &src)
{
  runtime_assert(dst._shape == src._shape, "shape mismatch");
  iter::index index = make_index(dst._shape);
  index_t size = dst._shape.size();

#pragma omp parallel if (size > BS_OMP_OVERHEAD_THRESHOLD)
  {
#pragma omp for
    for (auto i = index.begin(); i != index.end(); i++)
    {
      dst[i] = (dtype) mapper::template map<ta>(src[i]);
    }
  }

  return dst;
}

template <typename binary, typename ta, typename tb>
inline void fmap(tensor<ta> &dst, const tensor<tb> &a, const tensor<tb> &b)
{
  dst.template fmap<binary, tb>(a, b);
}

template <typename binary, typename ta, typename tb>
inline void fmap(tensor<ta> &dst, const tensor<tb> &a, const tb &b)
{
  dst.template fmap<binary, tb>(a, b);
}

template <typename binary, typename ta, typename tb>
inline void fmap(tensor<ta> &dst, const tb &a, const tensor<tb> &b)
{
  dst.template fmap<binary, tb>(a, b);
}

template <typename dtype>
tensor<dtype> &tensor<dtype>::operator+=(const tensor<dtype> &other)
{
  return fmap<op::sv::add, dtype>(other);
}

template <typename dtype>
tensor<dtype> &tensor<dtype>::operator+=(const dtype scalar)
{
  return fmap<op::sv::add, dtype>(scalar);
}

template <typename dtype>
tensor<dtype> &tensor<dtype>::operator-=(const tensor<dtype> &other)
{
  return fmap<op::sv::minus, dtype>(other);
}

template <typename dtype>
tensor<dtype> &tensor<dtype>::operator-=(const dtype scalar)
{
  return fmap<op::sv::minus, dtype>(scalar);
}

template <typename dtype>
tensor<dtype> &tensor<dtype>::operator*=(const tensor<dtype> &other)
{
  return fmap<op::sv::mul, dtype>(other);
}

template <typename dtype>
tensor<dtype> &tensor<dtype>::operator*=(const dtype scalar)
{
  return fmap<op::sv::mul, dtype>(scalar);
}

template <typename dtype>
tensor<dtype> &tensor<dtype>::operator/=(const tensor<dtype> &other)
{
  return fmap<op::sv::div, dtype>(other);
}

template <typename dtype>
tensor<dtype> &tensor<dtype>::operator/=(const dtype scalar)
{
  return fmap<op::sv::minus, dtype>(scalar);
}

// compare methods

template <typename dtype>
tensor<bool> tensor<dtype>::eq(const tensor<dtype> &other) const
{
  tensor<bool> compare(this->_shape);
  return fmap<op::bi::eq, dtype>(compare, *this, other);
}

template <typename dtype>
tensor<bool> tensor<dtype>::neq(const tensor<dtype> &other) const
{
  tensor<bool> compare(this->_shape);
  return fmap<op::bi::neq, dtype>(compare, *this, other);
}

template <typename dtype>
tensor<bool> tensor<dtype>::eq(const dtype &other) const
{
  tensor<bool> compare(this->_shape);
  return fmap<op::bi::eq, dtype>(compare, *this, other);
}

template <typename dtype>
tensor<bool> tensor<dtype>::neq(const dtype &other) const
{
  tensor<bool> compare(this->_shape);
  return fmap<op::bi::neq, dtype>(compare, *this, other);
}

template <typename dtype>
tensor<dtype> &tensor<dtype>::fill(const dtype &scalar)
{
  return fmap<op::sv::assign, dtype>(scalar);
}

template <typename dtype>
tensor<dtype> &tensor<dtype>::zeros()
{
  return fmap<op::sv::assign, dtype>(0);
}

template <typename dtype>
tensor<dtype> &tensor<dtype>::ones()
{
  return fmap<op::sv::assign, dtype>(1);
}

template <typename dtype>
tensor<dtype> &tensor<dtype>::operator=(const dtype &scalar)
{
  return fmap<op::sv::assign, dtype>(scalar);
}

// partial specilized

// bool tensor
template <typename dtype>
tensor<bool> &tensor<dtype>::eq(const tensor<dtype> &a, const tensor<dtype> &b)
{
  return fmap<op::bi::eq, dtype>(a, b);
}

template <typename dtype>
tensor<bool> &tensor<dtype>::neq(const tensor<dtype> &a, const tensor<dtype> &b)
{
  return fmap<op::bi::neq, dtype>(a, b);
}

template <typename dtype>
tensor<bool> &tensor<dtype>::eq(const tensor<dtype> &a, const dtype &b)
{
  return fmap<op::bi::eq, dtype>(a, b);
}

template <typename dtype>
tensor<bool> &tensor<dtype>::neq(const tensor<dtype> &a, const dtype &b)
{
  return fmap<op::bi::neq, dtype>(a, b);
}

template <typename dtype>
tensor<bool> &tensor<dtype>::eq(const dtype &a, const tensor<dtype> &b)
{
  return fmap<op::bi::eq, dtype>(a, b);
}

template <typename dtype>
tensor<bool> &tensor<dtype>::neq(const dtype &a, const tensor<dtype> &b)
{
  return fmap<op::bi::neq, dtype>(a, b);
}

} // namespace bs
