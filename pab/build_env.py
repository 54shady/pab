#!/usr/bin/env python
# coding=utf-8

import os
from misc import pjoin
from misc import parse_kv_file


class BuildEnv():
    def __init__(self, product_device):
        self.__android_top = os.path.abspath(os.getcwd())
        self.__otp = "out/target/product"
        self.__android_out = pjoin(
            self.__android_top, self.__otp, product_device)
        self.__armgcc = "prebuilts/gcc/linux-x86/arm/arm-eabi-4.6/bin/arm-eabi-"
        self.__cross_compile = pjoin(self.__android_top, self.__armgcc)
        self.__host_bin = "out/host/linux-x86/bin"
        self.__host_utils_dir = pjoin(self.__android_top, self.__host_bin)
        self.__build_target = "pabuild/build_target"
        build_target = parse_kv_file(self.__build_target)
        self.envd = {
            "android_top": self.__android_top,
            "otp": self.__otp,
            "armgcc": self.__armgcc,
            "host_bin": self.__host_bin,
            "android_out": self.__android_out,
            "uboot_out": pjoin(self.__android_out, "obj", "UBOOT"),
            "kernel_out": pjoin(self.__android_out, "obj", "KERNEL"),
            "cross_compile": self.__cross_compile,
            "host_utils_dir": self.__host_utils_dir,
            "uboot_src": pjoin(self.__android_top, "u-boot"),
            "kernel_src": pjoin(self.__android_top, "kernel"),
            "env_setup": pjoin(self.__android_top, "build/envsetup.sh"),
            "gendroid": pjoin(self.__android_top, "gendroid.sh"),
            "kernel_config_file": build_target.get("KERNEL_CONFIG_FILE"),
            "kernel_target_image": build_target.get("KERNEL_TARGET_IMAGE"),
            "uboot_config": build_target.get("UBOOT_CONFIG_FILE"),
            "ota_script": "build/tools/releasetools/ota_from_target_files",
            "ota_key": "build/target/product/security/testkey"
        }
