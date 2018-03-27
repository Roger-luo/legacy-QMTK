#ifndef QMTK_SITE_INC
#define QMTK_SITE_INC

#include "general.h"

namespace qmtk {

/**
 * @brief this class wraps a site on arbitrary lattices
 */
class site {
public:

  site();
  site(const index_t *data, dim_t ndim);
  site(index_t i0);
  site(index_t i0, index_t i1);
  site(index_t i0, index_t i1, index_t i2);
  site(index_t i0, index_t i1, index_t i2, index_t i3);
  site(const site &other);
  site(site &&other);
  ~site();

  /**
   * @brief get index without bound check
   */
  inline index_t &get(dim_t index);

  /**
   * @brief get index with bound check
   */
  index_t& operator[](dim_t index);
  const index_t& operator[](dim_t index) const;

  /**
   * @brief output stream, this will take the style
   * of python tuple.
   */

  site &operator+=(const site &other);
  site &operator-=(const site &other);
  site &operator+=(const index_t &other);
  site &operator-=(const index_t &other);

  friend std::ostream& operator<<(std::ostream &os, const site &s);

  index_t *_data;
  dim_t _ndim;
};

site make_site(dim_t ndim);

/* operator overloading
 * binary operator acts like vectors.
 */
site operator+(const site &lhs, const site &rhs);
site operator-(const site &lhs, const site &rhs);

site operator+(const site &lhs, const index_t &rhs);
site operator-(const site &lhs, const index_t &rhs);

site operator+(const index_t &lhs, const site &rhs);
site operator-(const index_t &lhs, const site &rhs);

/*
 * compare operators
 */
bool operator==(const site &lhs, const site &rhs);
bool operator!=(const site &lhs, const site &rhs);

/*
 * only 1 dim site can compare to a scalar int.
 */
bool operator==(const site &lhs, const index_t &rhs);
bool operator!=(const site &lhs, const index_t &rhs);

bool operator==(const index_t &lhs, const site &rhs);
bool operator!=(const index_t &lhs, const site &rhs);

using bond = std::tuple<site, site>;

using site_list = std::vector<site>;
using bond_list = std::vector<bond>;

inline bond make_bond(index_t A, index_t B) {
  return std::make_tuple(site(A), site(B));
}

inline bond make_bond(index_t A0, index_t A1, index_t B0, index_t B1) {
  return std::make_tuple(site(A0, A1), site(B0, B1));
} 

}
#endif