"""Builds http server"""
from dataclasses import dataclass

from abstract_builder import AbstractBuilder


@dataclass
class _CbDefinition:
    qualified_name: str
    ressource_str: str


class HttpServerBuilder(AbstractBuilder):
    """Http server builder"""
    def __init__(self, include_folder: str, source_folder: str):
        super().__init__("http_server", include_folder, source_folder)
        functions = self._search_functions("http_server_bind_to")
        self.callbacks = [_CbDefinition(function.qualified_name, function.attribute_arg) for function in functions]
        for callback in self.callbacks:
            print(f"Found server callback: {callback}")
        # find containing set of header files
        self.header_files = set(
            (function.header_file_name for function in functions))

    def _generate_block(self, blockname: str, _: str) -> list[str]:
        match blockname:
            case "register":
                return [f"LOS::_HttpServer.on({cb.ressource_str}, {cb.qualified_name});" for cb in self.callbacks]
            case "includes":
                return [f"#include \"{headerfile}\"" for headerfile in self.header_files]
