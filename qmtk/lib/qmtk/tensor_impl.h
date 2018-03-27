#include "tensor.h"

template<typename dtype>
tensor<dtype>::tensor() : _data(nullptr), _shape() {};

template <typename dtype>
tensor<dtype>::tensor(const dtype *data, const shape &s)
  : _shape(s)
{
  _data = (dtype *)std::calloc(s.size(), sizeof(dtype));
  if(_data==nullptr)
    throw std::bad_alloc();

  if(data!=nullptr)
  {
    #pragma simd
    for(int i=0;i<s.size();i++)
      _data[i] = data[i];
  }
}

template <typename dtype>
tensor<dtype>::tensor(const tensor<dtype> &other)
  :tensor(other._data, other._shape){}

template <typename dtype>
tensor<dtype>::tensor(tensor<dtype> &&other) {
  tensor._data = other._data;
  tensor._shape = shape(std::move(other._shape));

  other._data = nullptr;
}

template <typename dtype>
tensor<dtype>::~tensor() {
  std::free(_data);
}
