#ifndef BS_TENSOR_INC
#define BS_TENSOR_INC

#include "general.hpp"
#include "shape.hpp"
#include "container.hpp"
#include "operators.hpp"

namespace bs
{
template <typename dtype>
class tensor : public container<dtype>
{
public:
  tensor() : container<dtype>() {};
  tensor(const shape &s) : container<dtype>(s) {};
  tensor(const dtype *data, const shape &s) : container<dtype>(data, s) {};
  tensor(const tensor<dtype> &other) : container<dtype>(other) {};
  tensor(tensor<dtype> &&other) : container<dtype>(other) {};

  template <typename saver, typename ta>
  tensor<dtype> &fmap(const ta &scalar);

  template <typename saver, typename ta>
  tensor<dtype> &fmap(const tensor<ta> &src);

  template <typename binary, typename ta>
  tensor<dtype> &fmap(const tensor<ta> &a, const tensor<ta> &b);

  template <typename binary, typename ta>
  tensor<dtype> &fmap(const tensor<ta> &a, const ta &b);

  template <typename binary, typename ta>
  tensor<dtype> &fmap(const ta &a, const tensor<ta> &b);

  template <typename mapper, typename ta, typename tb>
  friend tensor<ta> &fmap(tensor<ta> &dst, const tensor<tb> &src);

  template <typename binary, typename ta, typename tb>
  friend void fmap(tensor<ta> &dst, const tensor<tb> &a, const tensor<tb> &b);

  template <typename binary, typename ta, typename tb>
  friend void fmap(tensor<ta> &dst, const tensor<tb> &a, const tb &scalar);

  template <typename binary, typename ta, typename tb>
  friend void fmap(tensor<ta> &dst, const tb &scalar, const tensor<tb> &b);

  tensor<dtype> &operator+=(const tensor<dtype> &other);
  tensor<dtype> &operator+=(const dtype scalar);
  tensor<dtype> &operator-=(const tensor<dtype> &other);
  tensor<dtype> &operator-=(const dtype scalar);

  tensor<dtype> &operator*=(const tensor<dtype> &other);
  tensor<dtype> &operator*=(const dtype scalar);
  tensor<dtype> &operator/=(const tensor<dtype> &other);
  tensor<dtype> &operator/=(const dtype scalar);

  // compare methods
  tensor<bool> eq(const tensor<dtype> &other) const;
  tensor<bool> neq(const tensor<dtype> &other) const;

  tensor<bool> eq(const dtype &other) const;
  tensor<bool> neq(const dtype &other) const;

  tensor<bool> &eq(const tensor<dtype> &a, const tensor<dtype> &b);
  tensor<bool> &neq(const tensor<dtype> &a, const tensor<dtype> &b);

  tensor<bool> &eq(const tensor<dtype> &a, const dtype &b);
  tensor<bool> &neq(const tensor<dtype> &a, const dtype &b);

  tensor<bool> &eq(const dtype &a, const tensor<dtype> &b);
  tensor<bool> &neq(const dtype &a, const tensor<dtype> &b);

  // mappers
  tensor<dtype> &fill(const dtype &scalar);
  tensor<dtype> &zeros();
  tensor<dtype> &ones();

  tensor<dtype> &operator=(const dtype &scalar);

  friend std::ostream &operator<<(std::ostream &os, tensor<dtype> &t)
  {
    os << "tensor{" << t._shape;
    os << ", " << type::trait<dtype>::name << "}";
    
    return os; 
  }
};

} // namespace bs

#include "tensor_impl.hpp"

#endif // BS_TENSOR_INC