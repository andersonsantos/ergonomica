#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

# imported from different file
# pylint: disable=import-error

"""
[lib/lib/ls.py]

Defines the "ls" command.
"""

import os
import re
import sys
import datetime
from lib.lang.stat import creation_date
from lib.lang.error import ErgonomicaError

verbs = {}

def ls(env, args, kwargs):
    """[DIR,...] {long:BOOL}@List files in a directory. If long, then will list last edit dates."""
    _long = False
    try:
        if kwargs["long"] in ["true", "t"]:
            _long = True
    except KeyError:
        pass

    # date processing from numerical time
    d = lambda t: str(datetime.datetime.fromtimestamp(creation_date(t))) + " " if _long else ""

    if len(args) > 1:
        out = [ls(env, [x], kwargs) for x in args]
        # flatten
        return [d(item) + item for sublist in out for item in sublist]

    try:
        if len(args) == 0:
            return [env.theme["files"] + d(x) + x for x in os.listdir(env.directory)]
        out = [args[0] + ":\n"]
        out += [env.theme["files"] + d(x) + x for x in os.listdir(args[0])]
        out += [""]
    except OSError:
        _, error, _ = sys.exc_info()
        bad_dir = re.findall(r"'(.*?)'", str(error))[0]
        raise ErgonomicaError("[ergo: NoSuchDirectoryError] No such directory '%s'." % (bad_dir))

verbs["ls"] = ls
verbs["list"] = ls
