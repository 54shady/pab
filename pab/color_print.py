#!/usr/bin/env python
# coding=utf-8

import tcolor
import sys


class ColorPrint():
    def __init__(self, use_color=False):
        self.WARN_COLOR = self.SUCC_COLOR = self.RESET_COLOR = ""
        if use_color:
            self.WARN_COLOR = tcolor.pick_color(fg=tcolor.RED)
            self.SUCC_COLOR = tcolor.pick_color(fg=tcolor.GREEN)
            self.RESET_COLOR = tcolor.pick_color(reset=True)

    def color_print_normal(self, message):
        sys.stdout.write(message)

    def color_print_success(self, message):
        self.color_print_normal('%s%s%s\n' %
                         (self.SUCC_COLOR, message, self.RESET_COLOR))

    def color_print_warn(self, message):
        self.color_print_normal('%s%s%s\n' %
                         (self.WARN_COLOR, message, self.RESET_COLOR))
