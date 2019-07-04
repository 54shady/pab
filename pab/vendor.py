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
    afptool = pabObj.android_top + "/pabout/afptool"
    cmd1 = "%s -pack pabout pabout/update.img" % afptool
    pabObj.run_command(cmd1)
    rkimagetool = pabObj.android_top + "/pabout/rkImageMaker"
    release_update = pabObj.kernel_target_image[7:-4] + '-' + pabObj.time_stamp + '.img'
    cmd2 = "%s -RK330C pabout/MiniLoaderAll.bin pabout/update.img pabout/%s -os_type:androidos" % (rkimagetool,
            release_update)
    pabObj.run_command(cmd2)
    pabObj.print_success("===> pabout/%s" % release_update)
