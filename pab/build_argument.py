#!/usr/bin/env python
# coding=utf-8

import argparse
import textwrap
import os
import argcomplete
from misc import parse_kv_file


class BuildArgument():
    def __init__(self):
        parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                         description=textwrap.dedent('''\
                     Python Android Builder
                     --------------------------------------------------
                     Build the whole android world if no argument given
                     --------------------------------------------------
                     '''))

        # bool
        parser.add_argument(
            "-a", "--droid", help="build android", action="store_true")
        parser.add_argument(
            "--diffota", help="build android diff OTA package", action="store_true")
        parser.add_argument(
            "-p", "--package", help="build vendor package", action="store_true")
        parser.add_argument(
            "-k", "--kernel", help="build kernel", action="store_true")
        parser.add_argument(
            "-u", "--uboot", help="build uboot", action="store_true")
        parser.add_argument(
            "-c", "--menuconfig", help="kernel config", action="store_true")
        parser.add_argument(
            "-s", "--system", help="pack system image", action="store_true")
        parser.add_argument(
            "-O", "--buildota", help="build Android OTA package", action="store_true")

        # int
        parser.add_argument(
            "-j", "--jobs", help="running jobs", type=int)

        # string
        parser.add_argument(
            "-t", "--target_product", help="target_product for android", type=str)
        parser.add_argument(
            "-v", "--build_varient", help="userdebug or user", type=str,
            choices=["userdebug", "user"])
        parser.add_argument(
            "--source", help="OTA source package", type=str)
        parser.add_argument(
            "--target", help="OTA target package", type=str)
        parser.add_argument(
            "-C", "--clean", help="Clean build images", type=str,
            choices=["android", "kernel"])

        # auto complete the argument with TAB
        argcomplete.autocomplete(parser)
        # 1. put the line below in ~/.bashrc
        #   eval "$(register-python-argcomplete pad)"
        # 2. install the complete function
        # activate-global-python-argcomplete [--user]

        # parse the args
        args = parser.parse_args()

        # run this tool on android top dir
        self.__buildconfig = "pabuild/pabrc"
        try:
            assert os.path.exists(self.__buildconfig)
        except AssertionError:
            print 'Error : Not on android source tree'
            os.sys.exit()

        prj_info = parse_kv_file(self.__buildconfig)

        self.__build_droid = True if args.droid else False
        self.__build_vendor_package = True if args.package else False
        self.__build_kernel = True if args.kernel else False
        self.__build_uboot = True if args.uboot else False
        self.__diff_ota = True if args.diffota else False

        self.__source = args.source if args.source else False
        self.__target = args.target if args.target else False

        # clean what build?
        self.__clean_kernel = True if args.clean == "kernel" else False
        self.__clean_android = True if args.clean == "android" else False

        self.__kernel_config = True if args.menuconfig else False
        self.__pack_system = True if args.system else False
        self.__build_ota = True if args.buildota else False

        self.__jobs_nr = args.jobs if args.jobs else 16

        # TARGET_PRODUCT = AAA_BBB
        # PRODUCT_DEVICE = AAA-BBB
        self.__target_product = args.target_product if args.target_product else prj_info[
            "TARGET_PRODUCT"]
        target_product_aaa = self.__target_product.split('_')[0]
        target_product_bbb = self.__target_product.split('_')[1]
        self.__product_device = target_product_aaa + '-' + target_product_bbb
        self.__build_varient = args.build_varient if args.build_varient else prj_info[
            "TARGET_BUILD_VARIANT"]
        self.argsd = {
            "build_kernel": self.__build_kernel,
            "build_uboot": self.__build_uboot,
            "build_droid": self.__build_droid,
            "build_vendor": self.__build_vendor_package,
            "clean_kernel": self.__clean_kernel,
            "clean_android": self.__clean_android,
            "kernel_config": self.__kernel_config,
            "pack_system": self.__pack_system,
            "build_ota": self.__build_ota,
            "diff_ota": self.__diff_ota,
            "source_package": self.__source,
            "target_package": self.__target,
            "target_product": self.__target_product,  # PRODUCT_NAME
            "product_device": self.__product_device,  # PRODUCT_DEVICE
            "build_varient": self.__build_varient,
            "jobs_nr": self.__jobs_nr
        }

    def print_vars(self):
        """ print out all class members """
        for i, j in vars(self).items():
            print "%s=%s" % (i, j)
