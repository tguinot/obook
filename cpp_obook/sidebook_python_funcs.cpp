#include "sidebook.hpp"
#include <boost/interprocess/sync/named_mutex.hpp>

namespace py = boost::python;

py::list SideBook::py_snapshot_to_limit(int limit){
  py::list result;
  int i = 0;
  scoped_lock<named_mutex> lock(*mutex);
  for (sidebook_ascender it=data->begin(); it!=data->end(); it++){
    if (i >= limit || price(it) == default_value)
      break;
    result.append(py::make_tuple(py::make_tuple(price(it).numerator(), price(it).denominator()), py::make_tuple(quantity(it).numerator(), quantity(it).denominator())));
    i++;
  }
  return result;
}
