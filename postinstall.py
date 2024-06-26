"""Installer script for LorenzOS"""
import shutil
from glob import glob

print("Installing LorenzOS...")

Import("env")
include_folder = env["PROJECT_INCLUDE_DIR"]

for template_file in glob("build_tools/codegen_*.h"):
    print(f"Copy file from {template_file} to {include_folder}")
    shutil.copy(template_file, include_folder)

print("Done installing LorenzOS!")
