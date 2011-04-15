cmake_minimum_required (VERSION 2.0)

project (HelloLibrary1)

add_library (hello1 hello1.cc)

install (TARGETS hello1 DESTINATION lib)
install (FILES hello1.h DESTINATION include)

