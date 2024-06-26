"""Builds html into static content"""
from glob import glob
from pathlib import Path


def _build_html(html_path: str, include_folder: str):
    with open(html_path, "r", encoding="utf8") as f:
        filecontent = f.readlines()

    friendly_name = Path(html_path).stem

    with open(f"{include_folder}\\static_html_{friendly_name}.h", "w+", encoding="utf8") as f:
        f.write("#pragma once\n\n\n#include <Arduino.h>\n\n")
        f.write(
            f"static const char STATIC_HTML_{friendly_name.upper()}[] ICACHE_RODATA_ATTR =\n")
        for line in filecontent:
            # strip trailing \n, escape quotes
            line = line[:-1].replace('"', '\\"')
            # insert a c-style newline
            f.write('"' + line + '\\r\\n"\n')
        f.write(";\n")


def _build_favicon(html_folder: str, include_folder: str):
    with open(f"{html_folder}\\favicon.ico", "rb") as f:
        binary_content = f.read()

    with open(f"{include_folder}\\static_html_favicon.h", "w+", encoding="utf8") as f:
        f.write("#pragma once\n\n#include <Arduino.h>\n\n")
        f.write(
            "static const byte STATIC_HTML_FAVICON_CONTENT[] ICACHE_RODATA_ATTR = { \\\n")
        blocksize = 32
        for block in [binary_content[i:i + blocksize] for i in range(0, len(binary_content), blocksize)]:
            f.write("\t" + ", ".join(map(lambda b: "0x%02x" % b, block)) + ", \\\n")
        f.write("};\n")


def build_html(html_folder: str, include_folder: str):
    """Builds all encountered html files
    """
    _build_favicon(html_folder, include_folder)
    print("Built \"favicon.ico\"")

    for html_filepath in glob(f"{html_folder}\\*.html"):
        _build_html(html_filepath, include_folder)
        print(f"Built \"{html_filepath}\"")
