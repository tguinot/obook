# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.16

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/quantumlabs/code/obook/liborderbook

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/quantumlabs/code/obook/liborderbook

# Include any dependencies generated for this target.
include CMakeFiles/orderbook_wrapper.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/orderbook_wrapper.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/orderbook_wrapper.dir/flags.make

CMakeFiles/orderbook_wrapper.dir/orderbook_wrapper.cpp.o: CMakeFiles/orderbook_wrapper.dir/flags.make
CMakeFiles/orderbook_wrapper.dir/orderbook_wrapper.cpp.o: orderbook_wrapper.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/quantumlabs/code/obook/liborderbook/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/orderbook_wrapper.dir/orderbook_wrapper.cpp.o"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/orderbook_wrapper.dir/orderbook_wrapper.cpp.o -c /home/quantumlabs/code/obook/liborderbook/orderbook_wrapper.cpp

CMakeFiles/orderbook_wrapper.dir/orderbook_wrapper.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/orderbook_wrapper.dir/orderbook_wrapper.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/quantumlabs/code/obook/liborderbook/orderbook_wrapper.cpp > CMakeFiles/orderbook_wrapper.dir/orderbook_wrapper.cpp.i

CMakeFiles/orderbook_wrapper.dir/orderbook_wrapper.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/orderbook_wrapper.dir/orderbook_wrapper.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/quantumlabs/code/obook/liborderbook/orderbook_wrapper.cpp -o CMakeFiles/orderbook_wrapper.dir/orderbook_wrapper.cpp.s

CMakeFiles/orderbook_wrapper.dir/sidebook.cpp.o: CMakeFiles/orderbook_wrapper.dir/flags.make
CMakeFiles/orderbook_wrapper.dir/sidebook.cpp.o: sidebook.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/quantumlabs/code/obook/liborderbook/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building CXX object CMakeFiles/orderbook_wrapper.dir/sidebook.cpp.o"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/orderbook_wrapper.dir/sidebook.cpp.o -c /home/quantumlabs/code/obook/liborderbook/sidebook.cpp

CMakeFiles/orderbook_wrapper.dir/sidebook.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/orderbook_wrapper.dir/sidebook.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/quantumlabs/code/obook/liborderbook/sidebook.cpp > CMakeFiles/orderbook_wrapper.dir/sidebook.cpp.i

CMakeFiles/orderbook_wrapper.dir/sidebook.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/orderbook_wrapper.dir/sidebook.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/quantumlabs/code/obook/liborderbook/sidebook.cpp -o CMakeFiles/orderbook_wrapper.dir/sidebook.cpp.s

CMakeFiles/orderbook_wrapper.dir/orderbook.cpp.o: CMakeFiles/orderbook_wrapper.dir/flags.make
CMakeFiles/orderbook_wrapper.dir/orderbook.cpp.o: orderbook.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/quantumlabs/code/obook/liborderbook/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Building CXX object CMakeFiles/orderbook_wrapper.dir/orderbook.cpp.o"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/orderbook_wrapper.dir/orderbook.cpp.o -c /home/quantumlabs/code/obook/liborderbook/orderbook.cpp

CMakeFiles/orderbook_wrapper.dir/orderbook.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/orderbook_wrapper.dir/orderbook.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/quantumlabs/code/obook/liborderbook/orderbook.cpp > CMakeFiles/orderbook_wrapper.dir/orderbook.cpp.i

CMakeFiles/orderbook_wrapper.dir/orderbook.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/orderbook_wrapper.dir/orderbook.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/quantumlabs/code/obook/liborderbook/orderbook.cpp -o CMakeFiles/orderbook_wrapper.dir/orderbook.cpp.s

CMakeFiles/orderbook_wrapper.dir/orderbook_python_funcs.cpp.o: CMakeFiles/orderbook_wrapper.dir/flags.make
CMakeFiles/orderbook_wrapper.dir/orderbook_python_funcs.cpp.o: orderbook_python_funcs.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/quantumlabs/code/obook/liborderbook/CMakeFiles --progress-num=$(CMAKE_PROGRESS_4) "Building CXX object CMakeFiles/orderbook_wrapper.dir/orderbook_python_funcs.cpp.o"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/orderbook_wrapper.dir/orderbook_python_funcs.cpp.o -c /home/quantumlabs/code/obook/liborderbook/orderbook_python_funcs.cpp

