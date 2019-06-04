#!/usr/bin/env python
# coding=utf-8

import argparse
import textwrap
import os
import argcomplete
from misc import parse_kv_file
from config_file import get_config_file


class BuildArgument():
    def __init__(self):
        parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                         description=textwrap.dedent('''\
                     Python Build for Linux
                     --------------------------------------------------
                     Build the whole world if no argument given
                     --------------------------------------------------
                     '''))

        parser.add_argument(
            "-j", "--jobs", help="running jobs", type=int)
        parser.add_argument(
            "-p", "--package", help="build update image", action="store_true")
        parser.add_argument(
            "-k", "--kernel", help="build kernel", action="store_true")
        parser.add_argument(
            "--kmodule", help="build kernel modules only", action="store_true")
        parser.add_argument(
            "--kdefconfig", help="kernel defconfig file", type=str)
        parser.add_argument(
            "--ktarget", help="kernel target image", type=str)
        parser.add_argument(
            "-c", "--menuconfig", help="kernel config", action="store_true")
        parser.add_argument(
            "-u", "--uboot", help="build uboot", action="store_true")
        parser.add_argument(
            "--udefconfig", help="uboot defconfig file", type=str)
        parser.add_argument(
            "-r", "--rootfs", help="build rootfs", action="store_true")
        parser.add_argument(
            "--module", help="Alternative for make submodule", type=str)
        parser.add_argument(
            "-C", "--clean", help="Clean build images", type=str,
            choices=["kernel", "uboot"])
        parser.add_argument(
            "--pack", help="pack images", type=str,
            choices=["boot"])

        # auto complete the argument with TAB
        argcomplete.autocomplete(parser)

        # parse the args
        args = parser.parse_args()

        # run this tool on android top dir
        self.__buildconfig = get_config_file("pabrc")
        try:
            assert os.path.exists(self.__buildconfig)
        except AssertionError:
            print 'Error : Not on android source tree'
            os.sys.exit()

        prj_info = parse_kv_file(self.__buildconfig)
        self.__build_target = get_config_file("bt")
        build_target = parse_kv_file(self.__build_target)

        self.__build_vendor_package = True if args.package else False
        self.__build_kernel = True if args.kernel else False
        self.__build_kmodule_only = True if args.kmodule else False
        self.__build_uboot = True if args.uboot else False

        # for submodule
        self.__module = args.module if args.module else False

        # clean what build?
        self.__clean_kernel = True if args.clean == "kernel" else False
        self.__clean_uboot = True if args.clean == "uboot" else False

        # kernel defconfig file and tareget build
        self.__kdefconfig = args.kdefconfig if args.kdefconfig else build_target.get("KERNEL_CONFIG_FILE")
        self.__ktarget_image = args.ktarget if args.ktarget else build_target.get("KERNEL_TARGET_IMAGE")

        # uboot defconfig file
        self.__udefconfig = args.udefconfig if args.udefconfig else build_target.get("UBOOT_CONFIG_FILE")

        # pack x images
        self.__pack_boot = True if args.pack == "boot" else False

        self.__kernel_config = True if args.menuconfig else False
        self.__pack_system = True if args.rootfs else False

        self.__jobs_nr = args.jobs if args.jobs else 16

        self.argsd = {
            "build_kernel": self.__build_kernel,
            "build_kmodule": self.__build_kmodule_only,
            "build_uboot": self.__build_uboot,
            "build_vendor": self.__build_vendor_package,
            "clean_kernel": self.__clean_kernel,
            "clean_uboot": self.__clean_uboot,
            "pack_boot": self.__pack_boot,
            "kernel_config": self.__kernel_config,
            "pack_system": self.__pack_system,
            "submodule": self.__module,
            "kernel_config_file": self.__kdefconfig,
            "kernel_target_image": self.__ktarget_image,
            "uboot_config": self.__udefconfig,
            "jobs_nr": self.__jobs_nr
        }

    def print_vars(self):
        """ print out all class members """
        for i, j in vars(self).items():
            print "%s=%s" % (i, j)
