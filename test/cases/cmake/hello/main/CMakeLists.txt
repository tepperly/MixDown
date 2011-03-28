cmake_minimum_required (VERSION 2.0)

project (Hello)

include_directories (${CMAKE_PREFIX_PATH}/include)

add_executable (hello main.cc)

find_library (LIBHELLO1 NAMES hello1 PATHS ${CMAKE_PREFIX_PATH} /usr/lib /usr/local/lib)
if (LIBHELLO1)
  target_link_libraries (hello ${LIBHELLO1})
endif ()

install (TARGETS hello DESTINATION bin)


