"""Implements a builder for tasks"""
from dataclasses import dataclass

from abstract_builder import AbstractBuilder


@dataclass
class _TaskDefinition:
    name: str
    qualified_name: str
    interval: int


class TaskBuilder(AbstractBuilder):
    """Builder class for tasks
    """

    def __init__(self, include_folder: str, source_folder: str):
        super().__init__("tasks", include_folder, source_folder)
        functions = self._search_functions("task_with_interval")
        self.tasks = [_TaskDefinition(function.name, function.qualified_name, int(
            function.attribute_arg)) for function in functions]
        for task in self.tasks:
            print(f"Found task: {task}")
        # find containing set of header files
        self.header_files = set(
            (function.header_file_name for function in functions))

    def _generate_block(self, blockname: str, _: str) -> list[str]:
        match blockname:
            case "fcalls":
                lines = []  # type: list[str]
                for task in self.tasks:
                    lines.extend([f"static CycleLimit::CycleLimit {task.name}_cl_limit" + "{" + str(task.interval) +"};",
                                  f"if ({task.name}_cl_limit.IsCycleCooledDown())",
                                  f"\t{task.qualified_name}();"])
                return lines
            case "includes":
                return [f"#include \"{headerfile}\"" for headerfile in self.header_files]
