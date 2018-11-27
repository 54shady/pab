#!/usr/bin/env python
# coding=utf-8

import nicecopy
import os
import types
from misc import pjoin
from vendor import vendor_xxx
from pab import PyAndroidBuild


def backup_to_metadata(pab):
    # copy to metadata
    for dirpath, dirnames, filenames in os.walk(pab.final_images):
        for f in filenames:
            nicecopy.ncopy(pjoin(pab.final_images, f),
                           pjoin(pab.android_top, "metadata"))
            pab.print_success("===> medatada/" + f)


def main():
    pab = PyAndroidBuild()
    if pab.clean_kernel:
        pab.pab_kclean()
        pab.print_success("Kernel clean done.")
    elif pab.clean_android:
        pab.install_clean_droid()
        pab.print_success("Android install clean done.")
    elif pab.kernel_config:
        pab.pab_kconfig()
    elif pab.build_kernel:
        pab.pab_genk()
        pab.pab_genb()
    elif pab.build_uboot:
        pab.pab_genu()
    elif pab.build_droid:
        pab.pab_gendroid()
        pab.pab_genb()
        pab.pab_gens()
        pab.pab_genm()
        pab.pab_genr()
        pab.pab_genus()
        backup_to_metadata(pab)
    elif pab.pack_system:
        pab.pab_gens()
    elif pab.build_ota:
        pab.pab_geno()
        pab.print_success('Build OTA done.')
    elif pab.build_vendor:
        pab.pack_vendor = types.MethodType(vendor_xxx, pab)
        pab.pack_vendor()
    elif pab.diff_ota:
        if pab.source_package and pab.target_package:
            pab.pab_otadiff()
        else:
            diffota_usage = "pab --diffota --source <name> --target <name>"
            print diffota_usage
    else:  # brandnew build
        pab.pab_genu()
        pab.pab_kclean()
        pab.pab_genk()
        pab.install_clean_droid()
        pab.pab_gendroid()
        pab.pab_genb()
        pab.pab_gens()
        pab.pab_genm()
        pab.pab_genr()
        pab.pab_genus()
        backup_to_metadata(pab)
        pab.print_success("Done.")


if __name__ == '__main__':
    main()
