"""Entry point to build all"""
from sys import argv
from task_builder import TaskBuilder
from http_server_builder import HttpServerBuilder
from serializable_builder import SerializableBuilder
from html_builder import build_html

if argv[1] == "--debug-codegen":
    html_dir = argv[2]
    include_dir = html_dir + "\\include"
    src_dir = html_dir + "\\src"
else:
    Import("env")
    include_dir = env["PROJECT_INCLUDE_DIR"]
    src_dir = env["PROJECT_SRC_DIR"]
    html_dir = env["PROJECT_DIR"]

print("Building \"tasks\"...")
TaskBuilder(include_dir, src_dir).build()
print()

print("Building \"http_server\"...")
HttpServerBuilder(include_dir, src_dir).build()
print()

print("Building \"serializable\"...")
SerializableBuilder(include_dir, src_dir).build()
print()

print("Building \"html\"...")
build_html(html_dir, include_dir)
print()
