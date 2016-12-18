#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lang/parser.py]

Lexer module. Contains tokenize().
"""

# pylint doesn't know that `from lib.verbs...` is run from the above dir
# pylint: disable=import-error

import re
import subprocess
from lib.lib import verbs

def tokenize(string):
    """Tokenize ergonomica commands."""
    
    # bash escaped
    try:
        bash_escaped = re.search("`(.+?)`", string).groups()

        for item in bash_escaped:
            string = string.replace("`" + item + "`", 'bash "' + item + '"')
    except AttributeError:
        pass

    # python escaped
    try:
        python_escaped = re.search("\\\\(.+?)\\\\", string).groups()

        for item in python_escaped:
            string = string.replace("\\" + item + "\\", 'python "' + item + '"')
    except AttributeError:
        pass

    tokens = [""]
    _special = False
    special = ""
    kwargs = []

    for char in string:
        if _special:
            if char in ["'", '"', "}"]:
                if _special == "{":
                    for item in special.split(","):
                        kwargs.append(item)
                elif _special in ['"', "'"]:
                    tokens.append(special)
                _special = False
            else:
                special += char
        else:
            if char == " ":
                tokens.append("")
            elif char in ["{", '"', "'"]:
                _special = char
                special = ""
            else:
                tokens[-1] += char
    # filter out empty strings
    return [[x for x in tokens if x], kwargs]

def expand_sub_expressions(block):
    temp_block = block
    # evaluate $(exp) & replace
    matches = re.findall(r"\$\((.*?)\)", temp_block)
    for match in matches:
        temp_block = temp_block.replace("$(%s)" % (match), "\n".join(ergo(match)))
    return temp_block
