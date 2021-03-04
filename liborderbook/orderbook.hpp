#include <iostream>
#include <string>
#include "sidebook.hpp"
#include <boost/python/numpy.hpp>
#include <tuple>

#define BID_PATH_SUFFIX "_bids"
#define ASK_PATH_SUFFIX "_asks"

#define BID true
#define ASK false

typedef bool order_side;


class OrderbookReader {
  protected:
    SideBook *bids, *asks;
    std::pair<number**, int> _side_up_to_volume_(SideBook*, number);
    boost::python::list _py_side_up_to_volume_(SideBook*, number);


  public:
    virtual void init_shm (std::string);

    std::pair<number**, int> bids_up_to_volume (number);
    std::pair<number**, int> asks_up_to_volume (number);

    boost::python::list py_asks_up_to_volume(base_number n, base_number d);
    boost::python::list py_bids_up_to_volume(base_number n, base_number d);

    boost::python::list py_snapshot_bids(int);
    boost::python::list py_snapshot_asks(int);
    boost::python::tuple py_snapshot_whole(int);

    long py_bids_nonce();
    long py_asks_nonce();

    boost::python::tuple py_first_price(bool);

    number first_price (bool side) {
      return side == BID ? price(bids->begin()) : price(asks->begin());
    }

    void display_side (order_side);
};


class OrderbookWriter: public OrderbookReader {
  public:
  	
    void init_shm (std::string);
    void reset_content();
    void set_quantity_at (order_side, number, number);
    void py_set_quantity_at (order_side, base_number, base_number, base_number, base_number);
 };

