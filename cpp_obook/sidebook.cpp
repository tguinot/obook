#include "sidebook.hpp"
#include <iostream>
#include <boost/interprocess/sync/scoped_lock.hpp>
#include <boost/interprocess/sync/named_mutex.hpp>
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

bool compare_s(orderbook_entry_type a, orderbook_entry_type b){
    return (a[0] < b[0]);
}

bool compare_b(orderbook_entry_type a, orderbook_entry_type b){
    return (a[0] > b[0]);
}

void SideBook::setup_segment(std::string path, shm_mode mode){
    if (mode == read_write_shm)
        segment = new managed_shared_memory(open_or_create, path.c_str(), 90000);
    else if (mode == read_shm)
        segment = new managed_shared_memory(open_only, path.c_str());
}

SideBook::SideBook(std::string path, shm_mode mode, number fill_value){
    mutex = new named_mutex(open_or_create, path.c_str());
    setup_segment(path, mode);
    data = segment->find_or_construct< sidebook_content > ("unique")();
    default_value = fill_value;
    book_mode = mode;
    reset_content();
}

void SideBook::reset_content(){
    if (book_mode == read_write_shm) fill_with(default_value);
}

void SideBook::fill_with(number fillNumber){
    scoped_lock<named_mutex> lock(*mutex);
    for (sidebook_content::iterator i= data->begin(); i!=data->end(); i++){
        (*i)[0] = fillNumber;
        (*i)[1] = fillNumber;
    }
}

number** SideBook::snapshot_to_limit(int limit){
 number** result = new number*[limit];
 int i = 0;
 scoped_lock<named_mutex> lock(*mutex);
 for (sidebook_ascender it=data->begin(); it!=data->end(); i++){
    if (i >= limit || price(it) == default_value)
      break;

    result[i] = new number[2];
    result[i][0] = price(it);
    result[i][1] = quantity(it);
    //i++;
  }
  return result;
}

sidebook_ascender SideBook::begin() {
    return data->begin();
}

sidebook_ascender SideBook::end() {
    return data->end();
}

void SideBook::insert_at_place(sidebook_content *data, orderbook_entry_type to_insert, sidebook_content::iterator loc){
    if (loc == data->end())
        return;
    if ((*loc)[0] != to_insert[0] && to_insert[1].numerator() != 0){
        std::rotate(loc, data->end()-1, data->end());

        (*loc)[0] = to_insert[0];
        (*loc)[1] = to_insert[1];
    } else if ((*loc)[0] == to_insert[0] && to_insert[1].numerator() == 0) {
        std::copy(loc+1,data->end(), loc);
        data->back()[0] = default_value;
        data->back()[1] = default_value;
    } else if (to_insert[1].numerator() != 0){
        (*loc)[1] = to_insert[1];
    }
}

void SideBook::insert_ask(number new_price, number new_quantity) {
    scoped_lock<named_mutex> lock(*mutex);
    orderbook_entry_type to_insert = {new_price, new_quantity};
    sidebook_content::iterator loc = std::lower_bound<sidebook_content::iterator, orderbook_entry_type>(data->begin(), data->end(), to_insert, compare_s);
    insert_at_place(data, to_insert, loc);
}

void SideBook::insert_bid(number new_price, number new_quantity) {
    scoped_lock<named_mutex> lock(*mutex);
    orderbook_entry_type to_insert = {new_price, new_quantity};
    sidebook_content::iterator loc = std::lower_bound<sidebook_content::iterator, orderbook_entry_type>(data->begin(), data->end(), to_insert, compare_b);
    insert_at_place(data, to_insert, loc);
}
