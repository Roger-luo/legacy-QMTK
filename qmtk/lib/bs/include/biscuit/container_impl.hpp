#include "container.hpp"
// TODO: make storage like a shared_ptr, or use a shared_ptr instead?
namespace bs
{
template <typename dtype>
container<dtype>::container() : _storage(), _shape(){};

template <typename dtype>
container<dtype>::container(const shape &s) : container(nullptr, s) {};

template <typename dtype>
container<dtype>::container(const dtype *data, const shape &s)
    : _storage(data, s.size()), _shape(s) {}

template <typename dtype>
container<dtype>::container(const container<dtype> &other)
    : _storage(other._storage), _shape(other._shape) {}

template <typename dtype>
container<dtype>::container(container<dtype> &&other)
{
  _storage = std::move(other._storage);
  _shape = std::move(other._shape);
}

template <typename dtype>
container<dtype> &container<dtype>::operator=(const container<dtype> &other)
{
  _storage = other._storage;
  _shape = other._shape;
  return *this;
}

template <typename dtype>
container<dtype> &container<dtype>::operator=(container<dtype> &&other)
{
  _storage = std::move(other._storage);
  _shape = std::move(other._shape);
  return *this;
}

// access methods

template <typename dtype>
dtype &container<dtype>::operator()(index_t *index) {
  return _storage[_shape.offset(index)];
}

template <typename dtype>
dtype &container<dtype>::operator()(std::vector<index_t> &index) {
  return _storage[_shape.offset(index)];
}

template <typename dtype>
dtype &container<dtype>::operator()(index_t i0) {
  return _storage[_shape.offset(i0)];
}

template <typename dtype>
dtype &container<dtype>::operator()(index_t i0, index_t i1) {
  return _storage[_shape.offset(i0, i1)];
}

template <typename dtype>
dtype &container<dtype>::operator()(index_t i0, index_t i1, index_t i2) {
  return _storage[_shape.offset(i0, i1, i2)];
}

template <typename dtype>
dtype &container<dtype>::operator()(index_t i0, index_t i1, index_t i2, index_t i3) {
  return _storage[_shape.offset(i0, i1, i2, i3)];
}

template <typename dtype>
const dtype &container<dtype>::operator()(index_t *index) const
{
  return _storage[_shape.offset(index)];
}

template <typename dtype>
const dtype &container<dtype>::operator()(std::vector<index_t> &index) const
{
  return _storage[_shape.offset(index)];
}

template <typename dtype>
const dtype &container<dtype>::operator()(index_t i0) const
{
  return _storage[_shape.offset(i0)];
}

template <typename dtype>
const dtype &container<dtype>::operator()(index_t i0, index_t i1) const
{
  return _storage[_shape.offset(i0, i1)];
}

template <typename dtype>
const dtype &container<dtype>::operator()(index_t i0, index_t i1, index_t i2) const
{
  return _storage[_shape.offset(i0, i1, i2)];
}

template <typename dtype>
const dtype &container<dtype>::operator()(index_t i0, index_t i1, index_t i2, index_t i3) const
{
  return _storage[_shape.offset(i0, i1, i2, i3)];
}

template <typename dtype>
dtype &container<dtype>::operator[](iterator &index)
{
  return _storage[*index];
}

template <typename dtype>
const dtype &container<dtype>::operator[](iterator &index) const
{
  return _storage[*index];
}

template <typename dtype>
container<dtype> &container<dtype>::reshape(const shape &s)
{
  if(s.size() > _shape.size())
  {
    _storage.resize(s.size());
  }

  _shape = s;
  return *this;
}

template <typename dtype>
inline container<dtype> &container<dtype>::transpose(index_t i0, index_t i1)
{
  return _shape.transpose(i0, i1);
}

template <typename dtype>
inline container<dtype> &container<dtype>::transpose(index_t i0, index_t i1, index_t i2)
{
  return _shape.transpose(i0, i1, i2);
}

template <typename dtype>
inline container<dtype> &container<dtype>::transpose(index_t i0, index_t i1, index_t i2, index_t i3)
{
  return _shape.transpose(i0, i1, i2, i3);
}

template <typename dtype>
inline container<dtype> &container<dtype>::transpose(const index_t *index)
{
  return _shape.transpose(index);
}

template <typename dtype>
inline container<dtype> &container<dtype>::transpose(const std::vector<index_t> &index)
{
  return _shape.transpose(index);
}

} // namespace bs
