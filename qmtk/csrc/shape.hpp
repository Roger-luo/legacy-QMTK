#ifndef QMTK_SHAPE_INC
#define QMTK_SHAPE_INC

#include "general.hpp"

class shape
{
  shape():_data(nullptr), _ndim(0) {};
  shape(ssize_t ndim) {
    _data = std::malloc(sizeof(ssize_t) * ndim);
    if(_data==nullptr)
      throw std::bad_alloc("alloc for class shape failed");
    _ndim = ndim;
  }

  template<typename... T>
  shape(T... args) :shape(sizeof...(args)) {
    _count = 0;
    init(args...);
  };

  shape(const ssize_t *data, ssize_t ndim)
    : shape(ndim) {
    for(int i=0;i<ndim;i++)
      _data[i] = data[i];
  }

  shape(const shape &other)
    :shape(other._data, other._ndim) {}

  ~shape() {std::free(_data);};

  template<typename... T>
  inline void init(int i0, T... args) {
    _data[_count] = i0;
    _count++;
    init(args...);
  }

  inline void init() {_count=0;}

  inline ssize_t &operator[](ssize_t index) {
    return _data[index];
  }

  inline ssize_t size() const {
    return _ndim;
  }

  inline ssize_t *data() {return _data;}

  ssize_t *_data;
  ssize_t _ndim;

private:
  ssize_t _count;
}

#endif