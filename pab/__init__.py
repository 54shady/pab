#!/usr/bin/env python
# coding=utf-8

import nicecopy
import os
import types
from misc import pjoin
from vendor import vendor_xxx
from pab import PyAndroidBuild
from pablist import SingleList


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
    args_action.append_node_rear(pab.build_kernel, build_bootimage)

    # vendor action
    pab.pack_vendor = types.MethodType(vendor_xxx, pab)
    args_action.append_node_rear(pab.build_vendor, pab.pack_vendor)

    # pack images(append in order)
    args_action.append_node_rear(pab.pack_boot, pab.pab_genb)

    # build rootfs
    args_action.append_node_rear(pab.build_rootfs, pab.pab_genrootfs)

    # build recovery
    args_action.append_node_rear(pab.build_recovery, pab.pab_genrecovery)

    # try argument action first
    args_action.do_command()

    # running default action with on argument
    if args_action.default_actionall == 0:
        noargs_action.append_node_rear(1, pab.pab_uclean)
        noargs_action.append_node_rear(1, pab.pab_genu)
        noargs_action.append_node_rear(1, pab.pab_kclean)
        noargs_action.append_node_rear(1, pab.pab_genk)
        noargs_action.do_command()
        pab.print_success("Done.")


if __name__ == '__main__':
    main()
