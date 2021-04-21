#include "sidebook.hpp"
#include <iostream>
#include <boost/interprocess/sync/scoped_lock.hpp>
#include <boost/interprocess/sync/sharable_lock.hpp>
#include <boost/interprocess/sync/lock_options.hpp>
#include "boost/date_time/posix_time/posix_time.hpp"
#include <algorithm>

using namespace boost::posix_time;

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
    std::string mutex_path = path + "_mutex";
    // std::cout << "Creating upgradable mutex " << mutex_path << std::endl;
    mutex = new named_upgradable_mutex(open_or_create, mutex_path.c_str());
    // std::cout << "Setting up SHM segment " << path << std::endl;
    setup_segment(path, mode);
    // std::cout << "Constructing SHM objects " << path << std::endl;
    data = segment->find_or_construct< sidebook_content > ("unique")();
    update_number = segment->find_or_construct< long > ("nonce")();
    default_value = fill_value;
    book_mode = mode;
    // std::cout << "Resetting SHM object " << path << std::endl;
    reset_content();
}

void SideBook::reset_content(){
    if (book_mode == read_write_shm) {
        *update_number = 0;
        fill_with(default_value);
    }
}

void SideBook::fill_with(number fillNumber){
    scoped_lock<named_upgradable_mutex> lock(*mutex, defer_lock);
    ptime locktime(microsec_clock::local_time());
    locktime = locktime + milliseconds(75);
    
    bool acquired = lock.timed_lock(locktime);
    for (sidebook_content::iterator i= data->begin(); i!=data->end(); i++){
        (*i)[0] = fillNumber;
        (*i)[1] = fillNumber;
    }
    (*update_number)++;
    if (!acquired) {
        std::cout << "Unable to acquire memory in fill_with" << std::endl;
    } else {
        lock.unlock();
    }
}

number** SideBook::extract_to_limit(int limit){
    number** result = new number*[limit];
    int i = 0;
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

number** SideBook::snapshot_to_limit(int limit){
    scoped_lock<named_upgradable_mutex> lock(*mutex, defer_lock);
    ptime locktime(microsec_clock::local_time());
    locktime = locktime + milliseconds(75);
    
    bool acquired = lock.timed_lock(locktime);
    if (!acquired) {
        std::cout << "Unable to acquire memory in snapshot_to_limit" << std::endl;
    }
    return extract_to_limit(limit);
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
    (*update_number)++;
}

void SideBook::_delete_first_entry(){
    std::copy(data->begin()+1, data->end(), data->begin());
        data->back()[0] = default_value;
        data->back()[1] = default_value;
}

void SideBook::clean_first_limit() {
    scoped_lock<named_upgradable_mutex> lock(*mutex, defer_lock);
    ptime locktime(microsec_clock::local_time());
    locktime = locktime + milliseconds(75);

    bool acquired = lock.timed_lock(locktime);
    _delete_first_entry();
    if (!acquired) {
        std::cout << "Unable to acquire memory in insert_ask" << std::endl;
    } else {
        lock.unlock();
    }
}

void SideBook::insert_ask(number new_price, number new_quantity) {
    orderbook_entry_type to_insert = {new_price, new_quantity};

    scoped_lock<named_upgradable_mutex> lock(*mutex, defer_lock);
    ptime locktime(microsec_clock::local_time());
    locktime = locktime + milliseconds(75);
    
    bool acquired = lock.timed_lock(locktime);
    sidebook_content::iterator loc = std::lower_bound<sidebook_content::iterator, orderbook_entry_type>(data->begin(), data->end(), to_insert, compare_s);
    insert_at_place(data, to_insert, loc);
    if (!acquired) {
        std::cout << "Unable to acquire memory in insert_ask" << std::endl;
    } else {
        lock.unlock();
    }
}

void SideBook::insert_ask_no_lock(number new_price, number new_quantity) {
    orderbook_entry_type to_insert = {new_price, new_quantity};

    sidebook_content::iterator loc = std::lower_bound<sidebook_content::iterator, orderbook_entry_type>(data->begin(), data->end(), to_insert, compare_s);
    insert_at_place(data, to_insert, loc);
}

void SideBook::insert_bid(number new_price, number new_quantity) {
    orderbook_entry_type to_insert = {new_price, new_quantity};

    scoped_lock<named_upgradable_mutex> lock(*mutex, defer_lock);
    ptime locktime(microsec_clock::local_time());
    locktime = locktime + milliseconds(75);
    bool acquired = lock.timed_lock(locktime);
    
    sidebook_content::iterator loc = std::lower_bound<sidebook_content::iterator, orderbook_entry_type>(data->begin(), data->end(), to_insert, compare_b);
    insert_at_place(data, to_insert, loc);

    if (!acquired) {
        std::cout << "Unable to acquire memory in insert_bid" << std::endl;
    } else {
        lock.unlock();
    }
}

void SideBook::insert_bid_no_lock(number new_price, number new_quantity) {
    orderbook_entry_type to_insert = {new_price, new_quantity};

    sidebook_content::iterator loc = std::lower_bound<sidebook_content::iterator, orderbook_entry_type>(data->begin(), data->end(), to_insert, compare_b);
    insert_at_place(data, to_insert, loc);
}