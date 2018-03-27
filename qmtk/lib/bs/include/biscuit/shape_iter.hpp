#ifndef BS_SHAPE_ITER
#define BS_SHAPE_ITER

#include "shape.hpp"

namespace bs {

class end {};

namespace iter {

/**
 * @brief iterator type. iterator for classes in BS
 * should register in this template type
 */
template<typename dtype>
class iterator_t {};

/**
 * @brief index type. index borrows a shape, and offers
 * iteration methods to loop through a tensor with certain
 * shape. (usually we return an offset in memory address)
 */
class index;

/**
 * @brief iteration end
 */
template <>
class iterator_t<end> {
public:
  iterator_t(){};
};

template <>
class iterator_t<index>;

class index
{
public:
  using iterator = iterator_t<index>;
  shape _shape;

  index(const shape &s);

  const iterator_t<index> begin() const;
  const iterator_t<index> end() const;
};

const shape inner(const shape &s);

/**
 * @brief index iterator loop to next index, when
 * it add 1.
 */
template <>
class iterator_t<index>
{
private:
  const shape &_shape;
public:
  index_t _count;
  index_t *_data;
  iterator_t();
  iterator_t(const shape &s);
  iterator_t(const iterator_t &itr);
  iterator_t(iterator_t &&itr);
  ~iterator_t();

  iterator_t<index> &operator=(const iterator_t<end> &ends);

  inline const index_t curr_idx() const {return _count;};

  // get offset
  index_t operator*();

  iterator_t<index> &operator+=(index_t offset);
  iterator_t<index> &operator-=(index_t offset);

  iterator_t<index> &operator++();
  iterator_t<index> &operator--();

  iterator_t<index> operator++(int);
  iterator_t<index> operator--(int);

  friend bool operator==(const iterator_t<index> &lhs, const iterator_t<index> &rhs);
  friend bool operator!=(const iterator_t<index> &lhs, const iterator_t<index> &rhs);

  friend bool operator==(const iterator_t<index> &lhs, const iterator_t<end> &rhs);
  friend bool operator!=(const iterator_t<index> &lhs, const iterator_t<end> &rhs);
  friend bool operator==(const iterator_t<end> &lhs, const iterator_t<index> &rhs);
  friend bool operator!=(const iterator_t<end> &lhs, const iterator_t<index> &rhs);

  friend std::ostream &operator<<(std::ostream &os, iterator_t<index> &self);
};

} // namespace iter

iter::index make_index(const shape &s);

} // namespace bs

#include "shape_iter_impl.hpp"

#endif