#ifndef BS_SHAPE_INC
#define BS_SHAPE_INC

#include "general.hpp"

namespace bs
{

static const int kShapeBuffer = 5;

class shape
{
private:
  dim_t totalSize;
  /**
   * @brief minimum missing id. each slice operation
   * will cause in-contiguous array memory. we will record
   * minimum missing id in slice operation to avoid loop
   * through in-contiguous array memory. all the id smaller
   * than minimum missing id together is a contiguous
   * memory block. Should loop through this block first.
   */
  index_t minMissingId;

  /**
   * @brief reOrder by numbers in *index
   * with an assisted array *temp
   */
  void reOrder(index_t *src, index_t *temp, const index_t *index);

public:
  index_t *_ids;
  index_t *_sizes;
  index_t *_strides;
  dim_t _ndim;
  index_t _offset;

  // TODO: use buffer for small size?
  // index_t _small_ids[kShapeBuffer];
  // index_t _small_sizes[kShapeBuffer];
  // index_t _small_strides[kShapeBuffer];

  void init(index_t padding, const index_t *ids, const index_t *sizes, const index_t *strides, dim_t ndim);
  void copy(const shape &other);
  void move(shape &&other);

  shape();
  shape(const index_t *ids, const index_t *sizes, const index_t *strides, dim_t ndim);
  shape(index_t i0);
  shape(index_t i0, index_t i1);
  shape(index_t i0, index_t i1, index_t i2);
  shape(index_t i0, index_t i1, index_t i2, index_t i3);

  shape(const shape &other);
  shape(shape &&other);
  ~shape();

  shape &operator=(const shape &other);
  shape &operator=(shape &&other);

  index_t offset() const;
  index_t offset(index_t *index) const;
  index_t offset(std::vector<index_t> &index) const;
  index_t offset(index_t i0) const;
  index_t offset(index_t i0, index_t i1) const;
  index_t offset(index_t i0, index_t i1, index_t i2) const;
  index_t offset(index_t i0, index_t i1, index_t i2, index_t i3) const;


  // access methods
  const dim_t &size() const;
  const dim_t &ndim() const;
  const index_t &id(dim_t index) const;
  const index_t &size(dim_t index) const;
  const index_t &stride(dim_t index) const;
  const index_t &operator[](dim_t index) const;
  inline const index_t missing() const {return minMissingId;};

  // setters
  index_t &id(dim_t index);
  index_t &size(dim_t index);
  index_t &stride(dim_t index);

  // memory check
  bool iscontiguous() const;

  /**
   * @brief transpose methods. for raw pointer, its
   * size should be kept to the number of dimensions
   * of current shape instance. there is no checking
   * for this bound.
   * 
   * for direct transpose methods (takes integers), it
   * should be the current i-th leg id number;
   */
  shape &transpose(index_t i0, index_t i1);
  shape &transpose(index_t i0, index_t i1, index_t i2);
  shape &transpose(index_t i0, index_t i1, index_t i2, index_t i3);
  shape &transpose(const index_t *index);
  shape &transpose(const std::vector<index_t> &index);

  shape &narrow(dim_t dim, index_t firstIndex, index_t size);
  shape &select(dim_t dim, index_t sliceIndex);

  // output stream
  // for analysis
  friend std::ostream &operator<<(std::ostream &os, shape &s);

  friend std::ostream &repr(std::ostream &os, shape &s);
};

// compare methods
bool operator==(const shape &lhs, const shape &rhs);
bool operator!=(const shape &lhs, const shape &rhs);

// transpose
shape transpose(const shape &s, index_t i0, index_t i1);
shape transpose(const shape &s, index_t i0, index_t i1, index_t i2);
shape transpose(const shape &s, index_t i0, index_t i1, index_t i2, index_t i3);
shape transpose(const shape &s, const index_t *index);
shape transpose(const shape &s, const std::vector<index_t> &index);

shape narrow(const shape &s, dim_t dim, index_t firstIndex, index_t size);
shape select(const shape &s, dim_t dim, index_t sliceIndex);

}

#include "shape_impl.hpp"

#endif // BS_SHAPE_INC