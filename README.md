

# ToDoGen
**ToDoGen**, aka ToDo Generator, is a simple Python utility for inspecting source code for `TODO` comments and generating a TODO list as a section in the README file.
- For **C/C++** projects, ToDoGen is distributed as a Conan package that provides a CMake target.
- For **Java/Kotlin** and projects, ToDoGen is available as a Gradle plugin that provides a Gradle task.

## Usage
Use the python script to generate TODOs section for readme:
```bash
python todogen.py --readme <README_FILE> --src <PROJECT_SOURCE_DIR>
```

## Integration

### C/C++ integration
To integrate it as a CMake target in you C/C++ build system, add
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
        self.tool_requires("todogen/<VERSION>@mta/master")
```

### Java/Kotlin integration
To integrate TodoGen as a Gradle plugin in you Java/Kotlin build system, include the plugin in your `build.gradle`
```gradle
plugins {
    id '<GROUP>.todogen' version '1.1.0'
}
```
and use the generator task to the build system
```gradle
todogen {
    srcDir = file("$rootDir/src")
    readme = file("$rootDir/README.md")
}
```
If you want the task to be run automatically during build, add:
```gradle
tasks.matching { it.name in ["assemble", "preBuild", "build"] }.configureEach {
    dependsOn(tasks.named("updateTodos"))
}
```

## Build

### Build and publish Conan package
To create and install the package in the local cache, run the following command in the `cpp/` directory:
```bash
conan create . @<user>/<channel> -pr:h default -pr:b default
```
To store the package to your remote, perform conan upload:
```bash
conan upload . todogen/<VERSION>@<user>/<channel> -r <REMOTE> --all --confirm
```

### Build and publish Gradle plugin
To create the Gradle plugin in the local Maven cache, run the following command in the `java/` directory:
```bash
gradle create
```
To release the stable package to the Maven, run the following command:
```bash
gradle publish
```
To feed maven credentials or change default package group, modify _gradle.properties_ file.
