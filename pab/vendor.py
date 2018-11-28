#!/usr/bin/env python
# coding=utf-8

from misc import parse_kv_file
from config_file import get_config_file


def get_vendor_xxx_info():
    pabrc = get_config_file("pabrc")
    brc = parse_kv_file(pabrc)
    version_nb = brc.get('VERSION_NUMBER')
    android_version = brc.get('VENDOR_ANDROID_VERSION')
    platform_name = brc.get('VENDOR_PLATFORM_NAME')
    platform_id = brc.get('VENDOR_PLATFORM_ID')
    vendor_tag = brc.get('VENDOR_TAG')
    vendor_suffix = brc.get('VENDOR_SUFFIX')
    passwd = brc.get('VENDOR_PASSWD')
    vendor_tag = "_%s_%s_%s_V%s.%s_" % (vendor_tag,
                                        android_version, platform_name, platform_id, version_nb)
    return vendor_suffix, passwd, vendor_tag


def vendor_xxx(pabObj):
    """
    xxx is specific vendor name
    """
    vendor_suffix, passwd, vendor_tag = get_vendor_xxx_info()
    pab_package_prefix = pabObj.product_device[7:] + vendor_tag
    vendor_package_name = pab_package_prefix + \
        pabObj.time_stamp + "." + vendor_suffix

    # pack file list below under metadata
    vendor_file = get_config_file("vendor")
    pack_list = []
    with open(vendor_file) as f:
        pack_list = f.read().splitlines()

    # Found no file to pack? exit
    if pack_list == []:
        pabObj.goto_exit("check your %s" % vendor_file)

    # rar a -ep -hpxxx package file
    # xxx is passwd
    # exclude path from name
    pack_cmd = "/usr/bin/rar a -ep -hp%s" % passwd
    pack_cmd += " metadata/%s" % vendor_package_name
    for pimages in pack_list:
        pack_cmd += " metadata/%s" % pimages

    pabObj.run_command(pack_cmd)
    pabObj.print_success("===> metadata/" + vendor_package_name)
