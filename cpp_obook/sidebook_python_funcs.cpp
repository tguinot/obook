#include "sidebook.hpp"

namespace py = boost::python;

py::list SideBook::py_snapshot_to_limit(int limit){
    py::list result;
    int i = 0;
    sharable_lock<named_upgradable_mutex> lock(*mutex);
    for (sidebook_ascender it=data->begin(); it!=data->end(); it++){
        if (i >= limit || price(it) == default_value)
            break;
        result.append(py::make_tuple(py::make_tuple(price(it).numerator(), price(it).denominator()),
                                     py::make_tuple(quantity(it).numerator(), quantity(it).denominator()),
                                     py::make_tuple((*it)[2].numerator(), (*it)[2].denominator()),
                py::make_tuple((*it)[3].numerator(), (*it)[3].denominator()),
                py::make_tuple((*it)[4].numerator(), (*it)[4].denominator()),
                py::make_tuple((*it)[5].numerator(), (*it)[5].denominator()),
                py::make_tuple((*it)[6].numerator(), (*it)[6].denominator()),
                py::make_tuple((*it)[7].numerator(), (*it)[7].denominator()),
                py::make_tuple((*it)[8].numerator(), (*it)[8].denominator()),
                py::make_tuple((*it)[9].numerator(), (*it)[9].denominator()),
                py::make_tuple((*it)[10].numerator(), (*it)[10].denominator()),
                py::make_tuple((*it)[11].numerator(), (*it)[11].denominator())));
        i++;
    }
    return result;
}
