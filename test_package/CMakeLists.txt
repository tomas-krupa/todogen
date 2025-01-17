cmake_minimum_required(VERSION 3.15)

project(test_package)

find_package(ToDoGen REQUIRED)

configure_file(${CMAKE_SOURCE_DIR}/README.md
               ${CMAKE_CURRENT_BINARY_DIR}/README.md COPYONLY)

update_todos(TARGET update_todos_in_readme README ${CMAKE_BINARY_DIR}/README.md
             SOURCE_DIR ${CMAKE_SOURCE_DIR})
