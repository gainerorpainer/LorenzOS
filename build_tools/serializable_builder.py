"""Implements a builder for tasks"""
import re
from dataclasses import dataclass
from abstract_builder import _AttributedFunction, AbstractBuilder


@dataclass
class _SerializableClass:
    name: str
    qualified_name: str
    fields: list[str]
    is_parsable: bool
    qualified_extension_serialization: str = None
    qualified_extension_parsing: str = None


class SerializableBuilder(AbstractBuilder):
    """Builder class for serializable"""

    STRUCT_FIELD_RE = re.compile(
        r"(\w+)\s+(\w+)(?:\[\w*\])?(?:\s*=\s*.*)?(?:\s*{.*})?;")

    def __init__(self, include_folder: str):
        super().__init__("serializable", include_folder)
        classes = self._search_classes("is_serializable_class")
        serialization_functions = self._search_functions(
            "serialization_extension_for")
        parsing_functions = self._search_functions("parsing_extension_for")
        # find containing set of header files
        self.header_files = set(
            (_class.header_file_name for _class in classes))
        self.classes = []  # type: list[_SerializableClass]
        for _class in classes:
            print(f"Found class: {_class}")

            # parse class content to find fields
            with open(
                f"{include_folder}\\{_class.header_file_name}", "r", encoding="utf8"
            ) as f:
                content = f.read()
                # trim to known occurence
                content = content[_class.occurence_span[0]:_class.occurence_span[1]]
            fields = []  # type: list[str]
            for field_match in SerializableBuilder.STRUCT_FIELD_RE.finditer(content):
                fields.append(field_match[2])

            # try to find matching extension functions in same header file
            def __find_func(iterable: list[_AttributedFunction]) -> str | None:
                for item in iterable:
                    if item.header_file_name == _class.header_file_name and item.attribute_arg == f'"{_class.name}"':
                        print(f"Found extensions function: {item}")
                        return item.qualified_name
                return None
            serialization_ext_f = __find_func(serialization_functions)
            parsing_ext_f = __find_func(parsing_functions)
            self.classes.append(_SerializableClass(
                _class.name, _class.qualified_name, fields, _class.attribute_arg == "SERIALIZABLE_AND_PARSABLE", serialization_ext_f, parsing_ext_f))

    def _generate_block(self, blockname: str, indentation: str) -> list[str]:
        match blockname.lower():
            case "includes":
                return [f"#include \"{headerfile}\"" for headerfile in self.header_files]
            case "fragments":
                fragments = []  # type: list[list[str]]
                for file in ["_fragment_serialize.h", "_fragment_tryParse.h"]:
                    with open(file, "r", encoding="utf8") as f:
                        fragments.append(
                            SerializableBuilder._no_trailing_breaks(f.readlines()))
                block = []  # type: list[str]
                for i, _class in enumerate(self.classes):
                    if i > 0:
                        block.append("")
                    # skip tryParse fragment if not parsable
                    for fragment in fragments if _class.is_parsable else [fragments[0]]:
                        block_lines = AbstractBuilder._build_template(
                            fragment, lambda x, _: SerializableBuilder.__generate_block_for(_class, x, indentation))
                        # remove trailing newlines
                        block.extend(
                            SerializableBuilder._no_trailing_breaks(block_lines))
                return block

    @staticmethod
    def _no_trailing_breaks(lines: list[str]) -> list[str]:
        for i, line in enumerate(lines):
            if len(line) > 0 and line[-1] == "\n":
                lines[i] = line[:-1]
        return lines

    @staticmethod
    def __generate_block_for(_class: _SerializableClass, blockname: str, indentation: str) -> list[str]:
        match blockname:
            case "type":
                return [_class.name]
            case "qualified_type":
                return [_class.qualified_name]
            case "write":
                lines = [f'{indentation}doc["{field}"] = in.{
                    field};' for field in _class.fields]
                # remove indentation from first item
                lines[0] = lines[0][len(indentation):]
                return lines
            case "extension_write":
                return [] if _class.qualified_extension_serialization is None else [f"{_class.qualified_extension_serialization}(doc);"]
            case "read":
                fields = _class.fields
                temporaries = [
                    f'{indentation}JsonVariant {field} = doc["{field}"];' for field in fields
                ]
                null_check = [
                    f"{indentation}if ("
                    + " || ".join([f"{field}.isNull()" for field in fields])
                    + ")",
                    f"{indentation}\treturn false;"
                ]
                writes = [f"{indentation}out.{field} = {
                    field};" for field in fields]
                lines = temporaries + [""] + null_check + [""] + writes
                # remove indentation from first item
                lines[0] = lines[0][len(indentation):]
                return lines
            case "extension_read":
                return ["// not implemented"]
