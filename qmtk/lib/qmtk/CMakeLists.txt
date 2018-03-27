cmake_minimum_required(VERSION 2.6)

if(POLICY CMP0026)
  cmake_policy(SET CMP0026 OLD)    
endif(POLICY CMP0026)

set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake ${CMAKE_MODULE_PATH})
set(CMAKE_LIBRARY_PATH /usr/lib/x86_64-linux-gnu/ ${CMAKE_LIBRARY_PATH})

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3")

# set(VECTOR_DIAG ON)
set(VECTOR_VERBOSE ON)

if(VECTOR_DIAG)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Rpass-missed=loop-vectorize")
endif(VECTOR_DIAG)

if(VECTOR_VERBOSE)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Rpass=loop-vectorize")
endif(VECTOR_VERBOSE)

# set(CMAKE_VERBOSE_MAKEFILE ON)

set(hdr qmtk.h site.h lattice.h shape.h)
set(src site.cpp lattice.cpp shape.cpp)
set(src ${src} ${hdr})

include_directories((${CMAKE_CURRENT_SOURCE_DIR}))
add_library(qmtk SHARED ${src})

include(CTest)
enable_testing()

add_executable(test_qmtk test/test.cpp)
target_link_libraries(test_qmtk gtest pthread qmtk)

add_test(all_tests test_qmtk)