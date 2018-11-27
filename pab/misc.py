#!/usr/bin/env python
# coding=utf-8

import os


def pjoin(*args, **kwargs):
    """ wraper for path join """
    return os.path.join(*args, **kwargs)


def parse_kv_file(filename):
    record = {}
    f = open(filename)

    # parse each line in file
    for line in f:
        # trim the leading and trialing white space
        line = line.strip()

        # filter out blank and comment line
        if not line or line.startswith('#'):
            continue

        key, value = line.split('=', 1)
        record[key] = value

    # close the file
    f.close()
    return record
