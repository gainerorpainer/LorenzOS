"""Entry point to build all"""
from sys import argv
from task_builder import TaskBuilder
from http_server_builder import HttpServerBuilder
from serializable_builder import SerializableBuilder
from html_builder import build_html

if argv[1] == "--debug-codegen":
    html_folder = argv[2]
    include_folder = argv[3]
else:
    Import("env")
    include_folder = env["PROJECT_INCLUDE_DIR"]
    html_folder = env["PROJECT_DIR"]

print("Building \"tasks\"...")
TaskBuilder(include_folder).build()
print()

print("Building \"http_server\"...")
HttpServerBuilder(include_folder).build()
print()

print("Building \"serializable\"...")
SerializableBuilder(include_folder).build()
print()

print("Building \"html\"...")
build_html(html_folder, include_folder)
print()
