#ifndef QMTK_TENSOR_INC
#define QMTK_TENSOR_INC

#include "general.h"
#include "shape.h"

namespace qmtk {

template <typename dtype>
class tensor
{
public:
  dtype *_data;
  shape _shape;

  tensor();
  tensor(const dtype *data, const shape &s);
  tensor(const tensor<dtype> &other);
  tensor(tensor<dtype> &&other);
  ~tensor();

  tensor<dtype>& operator+=(const tensor<dtype> &other);
  tensor<dtype>& operator+=(const dtype scalar);
  tensor<dtype>& =(const tensor<dtype> &other);
  tensor<dtype>& operator-=(const dtype scalar);

  tensor<dtype>& operator*=(const tensor<dtype> &other);
  tensor<dtype>& operator*=(const dtype scalar);
  tensor<dtype>& operator/=(const tensor<dtype> &other);
  tensor<dtype>& operator/=(const dtype scalar);

  /**
   * @brief matrix multiplication is a special case for tensor contraction.
   */
  tensor<dtype>& mul(tensor<dtype> &other);

  /**
   * @brief general multiplication is a contraction of two legs.
   */
  tensor<dtype>& mul(tensor<dtype> &other, index_t leg0, index_t leg1);

  tensor<dtype>& fmap();
};


template <typename dtype>
bool operator==(const tensor<dtype> &lhs, const tensor<dtype> &rhs);
template <typename dtype>
bool operator!=(const tensor<dtype> &lhs, const tensor<dtype> &rhs);

template <typename dtype>
bool operator==(const tensor<dtype> &lhs, const dtype &rhs);
template <typename dtype>
bool operator!=(const tensor<dtype> &lhs, const dtype &rhs);
template <typename dtype>
bool operator==(const dtype &lhs, const tensor<dtype> &rhs);
template <typename dtype>
bool operator!=(const dtype &lhs, const tensor<dtype> &rhs);

#include "tensor_impl.h"

}
#endif