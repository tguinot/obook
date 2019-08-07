cmake_minimum_required(VERSION 2.8)
include(ExternalProject)

list(APPEND CMAKE_MODULE_PATH  "${CMAKE_SOURCE_DIR}/cmake/Modules/")

project(tutorial)

  #find_package(PythonInterp REQUIRED)
  find_package(Python3 COMPONENTS Interpreter Development)
  find_package(PythonLibs REQUIRED)
  include(BuildBoost)

  include_directories(${Boost_INCLUDE_DIR} ${PYTHON_INCLUDE_DIRS})
  link_directories(${Boost_LIBRARY_DIR})

  add_library(orderbook_wrapper SHARED orderbook_wrapper.cpp sidebook.cpp orderbook.cpp orderbook_python_funcs.cpp sidebook_python_funcs.cpp)
  target_link_libraries(orderbook_wrapper ${Boost_LIBRARIES} ${PYTHON_LIBRARIES})
  target_link_libraries(orderbook_wrapper rt)
  add_dependencies(orderbook_wrapper Boost)

  set_target_properties(orderbook_wrapper PROPERTIES SUFFIX .so)
  set_target_properties(orderbook_wrapper PROPERTIES PREFIX "")
