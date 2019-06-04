#!/usr/bin/env python
# coding=utf-8

import os
from misc import pjoin
from misc import parse_kv_file
from config_file import get_config_file


class BuildEnv():
    def __init__(self):
        self.__android_top = os.path.abspath(os.getcwd())
        self.__otp = "out"
        self.__android_out = pjoin(self.__android_top, self.__otp)
        self.__armgcc = "prebuilts/gcc/linux-x86/aarch64/gcc-linaro-6.3.1-2017.05-x86_64_aarch64-linux-gnu/bin/aarch64-linux-gnu-"
        self.__cross_compile = pjoin(self.__android_top, self.__armgcc)
        self.__build_target = get_config_file("bt")
        build_target = parse_kv_file(self.__build_target)
        self.envd = {
            "android_top": self.__android_top,
            "otp": self.__otp,
            "armgcc": self.__armgcc,
            "android_out": self.__android_out,
            "uboot_out": pjoin(self.__android_out, "UBOOT"),
            "kernel_out": pjoin(self.__android_out, "KERNEL"),
            "cross_compile": self.__cross_compile,
            "uboot_src": pjoin(self.__android_top, "u-boot"),
            "kernel_src": pjoin(self.__android_top, "kernel"),
            "kernel_config_file": build_target.get("KERNEL_CONFIG_FILE"),
            "kernel_target_image": build_target.get("KERNEL_TARGET_IMAGE"),
            "uboot_config": build_target.get("UBOOT_CONFIG_FILE"),
        }
