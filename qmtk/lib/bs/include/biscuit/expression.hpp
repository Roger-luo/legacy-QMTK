#ifndef BS_EXPR_INC
#define BS_EXPR_INC

#include "operators.hpp"

namespace expr {

template <typename saver, typename rvalue, typename dtype>
struct engine;

template <typename subtype, typename dtype>
struct expr
{
  inline const subtype& self(void) const {
    return *static_cast<const subtype *>(this);
  }

  inline subtype* ptrself(void) {
    return static_cast<subtype*>(this);
  }
};

template <typename dtype>
struct scalar: public expr<scalar<dtype>, dtype>
{
  dtype _data;
  scalar(dtype data) : _data(data) {};
} 

template <typename dtype>
inline make_scalar<dtype> (dtype s) {
  return scalar<dtype>(s);
}

template <typename dst_t, typename src_t, typename etype>
struct typecast: public expr<typecast<dst_t, src_t, etype>, dst_t>
{
  const etype &_expr;
  explicit typecast(const etype &e) : _expr(e) {}
};

template <typename dst_t, typename src_t, typename etype>
inline typecast<dst_t, src_t, etype> make_cast(const expr<etype, src_t> &e) {
  return typecast<dst_t, src_t, etype>(e.self());
}

template <typename etype, typename dtype>
struct transpose: public expr<transpose<etype, dtype>, dtype>
{
  const etype &_expr;
  explicit transpose(const etype &e) : expr(e) {};
  inline const etype &t(void) const {
    return _expr;
  }
};

template <typename container_t, typename dtype>
class rvalue: public expr<container_t, dtype>
{
public:

  inline const transpose<container_t, dtype> t(void) const
  {
    return transpose<container_t, dtype>(this->self());
  }

  inline container_t &operator+=(dtype s) {
    engine<op::sv::add, container_t, dtype>::eval(this->ptrself(), scalar<dtype>(s));
    return *(this->ptrself());
  }

  inline container_t &operator-=(dtype s) {
    engine<op::sv::minus, container_t, dtype>::eval(this->ptrself(), scalar<dtype>(s));
  }

  inline container_t &operator*=(dtype s) {
    engine<op::sv::mul, container_t, dtype>::eval(this->ptrself(), scalar<dtype>(s));
    return *(this->ptrself());
  }

  inline container_t &operator/=(dtype s) {
    engine<op::sv::div, container_t, dtype>::eval(this->ptrself(), scalar<dtype>(s));
    return *(this->ptrself());
  }

  inline container_t &__assign(dtype s) {
    engine<op::sv::assign, container_t, dtype>::eval(this->ptrself(), scalar<dtype>(s));
    return *(this->ptrself());
  }

  template<typename expr_t>
  inline container_t &__assign(const expr<expr_t, dtype> &exp) {
    engine<op::sv::assign, container_t, dtype>::eval(this->ptrself(), exp.self());
    return *(this->ptrself());
  }
};

} // namespace expr

#endif // BS_EXPR_INC