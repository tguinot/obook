#include "orderbook.hpp"

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

py::tuple OrderbookReader::py_snapshot_whole(int limit) {
  sharable_lock<named_upgradable_mutex> bids_lock(*(bids->mutex));
  sharable_lock<named_upgradable_mutex> asks_lock(*(asks->mutex));

  py::list snapped_bids = bids->py_snapshot_to_limit(limit);
  py::list snapped_asks = asks->py_snapshot_to_limit(limit);
  return py::make_tuple(snapped_bids, snapped_asks);
}

py::tuple OrderbookReader::py_first_price (bool side) {
    number top_price = first_price(side);
    return py::make_tuple(top_price.numerator(), top_price.denominator());
}
