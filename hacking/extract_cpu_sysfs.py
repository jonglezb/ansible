#!/usr/bin/env python

from __future__ import print_function, division, unicode_literals

from collections import defaultdict
from functools import reduce
import json
import os
import sys

SYSFS_ROOT = "/sys/devices/system/cpu"

def directory_to_dict(rootdir):
    """Returns the whole content of a directory into a nested dict-like object
    representing the directory hierarchy, with the final level storing the
    content of the files as strings.  Directory symlinks are ignored.

    Note: this assumes that the content of all files is decodable as UTF-8
    """
    # Recursive defaultdict
    nested_dict = lambda: defaultdict(nested_dict)
    data = nested_dict()
    for abs_dirname, dirs, files in os.walk(rootdir):
        # Remove prefix
        dirname = abs_dirname[len(rootdir) + 1:]
        if len(dirname) == 0:
            inner_dict = data
        else:
            # Create structure and get last component
            components = dirname.split("/")
            inner_dict = reduce(lambda x, y: x[y], components, data)
        for filename in files:
            abs_filename = os.path.join(abs_dirname, filename)
            try:
                content = open(abs_filename, "r").read()
            except (OSError, IOError):
                content = ""
            inner_dict[filename] = content
    return data


if __name__ == '__main__':
    d = directory_to_dict(SYSFS_ROOT)
    print(json.dumps(d))
