#ifndef QMTK_SPACE_INC
#define QMTK_SPACE_INC

#include "general.hpp"

template<typename T>
class Spin {
private:
  bool need_rand_init;
  int iter_count;

  std::random_device rd;
  std::default_random_engine engine;
  std::uniform_real_distribution<float> dice;

public:
  T *_data;
  std::vector<ssize_t> _shape;
  ssize_t _size;
  int _up;
  int _down;
  unsigned int _nflips;
  float _p;

  inline py::tuple get_shape() {
    py::tuple shape(_shape.size());
    for(unsigned i=0;i<_shape.size();i++)
      shape[i] = _shape[i];
    return shape;
  }

  inline void set_shape(const py::object &shape) {
    if(py::isinstance<py::tuple>(shape))
      set_shape(shape.cast<py::tuple>());
    else
    {
      try {
        set_shape(shape.cast<int>());
      } catch (py::cast_error &e) {
        throw py::cast_error("invalid argument,"
          "expect int or tuple of int");
      }
    }

  }

  inline void set_shape(const py::tuple &shape) {
    _shape.clear();
    for(auto i=shape.begin();i!=shape.end();i++)
    {
      ssize_t t;
      try {
         t = py::cast<ssize_t>(*i);
      } catch (py::cast_error &e) {
        throw py::cast_error("shape expect integers");
      }
      _shape.push_back(t);
    }
  }

  inline void set_shape(ssize_t shape) {
    _shape.clear();
    _shape.push_back(shape);
  }

  Spin(const py::tuple &shape)
    : Spin(shape, 0, 1, 1, 0.5) {};

  Spin(const py::tuple &shape,
      int down, int up,
      unsigned int nflips,
      float p )
      : iter_count(0), rd(), engine(rd()), dice(0, 1),
        _shape(py::cast<std::vector<ssize_t>>(shape)),
        _up(up), _down(down), _nflips(nflips),
        _p(p)
  {
    _size = 1;
    for(auto i=_shape.begin();i!=_shape.end();i++)
      _size *= *i;
    _data = (T*)std::calloc(_size, sizeof(T));
    reset();
  }

  ~Spin() {std::free(_data);};

  void rand() {
    need_rand_init = false;
    for(int i=0;i<this->_size;i++)
      _data[i] = choose();
  }

  T choose() {
    if(dice(engine) > _p) return _up;
    else return _down;
  }

  void reset() {
    need_rand_init = true;
    for(int i=0;i<this->_size;i++)
      _data[i] = _down;
  }

  void shift() {
    for(ssize_t i=0;i<this->_size;i++) {
      if(_data[i] == _up)
        _data[i] = _down;
      else {
        _data[i] = _up;
        break;
      }
    }
  }

  Spin &iter() {
    this->iter_count = 0;
    if(!need_rand_init)
      this->reset();
    return *this;
  }

  Spin &next() {
    if(this->iter_count < 1)
    {
      iter_count++;
    }
    else if(this->iter_count < (1<<this->_size))
    {
      iter_count++;
      this->shift();
    }
    else
      throw pybind11::stop_iteration();
    return *this;
  }

  inline ssize_t rand_offset() {
    std::uniform_int_distribution<ssize_t> offset(0, _size-1);
    return offset(engine);
  }

  inline void flip(ssize_t offset) {
    if(_data[offset]==_up) _data[offset] = _down;
    else _data[offset] = _up;
  }

  void randflip(long MAX_FLIPS) {
    if(this->need_rand_init)
      return this->rand();

    if(_nflips==1) flip(rand_offset());
    else {
      std::set<ssize_t> history;
      for(int i=0;i<MAX_FLIPS;i++)
      {
        ssize_t offset = rand_offset();
        if(history.find(offset)!=history.end())
        {
          history.insert(offset);
          flip(offset);
        }
        if(history.size() == _nflips)
          break;
      }
    }
  }
};

#endif