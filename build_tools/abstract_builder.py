"""Base class for all builders"""
import re
from glob import glob
from itertools import repeat
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


@dataclass
class _AttributedClass:
    header_file_name: str
    occurence_span: tuple[int, int]
    attribute_arg: str
    name: str
    qualified_name: str


@dataclass
class _AttributedFunction:
    header_file_name: str
    occurence_span: tuple[int, int]
    attribute_arg: str
    name: str
    qualified_name: str
    return_type: str
    arguments: str


@dataclass
class _Namespace:
    qualified_name: str
    start: int
    end: int


@dataclass
class _SearchResult:
    filename: str
    match: re.Match[str]
    namespaces: list[_Namespace]


class AbstractBuilder:
    """Base class for all builders"""
    CODEGENERATED_RE = re.compile(r"\/\* _CODEGENERATED_(.*?) (?:(.*) )?\*\/")
    NAMESPACE_RE = re.compile(r"namespace (.*?)\s*\{((?:.*\n.*)+)\}")
    _ATTRIBUTE_RE = r"\[\[(\w+)(?:\(((?:[\w]+)|(?:\".*\"))\))?\]\]"
    ATTR_FUNCTION_RE = re.compile(
        r"\[\[(\w+)(?:\(((?:[\w]+)|(?:\".*\"))\))?\]\]\s+(\w+)\s+(\w+)\((.*)\);")
    ATTR_CLASS_RE = re.compile(
        r"(?:struct|class)\s+" + _ATTRIBUTE_RE + r"\s+(.*)\s+{(?:.|\n)*}")

    def __init__(self, context: str, include_folder: str):
        self.context = context
        self.include_folder = include_folder
        self.do_not_build = False

    def _generate_block(self, blockname: str, indentation: str) -> list[str]:
        raise NotImplementedError("Abstract function")

    def build(self):
        """Builds a codegen_*.h file into a single file
        """
        if self.do_not_build:
            print("Nothing to build, skipping")
            return

        out_header_filepath = f"{self.include_folder}\\codegen_{self.context}.h"
        with open(f"codegen_{self.context}.h", "r", encoding="utf8") as templatefile, open(out_header_filepath, "w+", encoding="utf8") as sourcefile:
            sourcefile.writelines(AbstractBuilder._build_template(
                templatefile.readlines(), self._generate_block))
        print(f"Built header file: {out_header_filepath}")

    def __search_objects(self, regex: re.Pattern[str]) -> list[_SearchResult]:
        result = []  # type: list[_SearchResult]
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
                result.append(_SearchResult(Path(file_path).name, obj_match, namespaces))
        return result

    def _search_functions(self, attribute_name: str) -> list[_AttributedFunction]:
        found_objects = self.__search_objects(AbstractBuilder.ATTR_FUNCTION_RE)
        # find all objects
        objects = []  # type: list[_AttributedFunction]
        for obj in found_objects:
            if obj.match[1] != attribute_name:
                continue
            span = obj.match.span()
            containing_namespace = next(
                (namespace for namespace in obj.namespaces if span[0] >= namespace.start and span[1] <= namespace.end), None)
            qualifiers = [
                containing_namespace.qualified_name if containing_namespace else ""] + [obj.match[4]]
            obj = _AttributedFunction(obj.filename, span, obj.match[2], obj.match[4], "::".join(
                qualifiers), obj.match[3], obj.match[5])
            objects.append(obj)
        return objects

    def _search_classes(self, attribute_name: str) -> list[_AttributedClass]:
        found_objects = self.__search_objects(AbstractBuilder.ATTR_CLASS_RE)
        # find all objects
        objects = []  # type: list[_AttributedClass]
        for obj in found_objects:
            if obj.match[1] != attribute_name:
                continue
            span = obj.match.span()
            containing_namespace = next(
                (namespace for namespace in obj.namespaces if span[0] >= namespace.start and span[1] <= namespace.end), None)
            qualifiers = [
                containing_namespace.qualified_name if containing_namespace else ""] + [obj.match[3]]
            obj = _AttributedClass(obj.filename, span, obj.match[2], obj.match[3], "::".join(qualifiers))
            objects.append(obj)
        return objects

    @staticmethod
    def _build_template(template: list[str], block_resolver: Callable[[str, int], list[str]]) -> list[str]:
        out_buffer = []  # type: list[str]
        placeholder_active = False
        for line in template:
            match = AbstractBuilder.CODEGENERATED_RE.search(line)
            if match:
                blockname = match[1].lower()

                # placeholder handling
                if blockname == "placeholder":
                    placeholder_active = match[2] == "BEGIN"
                    continue

                span = match.span()
                indentation = "".join(repeat(" ", span[0]))
                block_lines = block_resolver(blockname, indentation)
                if block_lines is None:
                    raise NotImplementedError(
                        f"{repr(block_resolver)} does not resolve the blockname \"{blockname}\"")
                if len(block_lines) == 0:
                    continue
                if len(block_lines) == 1:
                    line = line[0:span[0]] + block_lines[0] + line[span[1]:]
                else:
                    line = indentation + \
                        f"\n{indentation}".join(block_lines) + "\n"

            if placeholder_active:
                continue

            out_buffer.append(line)

        return out_buffer
