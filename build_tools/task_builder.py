"""Implements a builder for tasks"""
from dataclasses import dataclass

from abstract_builder import AbstractBuilder


@dataclass
class _TaskDefinition:
    qualified_name: str
    interval: int


class TaskBuilder(AbstractBuilder):
    """Builder class for tasks
    """
    def __init__(self, include_folder: str):
        super().__init__("tasks", include_folder)
        functions = self._crawl_folder("task_with_interval")
        self.tasks = [_TaskDefinition(function.qualified_name, int(function.attribute_arg)) for function in functions]
        for task in self.tasks:
            print(f"Found task: {task}")
        # find containing set of header files
        self.header_files = set(
            (function.header_file_name for function in functions))

    def _generate_block(self, blockname: str) -> list[str]:
        match blockname.lower():
            case "fcalls":
                return [f"{task.qualified_name}();" for task in self.tasks]
            case "includes":
                return [f"#include \"{headerfile}\"" for headerfile in self.header_files]
