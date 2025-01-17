set(TODOGEN_PY ${CMAKE_CURRENT_LIST_DIR}/todogen.py)

find_program(Python3_EXECUTABLE NAMES python3 python REQUIRED)

set(TODOGEN_FOUND TRUE)

function(update_todos)
  set(options)
  set(oneValueArgs TARGET README SOURCE_DIR)
  cmake_parse_arguments(UPDATE_TODOS "${options}" "${oneValueArgs}" "" ${ARGN})

  if(NOT UPDATE_TODOS_TARGET)
    message(FATAL_ERROR "TARGET argument is required")
  endif()

  if(NOT UPDATE_TODOS_README)
    message(FATAL_ERROR "README argument is required")
  endif()

  if(NOT UPDATE_TODOS_SOURCE_DIR)
    message(FATAL_ERROR "SOURCE_DIR argument is required")
  endif()

  add_custom_target(
    ${UPDATE_TODOS_TARGET} ALL
    COMMAND ${Python3_EXECUTABLE} ${TODOGEN_PY} --readme ${UPDATE_TODOS_README}
            --src ${UPDATE_TODOS_SOURCE_DIR}
    COMMENT
      "Updating ${UPDATE_TODOS_README} with TODOs from ${UPDATE_TODOS_SOURCE_DIR}..."
  )
endfunction()
