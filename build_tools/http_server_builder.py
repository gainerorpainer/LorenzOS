"""Builds http server"""
from dataclasses import dataclass
import re

from abstract_builder import AbstractBuilder


@dataclass
class _CbDefinition:
    qualified_name: str
    ressource_str: str


class HttpServerBuilder(AbstractBuilder):
    """Http server builder"""
    VERSION_RE = re.compile(r"VERSION\s+=\s+(.*)")
    BUILDNUMBER_RE = re.compile(r"constexpr int BUILD_NUMBER = int{(\d+)};")

    def __init__(self, project_folder: str, include_folder: str, source_folder: str):
        super().__init__("http_server", include_folder, source_folder)
        functions = self._search_functions("http_server_bind_to")
        self.callbacks = [_CbDefinition(
            function.qualified_name, function.attribute_arg) for function in functions]
        for callback in self.callbacks:
            print(f"Found server callback: {callback}")
        # find containing set of header files
        self.header_files = set(
            (function.header_file_name for function in functions))
        # try to reuse and increment build number
        with open(f"{project_folder}\\platformio.ini", "r", encoding="utf8") as f:
            content = f.read()
        self.version = HttpServerBuilder.VERSION_RE.search(content)[1]
        with open(f"{include_folder}\\codegen_http_server.h", "r", encoding="utf8") as f:
            content = f.read()
        if match := HttpServerBuilder.BUILDNUMBER_RE.search(content):
            self.build_number = int(match[1]) + 1
        else:
            self.build_number = 0

    def _generate_block(self, blockname: str, _: str) -> list[str]:
        match blockname:
            case "register":
                return [f"LOS::_HttpServer.on({cb.ressource_str}, {cb.qualified_name});" for cb in self.callbacks]
            case "includes":
                return [f"#include \"{headerfile}\"" for headerfile in self.header_files]
            case "buildnumber":
                return [str(self.build_number)]
            case "versionstr":
                return [f"\"{self.version}_{self.build_number}\""]