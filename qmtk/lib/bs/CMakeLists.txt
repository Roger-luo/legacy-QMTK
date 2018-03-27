cmake_minimum_required(VERSION 3.2)

project(biscuit VERSION 0.1 LANGUAGES C CXX)

if(POLICY CMP0026)
  cmake_policy(SET CMP0026 OLD)    
endif(POLICY CMP0026)

option(VECTOR_DIAG      "Set to ON to see vectorize diagnose"   OFF)
option(VECTOR_VERBOSE   "Set to ON to see vectorize verbose"    OFF)

option(BUILD_TESTS      "Set to ON to build tests"              ON)
option(BUILD_EXAMPLES   "Set to ON to build examples"           ON)
option(BUILD_DOCS       "Set to ON to build documentation"      OFF)
option(BUILD_BENCHMARKS "Set to ON to build benchmarks"         OFF)
option(COVERALLS        "Set to ON to build with code coverage" OFF)
option(PROFILE          "Set to ON to build with profiling"     OFF)
# set(CMAKE_VERBOSE_MAKEFILE ON)


set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake ${CMAKE_MODULE_PATH})
set(CMAKE_LIBRARY_PATH /usr/lib/x86_64-linux-gnu/ ${CMAKE_LIBRARY_PATH})

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
message(STATUS "C++11 support has been enabled by default.")

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3")

if(PROFILE AND (CMAKE_COMPILER_IS_GNUCXX OR MINGW OR
    CMAKE_CXX_COMPILER_ID MATCHES "Clang"))
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -pg")
endif()

# for diagnose
if(VECTOR_DIAG)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Rpass-missed=loop-vectorize")
endif(VECTOR_DIAG)

if(VECTOR_VERBOSE)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Rpass=loop-vectorize")
endif(VECTOR_VERBOSE)

#########################

# OpenMP support?
SET(WITH_OPENMP ON CACHE BOOL "OpenMP support if available?")
IF (APPLE AND CMAKE_COMPILER_IS_GNUCC)
  EXEC_PROGRAM (uname ARGS -v  OUTPUT_VARIABLE DARWIN_VERSION)
  STRING (REGEX MATCH "[0-9]+" DARWIN_VERSION ${DARWIN_VERSION})
  MESSAGE (STATUS "MAC OS Darwin Version: ${DARWIN_VERSION}")
  IF (DARWIN_VERSION GREATER 9)
    SET(APPLE_OPENMP_SUCKS 1)
  ENDIF (DARWIN_VERSION GREATER 9)
  EXECUTE_PROCESS (COMMAND ${CMAKE_C_COMPILER} -dumpversion
    OUTPUT_VARIABLE GCC_VERSION)
  IF (APPLE_OPENMP_SUCKS AND GCC_VERSION VERSION_LESS 4.6.2)
    MESSAGE(STATUS "Warning: Disabling OpenMP (unstable with this version of GCC)")
    MESSAGE(STATUS " Install GCC >= 4.6.2 or change your OS to enable OpenMP")
    SET(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wno-unknown-pragmas")
    SET(WITH_OPENMP OFF CACHE BOOL "OpenMP support if available?" FORCE)
  ENDIF ()
ENDIF ()

IF (WITH_OPENMP)
  FIND_PACKAGE(OpenMP)
  IF(OPENMP_FOUND)
    MESSAGE(STATUS "Compiling with OpenMP support")
    SET(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
    SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
    SET(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_EXE_LINKER_FLAGS}")
  ENDIF(OPENMP_FOUND)
ENDIF (WITH_OPENMP)

#####################################

# BLAS

add_library(biscuit INTERFACE)
target_include_directories(biscuit INTERFACE
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include/>
  $<INSTALL_INTERFACE:include/biscuit>
)

find_package(BLAS)
if(BLAS_FOUND)
  set(USE_BLAS 1)
  target_link_libraries(biscuit INTERFACE ${BLAS_LIBRARIES})

  if(BLAS_INFO STREQUAL "mkl")
    add_definitions(-DBS_BLAS_MKL)
  endif()
endif()

find_package(LAPACK)
if(LAPACK_FOUND)
  set(USE_LAPACK 1)
  target_link_libraries(biscuit INTERFACE ${LAPACK_LIBRARIES})
endif()

if(BUILD_TESTS)
  add_subdirectory(test)
endif()

