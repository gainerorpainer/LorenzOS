"""Entry point to build all"""
import os

from task_builder import TaskBuilder
from http_server_builder import HttpServerBuilder
from html_builder import build_html

Import("env")
include_folder = env["PROJECT_INCLUDE_DIR"]
html_folder = env["PROJECT_DIR"]

print("Building \"tasks\"...")
TaskBuilder(include_folder).build()
print()

print("Building \"http_server\"...")
HttpServerBuilder(include_folder).build()
print()

print("Building \"html\"...")
build_html(html_folder, include_folder)
print()
