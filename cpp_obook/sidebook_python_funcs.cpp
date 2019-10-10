#include "sidebook.hpp"

namespace py = boost::python;

py::list SideBook::py_snapshot_to_limit(int limit){
    py::list result;
    int i = 0;
    sharable_lock<named_upgradable_mutex> lock(*mutex);
    for (sidebook_ascender it=data->begin(); it!=data->end(); it++){
        if (i >= limit || price(it) == default_value)
            break;
        py::list row;
        for (size_t j=0; j<EXCHANGECOUNT+2; j++)
            row.append(py::make_tuple((*it)[j].numerator(), (*it)[j].denominator()));
        result.append(row);
        i++;
    }
    return result;
}
