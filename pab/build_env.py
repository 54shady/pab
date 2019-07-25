#!/usr/bin/env python
# coding=utf-8

import os
from misc import pjoin
from misc import parse_kv_file
from config_file import get_config_file


class BuildEnv():
    def __init__(self):
        # parse the global config file
        self.__buildconfig = get_config_file("pabrc")
        try:
            assert os.path.exists(self.__buildconfig)
        except AssertionError:
            print 'Error : Not on android source tree'
            os.sys.exit()

        prj_info = parse_kv_file(self.__buildconfig)

        self.__android_top = os.path.abspath(os.getcwd())
        self.__otp = "out"
        self.__android_out = pjoin(self.__android_top, self.__otp)

        # config CROSS_COMPILE=aarch64-linux-gnu-
        # or leave it empty will using the prebuiltsgcc
        prebuiltsgcc = "prebuilts/gcc/linux-x86/aarch64/gcc-linaro-6.3.1-2017.05-x86_64_aarch64-linux-gnu/bin/aarch64-linux-gnu-"
        self.__armgcc = prj_info['CROSS_COMPILE'] if prj_info['CROSS_COMPILE'] else prebuiltsgcc
        self.__cross_compile = prj_info['CROSS_COMPILE'] if prj_info['CROSS_COMPILE'] else pjoin(self.__android_top, self.__armgcc)

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
            "env_setup": pjoin(self.__android_top, "buildroot/build/envsetup.sh"),
            "gendroid": get_config_file("gendroid"),
        }
