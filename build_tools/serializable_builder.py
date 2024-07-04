"""Implements a builder for tasks"""
import re
from dataclasses import dataclass
from abstract_builder import AbstractBuilder


@dataclass
class _SerializableClass:
    name: str
    qualified_name: str
    fields: list[str]


class SerializableBuilder(AbstractBuilder):
    """Builder class for serializable"""

    STRUCT_FIELD_RE = re.compile(
        r"(\w+)\s+(\w+)(?:\[\w*\])?(?:\s*=\s*.*)?(?:\s*{.*})?;")

    def __init__(self, include_folder: str):
        super().__init__("serializable", include_folder)
        classes = self._search_classes("is_serializable_class")
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
            self.classes.append(_SerializableClass(_class.name, _class.qualified_name, fields))

    def _generate_block(self, blockname: str, indentation: str) -> list[str]:
        match blockname.lower():
            case "includes":
                return [f"#include \"{headerfile}\"" for headerfile in self.header_files]
            case "fragments":
                template = [] # type: list[str]
                with open("_fragment_serializable.h", "r", encoding="utf8") as f:
                    for line in f.readlines():
                        # remove trailing newline (last line is different)
                        if line[-1] == "\n":
                            line = line[:-1]
                        template.append(line)
                block = []  # type: list[str]
                for _class in self.classes:
                    block.extend(AbstractBuilder._build_template(
                        template, lambda x,y : SerializableBuilder.__generate_block_for(_class, x, indentation)))
                    block.append("")
                return block

    @staticmethod
    def __generate_block_for(_class: _SerializableClass, blockname: str, indentation: str) -> list[str]:
        match blockname:
            case "type":
                return [_class.name]
            case "qualified_type":
                return [_class.qualified_name]
            case "write":
                lines = [f'{indentation}doc["{field}"] = in.{field};' for field in _class.fields]
                # remove indentation from first item
                lines[0] = lines[0][len(indentation):]
                return lines
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
                writes = [f"{indentation}out.{field} = {field};" for field in fields]
                lines = temporaries + [""] + null_check + [""] + writes
                # remove indentation from first item
                lines[0] = lines[0][len(indentation):]
                return lines
