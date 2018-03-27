#ifndef BS_STORAGE_INC
#define BS_STORAGE_INC

#include "general.hpp"
#include "type_trait.hpp"

namespace bs
{

template <typename dtype>
class storage
{
private:
  void init(const dtype *data, index_t size);
  void move(storage<dtype> &&other);

public:
  std::shared_ptr<dtype> _data;
  index_t _size;

  storage();
  storage(index_t size);
  storage(const dtype *data, index_t size);
  storage(const storage<dtype> &other);
  storage(storage<dtype> &&other);

  storage<dtype> &operator=(const storage<dtype> &other);
  storage<dtype> &operator=(storage<dtype> &&other);

  // acccess methods
  dtype &operator[](index_t index);
  const dtype &operator[](index_t index) const;

  const index_t size() const;
  const dtype *data() const;

  storage<dtype> &resize(index_t size);

  template <typename U>
  friend std::ostream &operator<<(std::ostream &, const storage<U> &);
};

} // namespace bs

#include "storage_impl.hpp"

#endif // BS_STORAGE_INC