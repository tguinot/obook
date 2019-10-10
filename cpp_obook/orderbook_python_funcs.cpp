#include "orderbook.hpp"

namespace py = boost::python;

py::list OrderbookReader::_py_side_up_to_volume_(SideBook *sb, number target_volume) {
    py::list result;
    sharable_lock<named_upgradable_mutex> lock(*sb->mutex);
    for (sidebook_ascender it=sb->begin(); it!=sb->end(); ++it){
        if (price(it) == sb->get_default_value())
            break;
        target_volume -= quantity(it);
        if (target_volume <= ZEROVAL) {
            result.append(py::make_tuple(price(it),  (quantity(it) + target_volume)));
            break;
        }
        result.append(py::make_tuple(price(it), quantity(it)));
    }
    return result;
}


void OrderbookWriter::py_set_quantity_at (order_side side, base_number new_qty_n, base_number new_qty_d, base_number new_price_n, base_number new_price_d, exchange_type exchange) {
    set_quantity_at(side, number(new_qty_n, new_qty_d), number(new_price_n, new_price_d), exchange);
}

py::list OrderbookReader::py_bids_up_to_volume(number target_volume) {
    return _py_side_up_to_volume_(bids, target_volume);
}

py::list OrderbookReader::py_asks_up_to_volume(number target_volume) {
    return _py_side_up_to_volume_(asks, target_volume);
}

py::list OrderbookReader::py_snapshot_bids(int limit) {
    return bids->py_snapshot_to_limit(limit);
}

py::list OrderbookReader::py_snapshot_asks(int limit) {
    return asks->py_snapshot_to_limit(limit);
}

py::tuple OrderbookReader::py_first_price (bool side) {
    number top_price = first_price(side);
    return py::make_tuple(top_price.numerator(), top_price.denominator());
}
