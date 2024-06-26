"""Base class for all builders"""
import re
from glob import glob
from itertools import repeat
from dataclasses import dataclass
from pathlib import Path


@dataclass
class _AttributedCodeObject:
    header_file_name: str
    occurence_span: tuple[int, int]
    name: str
    qualified_name: str
    attribute_arg: str


@dataclass
class _Namespace:
    qualified_name: str
    start: int
    end: int


class AbstractBuilder:
    """Base class for all builders"""
    CODEGENERATED_RE = re.compile(r"\/\* _CODEGENERATED_(.*?) \*\/")
    NAMESPACE_RE = re.compile(r"namespace (.*?)\s*\{((?:.*\n.*)+)\}")
    _ATTRIBUTE_RE = r"\[\[(\w+)(?:\(((?:[\w]+)|(?:\".*\"))\))?\]\]"
    ATTR_FUNCTION_RE = re.compile(
        r"\[\[(\w+)(?:\(((?:[\w]+)|(?:\".*\"))\))?\]\]\s+(?:\w+)\s+(\w+)\(\);")
    ATTR_CLASS_RE = re.compile(
        r"(?:struct|class)\s+" + _ATTRIBUTE_RE + r"\s+(.*)\s+{(?:.|\n)*}")

    def __init__(self, context: str, include_folder: str):
        self.context = context
        self.include_folder = include_folder
        self.do_not_build = False

    def _generate_block(self, blockname: str) -> list[str]:
        raise NotImplementedError("Abstract function")

    def build(self):
        """Writes to the codegen_*.h files
        """
        if self.do_not_build:
            print("Nothing to build, skipping")
            return

        out_header_filepath = f"{self.include_folder}/codegen_{self.context}.h"
        with open(f"codegen_{self.context}.h", "r", encoding="utf8") as templatefile, open(out_header_filepath, "w+", encoding="utf8") as sourcefile:
            template = templatefile.readlines()
            for line in template:
                match = AbstractBuilder.CODEGENERATED_RE.search(line)
                if match:
                    blockname = match[1]
                    span = match.span()
                    indentation = span[0]
                    block_lines = self._generate_block(blockname)
                    block_formatted = (
                        "\n" + "".join(repeat(" ", indentation))).join(block_lines)
                    line = line[0:span[0]] + \
                        block_formatted + line[span[1]:]
                sourcefile.write(line)
        print(f"Built header file: {out_header_filepath}")

    def __search_objects(self, attribute_name: str, regex: re.Pattern[str]) -> list[_AttributedCodeObject]:
        objects = []  # type: list[_AttributedCodeObject]
        for file_path in glob(f"{self.include_folder}\\*.h"):
            with open(file_path, "r", encoding="utf8") as f:
                content = f.read()

            # find all namespaces
            namespaces = []  # type: list[_Namespace]
            nodes_in_tree = list(zip(
                repeat([""]), repeat(0), AbstractBuilder.NAMESPACE_RE.finditer(content)))
            while len(nodes_in_tree) > 0:
                [parent_qualifiers, offset, node] = nodes_in_tree.pop(0)
                qualifiers = parent_qualifiers + [node[1]]
                name = "::".join(qualifiers)
                span = node.span()
                namespaces.append(
                    _Namespace(name, offset + span[0], offset + span[1]))
                # recursion
                nodes_in_tree.extend(
                    zip(repeat(qualifiers), repeat(node.regs[2][0]), AbstractBuilder.NAMESPACE_RE.finditer(node[2])))
            # shorter namespaces are more specific and should come first
            namespaces = sorted(namespaces, key=lambda x: x.end - x.start)

            # find all objects
            for obj_match in regex.finditer(content):
                if obj_match[1] != attribute_name:
                    continue
                span = obj_match.span()
                containing_namespace = next(
                    (namespace for namespace in namespaces if span[0] >= namespace.start and span[1] <= namespace.end), None)
                qualifiers = [
                    containing_namespace.qualified_name if containing_namespace else ""] + [obj_match[3]]
                obj = _AttributedCodeObject(
                    Path(file_path).name, span, obj_match[3], "::".join(qualifiers), obj_match[2])
                objects.append(obj)
        return objects

    def _search_functions(self, attribute_name: str):
        return self.__search_objects(attribute_name, AbstractBuilder.ATTR_FUNCTION_RE)

    def _search_classes(self, attribute_name: str):
        return self.__search_objects(attribute_name, AbstractBuilder.ATTR_CLASS_RE)
