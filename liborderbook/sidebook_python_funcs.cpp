#include "sidebook.hpp"
#include <boost/interprocess/sync/lock_options.hpp>
#include "boost/date_time/posix_time/posix_time.hpp"

namespace py = boost::python;
using namespace boost::interprocess;
using namespace boost::posix_time;

py::list SideBook::py_extract_to_limit(int limit){
  py::list result;
  int i = 0;
  for (sidebook_ascender it=data->begin(); it!=data->end(); it++){
    if (i >= limit || price(it) == default_value)
      break;
    result.append(py::make_tuple(py::make_tuple(price(it).numerator(), price(it).denominator()), py::make_tuple(quantity(it).numerator(), quantity(it).denominator())));
    i++;
  }
  return result;
}

py::list SideBook::py_snapshot_to_limit(int limit){
  scoped_lock<named_upgradable_mutex> lock(*mutex, defer_lock);
  ptime locktime(second_clock::local_time());
  locktime = locktime + milliseconds(75);
  
  bool acquired = lock.timed_lock(locktime);
  if (!acquired) {
    std::cout << "Unable to acquire memory in py_snapshot_to_limit" << std::endl;
  }
  
  return py_extract_to_limit(limit);
}
