#ifndef BS_CONTAINER_INC
#define BS_CONTAINER_INC

#include "general.hpp"
#include "storage.hpp"
#include "shape.hpp"
#include "shape_iter.hpp"

namespace bs {

template <typename dtype>
class container
{
public:
  using iterator = iter::iterator_t<iter::index>;

  storage<dtype> _storage;
  shape _shape;

  container();
  container(const shape &s);
  container(const dtype *data, const shape &s);
  container(const container<dtype> &other);
  container(container<dtype> &&other);

  container<dtype> &operator=(const container<dtype> &other);
  container<dtype> &operator=(container<dtype> &&other);

  // access methods
  dtype &operator()(index_t *index);
  dtype &operator()(std::vector<index_t> &index);
  dtype &operator()(index_t i0);
  dtype &operator()(index_t i0, index_t i1);
  dtype &operator()(index_t i0, index_t i1, index_t i2);
  dtype &operator()(index_t i0, index_t i1, index_t i2, index_t i3);

  const dtype &operator()(index_t *index) const;
  const dtype &operator()(std::vector<index_t> &index) const;
  const dtype &operator()(index_t i0) const;
  const dtype &operator()(index_t i0, index_t i1) const;
  const dtype &operator()(index_t i0, index_t i1, index_t i2) const;
  const dtype &operator()(index_t i0, index_t i1, index_t i2, index_t i3) const;

  dtype &operator[](iterator &index);
  const dtype &operator[](iterator &index) const;

  container<dtype> &reshape(const shape &s);

  container<dtype> &transpose(index_t i0, index_t i1);
  container<dtype> &transpose(index_t i0, index_t i1, index_t i2);
  container<dtype> &transpose(index_t i0, index_t i1, index_t i2, index_t i3);
  container<dtype> &transpose(const index_t *index);
  container<dtype> &transpose(const std::vector<index_t> &index);
};

} // namespace bs

#include "container_impl.hpp"

#endif