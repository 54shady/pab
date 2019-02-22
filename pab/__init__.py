#!/usr/bin/env python
# coding=utf-8

import nicecopy
import os
import types
from misc import pjoin
from vendor import vendor_xxx
from pab import PyAndroidBuild
from pablist import SingleList


def backup_to_metadata(pab):
    # copy to metadata
    for dirpath, dirnames, filenames in os.walk(pab.final_images):
        for f in filenames:
            nicecopy.ncopy(pjoin(pab.final_images, f),
                           pjoin(pab.android_top, "metadata"))
            pab.print_success("===> medatada/" + f)


def main():
    pab = PyAndroidBuild()

    # action list if argument given
    args_action = SingleList()

    # no argument? run this action list
    noargs_action = SingleList()

    # implement the action list in order
    # clean and build uboot
    args_action.append_node_rear(pab.clean_uboot, pab.pab_uclean)
    args_action.append_node_rear(pab.build_uboot, pab.pab_genu)

    # kernel clean, config, modules
    args_action.append_node_rear(pab.clean_kernel, pab.pab_kclean)
    args_action.append_node_rear(pab.kernel_config,
                                 pab.pab_kconfig)
    args_action.append_node_rear(pab.build_kmodule,
                                 pab.make_kernel_modules_only)

    # build boot image
    def build_bootimage():
        pab.pab_genk()
        pab.pab_genb()
    args_action.append_node_rear(pab.build_kernel, build_bootimage)

    # make android installclean
    args_action.append_node_rear(pab.clean_android, pab.install_clean_droid)

    # make android whole world
    def build_all():
        pab.pab_gendroid()
        pab.pab_genb()
        pab.pab_gens()
        pab.pab_genm()
        pab.pab_genr()
        pab.pab_genus()
    args_action.append_node_rear(pab.build_droid, build_all)

    # OTA package build
    args_action.append_node_rear(pab.build_ota, pab.pab_geno)

    # vendor action
    pab.pack_vendor = types.MethodType(vendor_xxx, pab)
    args_action.append_node_rear(pab.build_vendor, pab.pack_vendor)

    # OTA diff package build
    def build_otadiff():
        if pab.source_package and pab.target_package:
            pab.pab_otadiff()
        else:
            diffota_usage = "pab --diffota --source <name> --target <name>"
            print diffota_usage
    args_action.append_node_rear(pab.diff_ota, build_otadiff)

    # pack images(append in order)
    args_action.append_node_rear(pab.pack_boot, pab.pab_genb)

    # for submodule
    args_action.append_node_rear(pab.submodule,
                             pab.pab_droid_make_target)

    # try argument action first
    args_action.do_command()

    # running default action with on argument
    if args_action.default_actionall == 0:
        noargs_action.append_node_rear(1, pab.pab_uclean)
        noargs_action.append_node_rear(1, pab.pab_genu)
        noargs_action.append_node_rear(1, pab.pab_kclean)
        noargs_action.append_node_rear(1, pab.pab_genk)
        noargs_action.append_node_rear(1, pab.install_clean_droid)
        noargs_action.append_node_rear(1, pab.pab_gendroid)
        noargs_action.append_node_rear(1, pab.pab_genrecovery)
        noargs_action.append_node_rear(1, pab.pab_genb)
        noargs_action.append_node_rear(1, pab.pab_gens)
        noargs_action.append_node_rear(1, pab.pab_genm)
        noargs_action.append_node_rear(1, pab.pab_genr)
        noargs_action.append_node_rear(1, pab.pab_genus)
        noargs_action.do_command()
        backup_to_metadata(pab)
        pab.print_success("Done.")


if __name__ == '__main__':
    main()
