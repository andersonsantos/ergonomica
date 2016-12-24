#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

# no other way to do it
# pylint: disable=line-too-long

# this file is imported from a different directory
# pylint: disable=import-error

# needed to make the import work
# pylint: disable=wrong-import-position

# positional arguments are a good standard for commands
# pylint: disable=unused-argument

"""
[lib/lib/edit.py]

Defines the "edit" command.
"""

import os
import sys
import subprocess
sys.path[0] = os.path.join(sys.path[0], "lib")
from lib.suplemon.cli import main
from lib.lang.error import ErgonomicaError

verbs = {}

def edit(env, args, kwargs):
    """[FILE,...]@Edit a file."""
    try:
        if env.EDITOR == "suplemon":
            main(args)
        subprocess.call([env.EDITOR] + args)
    except OSError:
        try:
            subprocess.call([env.EDITOR])
            raise ErgonomicaError("[ergo: EditorError]: Unable to edit one or more files passed to edit.")
        except OSError:
            raise ErgonomicaError("[ergo: EditorError]: No such editor '%s'." % (env.EDITOR))
    return

verbs["edit"] = edit
