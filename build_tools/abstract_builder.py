"""Base class for all builders"""
import re
from glob import glob
from itertools import repeat
from dataclasses import dataclass
from pathlib import Path


@dataclass
class _AttributedFunction:
    header_file_name: str
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
    FUNCTION_RE = re.compile(
        r"(?:\w+)\s+(\w+)\(\)\s+__attribute__\(\((\w+)\(((?:[\w]+)|(?:\".*\"))\)\)\);")
    ATTR_FUNCTION_RE = re.compile(
        r"\[\[(\w+)(?:\(((?:[\w]+)|(?:\".*\"))\))?\]\]\s+(?:\w+)\s+(\w+)\(\);")

    def __init__(self, context: str, include_folder: str):
        self.context = context
        self.include_folder = include_folder

    def _generate_block(self, blockname: str) -> list[str]:
        raise NotImplementedError("Abstract function")

    def build(self):
        """Writes to the codegen_*.h files
        """
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

    def _crawl_folder(self, attribute_name: str) -> list[_AttributedFunction]:
        functions = []  # type: list[_AttributedFunction]
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

            # find all functions
            for function_match in AbstractBuilder.ATTR_FUNCTION_RE.finditer(content):
                if function_match[1] != attribute_name:
                    continue
                span = function_match.span()
                containing_namespace = next(
                    (namespace for namespace in namespaces if span[0] >= namespace.start and span[1] <= namespace.end), None)
                qualifiers = [
                    containing_namespace.qualified_name if containing_namespace else ""] + [function_match[3]]
                function = _AttributedFunction(
                    Path(file_path).name, function_match[3], "::".join(qualifiers), function_match[2])
                functions.append(function)
        return functions
