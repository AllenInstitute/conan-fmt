project(cmake_wrapper)

include(conanbuildinfo.cmake)
CONAN_BASIC_SETUP(TARGETS)

add_subdirectory("sources")
