#include "orderbook.hpp"
#include "boost/date_time/posix_time/posix_time.hpp"


using namespace boost::posix_time;
namespace py = boost::python;

py::list OrderbookReader::_py_side_up_to_volume_(SideBook *sb, number target_volume) {
  py::list result;
  sharable_lock<named_upgradable_mutex> rlock(*(sb->mutex));
  for (sidebook_ascender it=sb->begin(); it!=sb->end(); ++it){
     if (price(it) == sb->get_default_value())
       break;
     target_volume -= quantity(it);
     if (target_volume <= ZEROVAL) {
       number actual_quantity = quantity(it) + target_volume;
       result.append(py::make_tuple(py::make_tuple(price(it).numerator(), price(it).denominator()), py::make_tuple(actual_quantity.numerator(), actual_quantity.denominator())));
   
       break;
     }
    result.append(py::make_tuple(py::make_tuple(price(it).numerator(), price(it).denominator()), py::make_tuple(quantity(it).numerator(), quantity(it).denominator())));
   }
   return result;
}


void OrderbookWriter::py_set_quantity_at (order_side side, base_number new_qty_n, base_number new_qty_d, base_number new_price_n, base_number new_price_d) {
  set_quantity_at(side, number(new_qty_n, new_qty_d), number(new_price_n, new_price_d));
}

py::list OrderbookReader::py_bids_up_to_volume(base_number n, base_number d) {
  return _py_side_up_to_volume_(bids, number(n, d));
}

py::list OrderbookReader::py_asks_up_to_volume(base_number n, base_number d) {
  return _py_side_up_to_volume_(asks, number(n, d));
}

py::list OrderbookReader::py_snapshot_bids(int limit) {
  return bids->py_snapshot_to_limit(limit);
}

py::list OrderbookReader::py_snapshot_asks(int limit) {
  return asks->py_snapshot_to_limit(limit);
}

long OrderbookReader::py_bids_nonce() {
  long result;
  
  scoped_lock<named_upgradable_mutex> lock(*(bids->mutex), defer_lock);
  ptime locktime(second_clock::local_time());
  locktime = locktime + milliseconds(75);
  
  bool acquired_bids = lock.timed_lock(locktime);
  result = *(bids->update_number);
  if (!acquired_bids) {
    std::cout << "Failed to acquire bids nonce!" << std::endl;
  }

  return result;
}

long OrderbookReader::py_asks_nonce() {
    long result;
    
    scoped_lock<named_upgradable_mutex> lock(*(asks->mutex), defer_lock);
    ptime locktime(second_clock::local_time());
    locktime = locktime + milliseconds(75);

    bool acquired_asks = lock.timed_lock(locktime);
    result = *(asks->update_number);
    if (!acquired_asks) {
      std::cout << "Failed to acquire asks nonce!" << std::endl; 
    }

    return result;
}

py::tuple OrderbookReader::py_snapshot_whole(int limit) {
  ptime locktime(second_clock::local_time());
  locktime = locktime + milliseconds(75);

  py::list snapped_bids; 
  py::list snapped_asks;

  scoped_lock<named_upgradable_mutex> bidlock(*(bids->mutex), defer_lock);
  
  bool acquired_bids = bidlock.timed_lock(locktime);
  snapped_bids = bids->py_extract_to_limit(limit);
  if (!acquired_bids) {
    std::cout << "Failed to acquire bids in py_snapshot_whole!" << std::endl; 
  }

  scoped_lock<named_upgradable_mutex> asklock(*(asks->mutex), defer_lock);

  bool acquired_asks = asklock.timed_lock(locktime);
  snapped_asks = asks->py_extract_to_limit(limit);
  if (!acquired_asks) {
    std::cout << "Failed to acquire asks in py_snapshot_whole!" << std::endl; 
  }
  return py::make_tuple(snapped_bids, snapped_asks);
}

py::tuple OrderbookReader::py_first_price (bool side) {
    number top_price = first_price(side);
    return py::make_tuple(top_price.numerator(), top_price.denominator());
}
