"""Implements a builder for tasks"""

import re

from abstract_builder import AbstractBuilder


class ParametersBuilder(AbstractBuilder):
    """Builder class for parameters"""

    STRUCT_FIELD_RE = re.compile(r"(\w+)\s+(\w+)(?:\s*=\s*.*)?(?:\s*{.*})?;")

    def __init__(self, include_folder: str):
        super().__init__("parameters", include_folder)
        classes = self._search_classes("is_parameter_class")
        # find containing set of header files
        self.header_files = set(
            (_class.header_file_name for _class in classes))
        self.fields = []  # type: list[str]
        if len(classes) > 1:
            raise OverflowError("Too many attributed classes:" + repr(classes))
        if len(classes) == 0:
            print("No paramters class found")
            self.do_not_build = True
            return

        _class = classes[0]
        print(f"Found class: {_class}")
        # parse class content to find fields
        with open(
            f"{include_folder}\\{_class.header_file_name}", "r", encoding="utf8"
        ) as f:
            content = f.read()
            # trim to known occurence
            content = content[_class.occurence_span[0]: _class.occurence_span[1]]
        for field_match in ParametersBuilder.STRUCT_FIELD_RE.finditer(content):
            self.fields.append(field_match[2])

    def _generate_block(self, blockname: str) -> list[str]:
        if self.fields is None:
            return []
        match blockname.lower():
            case "includes":
                return [f'#include "{headerfile}"' for headerfile in self.header_files]
            case "write":
                return [f'doc["{field}"] = in.{field};' for field in self.fields]
            case "read":
                temporaries = [
                    f'JsonVariant {field} = doc["{field}"];' for field in self.fields
                ]
                null_check = [
                    "if ("
                    + " || ".join([f"{field}.isNull()" for field in self.fields])
                    + ")",
                    "\treturn false;"
                ]
                writes = [f"out.{field} = {field};" for field in self.fields]
                return temporaries + [""] + null_check + [""] + writes
