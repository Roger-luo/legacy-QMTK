include(CTest)
enable_testing()

MACRO(add_test_case section case)
add_executable("${section}_${case}.test" "${section}/${case}.cpp")
target_link_libraries("${section}_${case}.test" gtest pthread biscuit)
add_test("${section}_${case}" "${section}_${case}.test")
ENDMACRO()

# get subdirectories.
# https://stackoverflow.com/questions/
# 7787823/cmake-how-to-get-the-name-of-
# all-subdirectories-of-a-directory

MACRO(SUBDIRLIST result curdir)
  FILE(GLOB children RELATIVE ${curdir} ${curdir}/*)
  SET(dirlist "")
  FOREACH(child ${children})
    IF(IS_DIRECTORY ${curdir}/${child})
      LIST(APPEND dirlist ${child})
    ENDIF()
  ENDFOREACH()
  SET(${result} ${dirlist})
ENDMACRO()


add_executable(main.test test.cpp)
target_link_libraries(main.test gtest pthread biscuit)
add_test(all_tests main.test)
# workaround for https://gitlab.kitware.com/cmake/cmake/issues/8774
add_custom_target(run_tests COMMAND ${CMAKE_CTEST_COMMAND}
    DEPENDS main.test)

# SUBDIRLIST(ALL_TEST_SECTIONS ${CMAKE_CURRENT_SOURCE_DIR})

# FOREACH(section ${ALL_TEST_SECTIONS})
#   file(GLOB TEST_CASES "${CMAKE_CURRENT_SOURCE_DIR}/${section}/*.cpp")
#   FOREACH(case ${TEST_CASES})
#     get_filename_component(case ${case} NAME_WE)
#     add_test_case(${section} ${case})
#   ENDFOREACH()
# ENDFOREACH()