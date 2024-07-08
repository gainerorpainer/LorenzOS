"""Builds html into static content"""
from glob import glob
from pathlib import Path
from os.path import exists
from io import TextIOWrapper

BINDATA_BLOCKSIZE = 32


def _build_preamble(file: TextIOWrapper):
    file.write("#pragma once\n\n\n#include <Arduino.h>\n\n")


def _build_favicon(html_folder: str, file: TextIOWrapper):
    with open(f"{html_folder}\\favicon.ico", "rb") as f:
        binary_content = f.read()

    file.write(
        "static const byte STATIC_HTML_FAVICON_CONTENT[] ICACHE_RODATA_ATTR = { \\\n")
    for block in [binary_content[i:i + BINDATA_BLOCKSIZE] for i in range(0, len(binary_content), BINDATA_BLOCKSIZE)]:
        file.write(
            "\t" + ", ".join(map(lambda b: "0x%02x" % b, block)) + ", \\\n")
    file.write("};\n")


def _build_html(html_filepath: str, file: TextIOWrapper):
    with open(html_filepath, "r", encoding="utf8") as f:
        filecontent = f.readlines()
    name = Path(html_filepath).stem.upper()
    file.write(f"static const char STATIC_HTML_{name}[] ICACHE_RODATA_ATTR =\n")
    for line in filecontent:
        # strip trailing \n, escape quotes
        line = line[:-1].replace('"', '\\"')
        # insert a c-style newline
        file.write('"' + line + '\\r\\n"\n')
    file.write(";\n")


def build_html(html_folder: str, include_folder: str):
    """Builds all encountered html files
    """
    with open(f"{include_folder}\\codegen_html.h", "w+", encoding="utf8") as f:
        _build_preamble(f)

        if exists(f"{html_folder}\\favicon.ico"):
            _build_favicon(html_folder, f)
            f.write("\n")
            print("Built \"favicon.ico\"")

        for html_filepath in glob(f"{html_folder}\\*.html"):
            _build_html(html_filepath, f)
            f.write("\n")
            print(f"Built \"{html_filepath}\"")
