#ifndef QMTK_SITE_INC
#define QMTK_SITE_INC

class site {
private:
  /* data */
public:

  site(int *data, ssize_t ndim) {
    _data = std::malloc(sizeof(int) * ndim);
    if(_data==nullptr)
      throw std::bad_alloc("cannot alloc this site")
    _ndim = ndim

    if(data!=nullptr)
    {
      #pragma unroll
      for(ssize_t i=0;i<ndim;i++)
        _data[i] = data[i];
    }
  }

  site(int i0);
  site(int i0, int i1);
  site(int i0, int i1, int i2);
  site(int i0, int i1, int i2, int i3);

  inline int &unsafe_get(ssize_t index);

  inline int &operator[](ssize_t index);

  int *_data;
  ssize_t _ndim;
};

#endif