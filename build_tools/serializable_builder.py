"""Implements a builder for tasks"""
import re
from dataclasses import dataclass
from abstract_builder import OneToOneBuilder, _AttributedCodeObject


@dataclass
class _SerializableClass:
    name: str
    fields: list[str]


class SerializableBuilder(OneToOneBuilder):
    """Builder class for serializable"""

    STRUCT_FIELD_RE = re.compile(
        r"(\w+)\s+(\w+)(?:\[\w*\])?(?:\s*=\s*.*)?(?:\s*{.*})?;")

    def __init__(self, include_folder: str):
        super().__init__("parameters", include_folder)
        classes = self._search_classes("is_parameter_class")
        # find containing set of header files
        self.header_files = set(
            (_class.header_file_name for _class in classes))
        self.classes = {} # type: dict[_AttributedCodeObject, _SerializableClass]
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
            self.classes[_class] = _SerializableClass(_class.name, fields)

    def _generate_block_for(self, obj: _AttributedCodeObject, blockname: str) -> list[str]:
        match blockname.lower():
            case "include":
                return [f'#include "{obj.header_file_name}"']
            case "ns":
                return [obj.name]
            case "write":
                return [f'doc["{field}"] = in.{field};' for field in self.classes[obj].fields]
            case "read":
                fields = self.classes[obj].fields
                temporaries = [
                    f'JsonVariant {field} = doc["{field}"];' for field in fields
                ]
                null_check = [
                    "if ("
                    + " || ".join([f"{field}.isNull()" for field in fields])
                    + ")",
                    "\treturn false;"
                ]
                writes = [f"out.{field} = {field};" for field in fields]
                return temporaries + [""] + null_check + [""] + writes
