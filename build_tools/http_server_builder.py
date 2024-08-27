"""Builds http server"""
from dataclasses import dataclass
from datetime import datetime
import re

from abstract_builder import AbstractBuilder


@dataclass
class _CbDefinition:
    qualified_name: str
    ressource_str: str


class HttpServerBuilder(AbstractBuilder):
    """Http server builder"""
    VERSION_RE = re.compile(r"VERSION\s+=\s+(.*)")

    @staticmethod
    def __get_build_date() -> str:
        return datetime.now().strftime('%Y_%m_%d')

    def __init__(self, project_folder: str, include_folder: str, source_folder: str):
        super().__init__("http_server", include_folder, source_folder)
        # find and parse callbacks
        functions = self._search_functions("http_server_bind_to")
        self.callbacks = [_CbDefinition(
            function.qualified_name, function.attribute_arg) for function in functions]
        for callback in self.callbacks:
            print(f"Found server callback: {callback}")
        # find containing set of header files
        self.header_files = set(
            (function.header_file_name for function in functions))
        # parse version from projects .ini file
        with open(f"{project_folder}\\platformio.ini", "r", encoding="utf8") as f:
            content = f.read()
        self.version = HttpServerBuilder.VERSION_RE.search(content)[1]

    def _generate_block(self, blockname: str, _: str) -> list[str]:
        match blockname:
            case "includes":
                return [f"#include \"{headerfile}\"" for headerfile in self.header_files]
            case "versionstr":
                return [f"\"{self.version}-{HttpServerBuilder.__get_build_date()}\""]
            case "callbacks":
                return [f"LOS::_HttpServer.on({cb.ressource_str}, {cb.qualified_name});" for cb in self.callbacks]
