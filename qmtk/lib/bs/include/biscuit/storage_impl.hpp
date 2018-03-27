#include "storage.hpp"

namespace bs
{

template <typename dtype>
inline void storage<dtype>::init(const dtype *data, index_t size)
{
  _size = size;
  dtype *array = new dtype[size];
  _data.reset(array, std::default_delete<dtype[]>());

  if (data != nullptr)
  {
    for (int i = 0; i < size; i++)
    {
      array[i] = data[i];
    }
  }
}

template <typename dtype>
inline void storage<dtype>::move(storage<dtype> &&other)
{
  _data = std::move(other._data);
  _size = other._size;

  other._size = 0;
}

template <typename dtype>
storage<dtype>::storage() : _data(), _size(0){};

template <typename dtype>
storage<dtype>::storage(index_t size)
{
  init(nullptr, size);
}

template <typename dtype>
storage<dtype>::storage(const dtype *data, index_t size)
{
  init(data, size);
}

template <typename dtype>
storage<dtype>::storage(const storage<dtype> &other)
{
  _data = other._data;
  _size = other._size;
};

template <typename dtype>
storage<dtype>::storage(storage<dtype> &&other)
{
  move(std::move(other));
}

template <typename dtype>
storage<dtype> &storage<dtype>::operator=(const storage<dtype> &other)
{
  _data = other._data;
  _size = other._size;
  return *this;
}

template <typename dtype>
storage<dtype> &storage<dtype>::operator=(storage<dtype> &&other)
{
  move(std::move(other));
  return *this;
}

template <typename dtype>
dtype &storage<dtype>::operator[](index_t index)
{
  return *(_data.get() + index);
}

template <typename dtype>
const dtype &storage<dtype>::operator[](index_t index) const
{
  return *(_data.get() + index);
}

template <typename dtype>
const index_t storage<dtype>::size() const
{
  return _size;
}

template <typename dtype>
const dtype *storage<dtype>::data() const
{
  return _data.get();
}

template <typename dtype>
storage<dtype> &storage<dtype>::resize(index_t size)
{
  runtime_assert(size >= 0, "invalid value");

  dtype *newData;
  dtype *oldData = _data.get();
  index_t length = BSMIN(_size, size);

  if (size == 0)
    newData = nullptr;
  else
    newData = new dtype[size];

  for(int i = 0; i <= length; i++)
  {
    newData[i] = oldData[i];
  }

  _data.reset(newData);
  _size = size;
  return *this;
}

template <typename dtype>
std::ostream &operator<<(std::ostream &os, const bs::storage<dtype> &s)
{
  os << type::trait<dtype>::name;
  os << " storage (" << s.size();
  os << ")" << std::endl;
  return os;
}

} // namespace bs
