#!/usr/bin/env python
# coding=utf-8


def get_config_file(filename):
    # config file path
    conf_dir = "pabuild/"

    # alias name
    k = ["pabrc", "bt", "dtbs", "prevcp", "postcp", "vendor"]

    # real file name
    f_list = ["pabrc", "build_target",
              "dtbs", "prevcopy.txt",
              "postcopy.txt", "vendor.txt"
              ]

    v = []
    for f in f_list:
        v.append(conf_dir + f)

    d = dict(zip(k, v))

    if d.has_key(filename):
        return d[filename]
    else:
        print "Available file are %s" % d.keys()