CMakeFiles/orderbook_wrapper.dir/orderbook_python_funcs.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/orderbook_wrapper.dir/orderbook_python_funcs.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/quantumlabs/code/obook/liborderbook/orderbook_python_funcs.cpp > CMakeFiles/orderbook_wrapper.dir/orderbook_python_funcs.cpp.i

CMakeFiles/orderbook_wrapper.dir/orderbook_python_funcs.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/orderbook_wrapper.dir/orderbook_python_funcs.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/quantumlabs/code/obook/liborderbook/orderbook_python_funcs.cpp -o CMakeFiles/orderbook_wrapper.dir/orderbook_python_funcs.cpp.s

CMakeFiles/orderbook_wrapper.dir/sidebook_python_funcs.cpp.o: CMakeFiles/orderbook_wrapper.dir/flags.make
CMakeFiles/orderbook_wrapper.dir/sidebook_python_funcs.cpp.o: sidebook_python_funcs.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/quantumlabs/code/obook/liborderbook/CMakeFiles --progress-num=$(CMAKE_PROGRESS_5) "Building CXX object CMakeFiles/orderbook_wrapper.dir/sidebook_python_funcs.cpp.o"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/orderbook_wrapper.dir/sidebook_python_funcs.cpp.o -c /home/quantumlabs/code/obook/liborderbook/sidebook_python_funcs.cpp

CMakeFiles/orderbook_wrapper.dir/sidebook_python_funcs.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/orderbook_wrapper.dir/sidebook_python_funcs.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/quantumlabs/code/obook/liborderbook/sidebook_python_funcs.cpp > CMakeFiles/orderbook_wrapper.dir/sidebook_python_funcs.cpp.i

CMakeFiles/orderbook_wrapper.dir/sidebook_python_funcs.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/orderbook_wrapper.dir/sidebook_python_funcs.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/quantumlabs/code/obook/liborderbook/sidebook_python_funcs.cpp -o CMakeFiles/orderbook_wrapper.dir/sidebook_python_funcs.cpp.s

# Object files for target orderbook_wrapper
orderbook_wrapper_OBJECTS = \
"CMakeFiles/orderbook_wrapper.dir/orderbook_wrapper.cpp.o" \
"CMakeFiles/orderbook_wrapper.dir/sidebook.cpp.o" \
"CMakeFiles/orderbook_wrapper.dir/orderbook.cpp.o" \
"CMakeFiles/orderbook_wrapper.dir/orderbook_python_funcs.cpp.o" \
"CMakeFiles/orderbook_wrapper.dir/sidebook_python_funcs.cpp.o"

# External object files for target orderbook_wrapper
orderbook_wrapper_EXTERNAL_OBJECTS =

orderbook_wrapper.so: CMakeFiles/orderbook_wrapper.dir/orderbook_wrapper.cpp.o
orderbook_wrapper.so: CMakeFiles/orderbook_wrapper.dir/sidebook.cpp.o
orderbook_wrapper.so: CMakeFiles/orderbook_wrapper.dir/orderbook.cpp.o
orderbook_wrapper.so: CMakeFiles/orderbook_wrapper.dir/orderbook_python_funcs.cpp.o
orderbook_wrapper.so: CMakeFiles/orderbook_wrapper.dir/sidebook_python_funcs.cpp.o
orderbook_wrapper.so: CMakeFiles/orderbook_wrapper.dir/build.make
orderbook_wrapper.so: /usr/lib/x86_64-linux-gnu/libpython3.8.so
orderbook_wrapper.so: CMakeFiles/orderbook_wrapper.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/quantumlabs/code/obook/liborderbook/CMakeFiles --progress-num=$(CMAKE_PROGRESS_6) "Linking CXX shared library orderbook_wrapper.so"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/orderbook_wrapper.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/orderbook_wrapper.dir/build: orderbook_wrapper.so

.PHONY : CMakeFiles/orderbook_wrapper.dir/build

CMakeFiles/orderbook_wrapper.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/orderbook_wrapper.dir/cmake_clean.cmake
.PHONY : CMakeFiles/orderbook_wrapper.dir/clean

CMakeFiles/orderbook_wrapper.dir/depend:
	cd /home/quantumlabs/code/obook/liborderbook && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/quantumlabs/code/obook/liborderbook /home/quantumlabs/code/obook/liborderbook /home/quantumlabs/code/obook/liborderbook /home/quantumlabs/code/obook/liborderbook /home/quantumlabs/code/obook/liborderbook/CMakeFiles/orderbook_wrapper.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/orderbook_wrapper.dir/depend

