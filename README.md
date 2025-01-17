

# ToDoGen
**ToDoGen**, aka ToDo Generator, is a simple Python utility for inspecting source code for `TODO` comments and generating a TODO list as a section in the README file.
ToDoGen is provided as a Conan package, exposing a CMake target.

## Usage
Use the python script to generate TODOs section for readme:
```bash
python todogen.py --readme <README_FILE> --src <PROJECT_SOURCE_DIR>
```
Or integrate it as a CMake target in you build system:
```cmake
# when using `cmake` conan generator
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

# when using CMakeDeps or cmake_find_package* conan generators
find_package(ToDoGen REQUIRED)

update_todos(
        TARGET update_todos_in_readme
        README ${CMAKE_SOURCE_DIR}/README.md
        SOURCE_DIR ${CMAKE_SOURCE_DIR}/src)
```
together with consuming it in your `conanfile.py`:
```python
    def build_requirements(self):
        self.tool_requires("todogen/<VERSION>")
```
## Build conan package
To create and store the package in the local cache, run the following command in the source directory:
```bash
conan create .
```
