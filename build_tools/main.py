"""Entry point to build all"""
from sys import argv
from task_builder import TaskBuilder
from http_server_builder import HttpServerBuilder
from serializable_builder import SerializableBuilder
from html_builder import build_html

if argv[1] == "--debug-codegen":
    project_dir = argv[2]
    include_dir = project_dir + "\\include"
    src_dir = project_dir + "\\src"
else:
    Import("env")
    project_dir = env["PROJECT_DIR"]
    include_dir = env["PROJECT_INCLUDE_DIR"]
    src_dir = env["PROJECT_SRC_DIR"]

print("Building \"tasks\"...")
TaskBuilder(include_dir, src_dir).build()
print()

print("Building \"http_server\"...")
HttpServerBuilder(project_dir, include_dir, src_dir).build()
print()

print("Building \"serializable\"...")
SerializableBuilder(include_dir, src_dir).build()
print()

print("Building \"html\"...")
build_html(project_dir, include_dir)
print()
