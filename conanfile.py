from conans import ConanFile, CMake, tools
from os import path


class ToDoGenConan(ConanFile):
    name = "todogen"
    license = "S&B Licence"
    settings = {}
    description = "ToDo Generator"
    author = "Scheidt & Bachmann GmbH"
    homepage = "www.scheidt-bachmann.de"
    url = "https://git.ads.local/krupa.tomas/todogen"
    exports_sources = "todogen*"

    def set_version(self):
        self.version = tools.Git().run("describe --tags --abbrev=0")

    def build(self):
        pass

    def package(self):
        self.copy("todogen*", dst=".")

    def package_info(self):
        self.env_info.PYTHONPATH.append(self.package_folder)
        self.cpp_info.set_property(
            "cmake_build_modules", [path.join(self.package_folder, "todogen.cmake")]
        )
        self.cpp_info.build_modules["cmake"].append(
            path.join(self.package_folder, "todogen-config.cmake")
        )
        self.cpp_info.builddirs.append(path.join(self.package_folder))

    def package_id(self):
        self.info.clear()
