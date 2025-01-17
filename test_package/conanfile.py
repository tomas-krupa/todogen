from conans import ConanFile, CMake, tools
from os import path


class TestPackageConan(ConanFile):
    generators = "CMakeDeps", "CMakeToolchain"
    settings = "os", "arch", "compiler", "build_type"

    def build_requirements(self):
        self.tool_requires(self.tested_reference_str)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        with open(path.join(self.build_folder, "README.md"), "r") as readme_file:
            print(readme_file.read())
