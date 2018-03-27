#ifndef QMTK_SHAPE_INC
#define QMTK_SHAPE_INC

#include "general.h"

namespace qmtk {

static const int kShapeBuffer = 5;

class shape
{
private:
  dim_t total_size;

public:
  index_t *_sizes;
  index_t *_strides;
  dim_t _ndim;

  // TODO: use buffer for small size?
  // index_t _small_sizes[kShapeBuffer];
  // index_t _small_strides[kShapeBuffer];

  shape();
  shape(const index_t *sizes, const index_t *strides, dim_t ndim);
  shape(index_t i0);
  shape(index_t i0, index_t i1);
  shape(index_t i0, index_t i1, index_t i2);
  shape(index_t i0, index_t i1, index_t i2, index_t i3);

  shape(const shape &other);
  shape(shape &&other);
  ~shape();

  dim_t size() const;
  dim_t ndim() const;
  const index_t& operator[](dim_t index) const;
};

bool operator==(const shape &lhs, const shape &rhs);
bool operator!=(const shape &lhs, const shape &rhs);

}

#endif // QMTK_SHAPE_INC