#include "sidebook.hpp"
#include <iostream>
#include <boost/interprocess/sync/scoped_lock.hpp>
#include <boost/interprocess/sync/sharable_lock.hpp>
#include <numeric>
#include <algorithm>

number quantity(sidebook_content::iterator loc) {
    return (*loc)[1];
}

number price(sidebook_content::iterator loc) {
    return (*loc)[0];
}

number quantity(sidebook_content::reverse_iterator loc) {
    return (*loc)[1];
}

number price(sidebook_content::reverse_iterator loc) {
    return (*loc)[0];
}

bool compare_s(orderbook_row_type a, orderbook_row_type b){
    return (a[0] < b[0]);
}

bool compare_b(orderbook_row_type a, orderbook_row_type b){
    return (a[0] > b[0]);
}

void SideBook::setup_segment(std::string path, shm_mode mode){
    if (mode == read_write_shm)
        segment = new managed_shared_memory(open_or_create, path.c_str(), 500000);
    else if (mode == read_shm)
        segment = new managed_shared_memory(open_only, path.c_str());
}

SideBook::SideBook(std::string path, shm_mode mode, number fill_value){
    std::string mutex_path = path + "_mutex";
    std::cout << "Creating upgradable mutex " << mutex_path << std::endl;
    mutex = new named_upgradable_mutex(open_or_create, mutex_path.c_str());
    std::cout << "Setting up SHM segment " << path << std::endl;
    setup_segment(path, mode);
    std::cout << "Constructing SHM object " << path << std::endl;
    data = segment->find_or_construct< sidebook_content > ("unique")();
    default_value = fill_value;
    book_mode = mode;
    std::cout << "Resetting SHM object " << path << std::endl;
    reset_content();
}

void SideBook::reset_content(){
    if (book_mode == read_write_shm) fill_with(default_value);
}

void SideBook::fill_with(number fillNumber){
    scoped_lock<named_upgradable_mutex> lock(*mutex);
    for (sidebook_content::iterator i= data->begin(); i!=data->end(); i++){
        for (size_t j=0; j<EXCHANGECOUNT+2; j++)
            (*i)[j] = fillNumber;
    }
}

number** SideBook::snapshot_to_limit(int limit){
    number** result = new number*[limit];
    int i = 0;
    sharable_lock<named_upgradable_mutex> lock(*mutex);
    for (sidebook_ascender it=data->begin(); it!=data->end(); i++){
        if (i >= limit || price(it) == default_value)
            break;
        result[i] = new number[2+EXCHANGECOUNT];
        result[i][0] = price(it);
        result[i][1] = quantity(it);
        for (size_t j=2; j<EXCHANGECOUNT+2; j++)
            result[i][j] = (*it)[j];
    }
    return result;
}

sidebook_ascender SideBook::begin() {
    return data->begin();
}

sidebook_ascender SideBook::end() {
    return data->end();
}

number SideBook::get_row_total(orderbook_row_type *loc){
    number total = ZEROVAL;
    number *start = loc->data();
    return std::accumulate(start+2, start+2+EXCHANGECOUNT, total);
}

void SideBook::rotate_right_and_insert_entry(sidebook_content *content, orderbook_entry_type new_entry, exchange_type exchange, sidebook_content::iterator location) {
    std::rotate(location, content->end()-1, content->end());
    (*location)[0] = new_entry[0];
    (*location)[exchange] = new_entry[1];
    (*location)[1] = get_row_total(location);
}

void SideBook::remove_entry(sidebook_content *content, orderbook_entry_type new_entry, exchange_type exchange, sidebook_content::iterator location) {
    (*location)[exchange] = new_entry[1];
    (*location)[1] = get_row_total(location);
    if ((*location)[1] != ZEROVAL)
        return;
    std::copy(location+1,content->end(), location);
    content->back()[0] = default_value;
    content->back()[1] = default_value;
}

void SideBook::insert_at_place(sidebook_content *data, orderbook_entry_type to_insert, exchange_type exchange, sidebook_content::iterator loc){
    if (loc == data->end())
        return;
    // if price is not the one at location, rotate right and insert at location
    if ((*loc)[0] != to_insert[0] && to_insert[1].numerator() != 0){
        rotate_right_and_insert_entry(data, to_insert, exchange, loc);
        // if price is the one at location and quantity is 0, rotate left and fill back with default val
    } else if ((*loc)[0] == to_insert[0] && to_insert[1].numerator() == 0) {
        remove_entry(data, to_insert, exchange, loc);
        // if price is the one at location and quantity is NOT 0, change quantity
    } else if (to_insert[1].numerator() != 0){
        (*loc)[exchange] = to_insert[1];
        (*loc)[1] = get_row_total(loc);
    }
}

void SideBook::_insert(number new_price, number new_quantity, bool (*comp)(orderbook_row_type, orderbook_row_type), exchange_type exchange) {
    scoped_lock<named_upgradable_mutex> lock(*mutex);
    orderbook_entry_type to_insert = {new_price, new_quantity};
    orderbook_row_type to_cmp = {new_price, new_quantity};
    sidebook_content::iterator loc = std::lower_bound<sidebook_content::iterator, orderbook_row_type>(data->begin(), data->end(), to_cmp, comp);
    exchange += 2;
    insert_at_place(data, to_insert, exchange, loc);
}

void SideBook::insert_ask(number new_price, number new_quantity, exchange_type exchange) {
    _insert(new_price, new_quantity, compare_s, exchange);
}

void SideBook::insert_bid(number new_price, number new_quantity, exchange_type exchange) {
    _insert(new_price, new_quantity, compare_b, exchange);
}
