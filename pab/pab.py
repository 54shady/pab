#!/usr/bin/env python
# coding=utf-8


import nicecopy
import os
import subprocess
import shutil
import time
from build_argument import BuildArgument
from color_print import ColorPrint
from misc import pjoin
from build_env import BuildEnv
from vendor import get_vendor_xxx_info
from config_file import get_config_file


class PyAndroidBuild():
    def __init__(self):
        # init log function with color enable
        color_print = ColorPrint(True)
        self.print_success = color_print.color_print_success
        self.print_warn = color_print.color_print_warn

        # timestamp
        self.time_stamp = time.strftime('%Y%m%d', time.localtime(time.time()))

        # build argument
        pa = BuildArgument()
        for k, v in pa.argsd.iteritems():
            setattr(self, k, v)
        self.lunchcombo = self.target_product + "-" + self.build_varient

        # build enviroment
        be = BuildEnv(self.product_device)
        for k, v in be.envd.iteritems():
            setattr(self, k, v)

        # vendor
        self.rktools = pjoin(self.uboot_src, "tools")
        self.loader = pjoin(
            self.uboot_out, "RK3288UbootLoader_V2.30.10.bin")

        # final images absolutely path
        self.final_images = pjoin(
            self.android_top, "rockdev/Image-" + self.target_product)

        # final images relatively path
        self.final_images_r = self.final_images[len(self.android_top) + 1:]
        self.logo_resource = pjoin(
            self.uboot_src, "tools/resource_tool/resources")
        self.res_in = pjoin(self.kernel_src, "resource.img")
        self.res_out_logo = "resource_logo.img"
        self.res_out_fdt = "resource_dtb.img"
        self.misc_img = pjoin(self.android_top, "rkst/Image")
        self.vendor_package_tag = get_vendor_xxx_info()[2]

    def goto_exit(self, die_message=None):
        if die_message:
            self.print_warn(die_message)
        os.sys.exit()

    def print_vars(self):
        """ print out all class members """
        for i, j in vars(self).items():
            print "%s=%s" % (i, j)

    def pab_packres(self, res_dir, res_in, res_out):
        """
        pack res into resource.img
        res_dir : directory contain resource ready to pack
        res_in : old resource.img
        res_out : new resource.img with res packed
        """
        target_res_tool = pjoin(self.android_out, "resource_tool")
        # copy resource tool to out dir
        if not os.path.exists(target_res_tool):
            nicecopy.ncopy(self.uboot_src + "/tools/resource_tool",
                           self.android_out)

        # make tool
        make_tool = "make -C %s" % target_res_tool
        self.run_command(make_tool)

        pack_cmd = "%s/pack_resource.sh %s %s %s %s/resource_tool" \
            % (target_res_tool, res_dir, res_in, res_out,
                   target_res_tool)
        self.run_command(pack_cmd)

        nicecopy.ncopy(res_out, self.kernel_src, "resource.img")
        nicecopy.ncopy(res_out, self.kernel_out, "resource.img")
        nicecopy.ncopy(res_out, self.final_images, "resource.img")
        os.remove(res_out)

    def run_command(self, cmd, stdin=None, stdout=None, stderr=None):
        """ run shell command """
        try:
            p = subprocess.Popen(cmd, shell=True,
                                 stdout=stdout, stdin=stdin, stderr=stderr,
                                 executable="/bin/bash")
            p.wait()
            return p.returncode
        except KeyboardInterrupt:
            self.goto_exit("Stop %s" % cmd)

    def install_clean_droid(self):
        """ make installclean """
        # make installclean
        cmd = "%s %s %s %d installclean" % (self.gendroid,
                                            self.env_setup,
                                            self.lunchcombo,
                                            self.jobs_nr)
        self.run_command(cmd)

    def pab_otadiff(self):
        pack_ota_path = pjoin(self.android_top, "out/host/linux-x86")
        pack_ota_key = pjoin(self.android_top, self.ota_key)
        ota_diff_package = "ota_diff.zip"

        # ota_from_target_files [flags] input_target_files output_ota_package
        pack_ota_script = pjoin(self.android_top, self.ota_script)
        build_otadiff_cmd = "%s -v -i %s -p %s -k %s %s %s" % (
            pack_ota_script, self.source_package, pack_ota_path, pack_ota_key,
            self.target_package, ota_diff_package)
        self.run_command(build_otadiff_cmd)

    def pab_geno(self):
        """ build ota package """
        ota_update_uboot = "device/rockchip/" + self.product_device + "/ota/loader"
        ota_update_parameter = "device/rockchip/" + \
            self.product_device + "/ota/parameter"
        nicecopy.ncopy(self.uboot_out + "/RK3288UbootLoader_V2.30.10.bin",
                       ota_update_uboot)
        nicecopy.ncopy(self.android_top + "/metadata/parameter",
                       ota_update_parameter)

        # make ota
        cmd = "%s %s %s %d otapackage" % (self.gendroid,
                                          self.env_setup,
                                          self.lunchcombo,
                                          self.jobs_nr)
        self.run_command(cmd)

        # move ota package to metadata
        ota_package_name = ""
        pab_package_prefix = "%s%s" % (
            self.product_device[7:], self.vendor_package_tag)
        ota_subfix = "_OTA.zip"
        ota_package_name += pab_package_prefix + self.time_stamp + ota_subfix
        cmd_move_ota = "mv -vf %s/*.zip %s/%s" % (self.android_out,
                                                  self.android_top + "/metadata", ota_package_name)
        self.run_command(cmd_move_ota)

        # do the clean
        os.remove(ota_update_uboot + "/RK3288UbootLoader_V2.30.10.bin")
        os.remove(ota_update_parameter + "/parameter")

    def pab_gendroid(self):
        """ build android """
        cmd = "%s %s %s %d" % (self.gendroid,
                               self.env_setup,
                               self.lunchcombo,
                               self.jobs_nr)
        ret = self.run_command(cmd)
        if ret:
            self.goto_exit()

    def pab_genus(self):
        # copy userdata
        nicecopy.ncopy(pjoin(self.android_out,
                             "userdata.img"), pjoin(self.android_top, "metadata"))

    def pab_genu(self):
        """ build uboot """
        # clean all
        if os.path.exists(self.uboot_out):
            shutil.rmtree(self.uboot_out)

        # make uboot config
        make_uboot_config = self.pab_make_target(self.uboot_src, self.uboot_out,
                                                 self.uboot_config)

        if not os.path.exists(pjoin(self.uboot_out, ".config")):
            self.run_command(make_uboot_config)

        nicecopy.ncopy(self.rktools, self.uboot_out)

        # make uboot, which just make without named target
        make_uboot = self.pab_make_target(self.uboot_src, self.uboot_out, "")
        self.run_command(make_uboot)

        nicecopy.ncopy(self.loader, self.final_images)

        # pack logo
        self.pab_packres(self.logo_resource, self.res_in,
                         self.res_out_logo)

        # print some info
        loadername = self.loader.split('/')[-1]
        self.print_success("===> %s" %
                           (os.path.join(self.final_images_r, loadername)))

    def pab_gens(self):
        """ build system image """
        if os.path.exists(self.android_out + '/system'):
            #    st = os.lstat(self.android_out + '/system.img')
            #    system_size = st.st_size
            # BOARD_SYSTEMIMAGE_PARTITION_SIZE
            system_partiton_size = 1073741824
            make_ext4fs_args = "%s/make_ext4fs -l %d -L system -S %s/root/file_contexts -a system \
                %s/system.img %s/system" % (self.host_bin, system_partiton_size, self.android_out, self.final_images,
                                            self.android_out)
            while True:
                ret = self.run_command(make_ext4fs_args)
                if 0 == ret:
                    break

            tunefs = "/sbin/tune2fs -c -1 -i 0 %s/system.img" % (
                self.final_images)
            self.run_command(tunefs)
            e2fscheck = "%s/e2fsck -fyD %s/system.img" % (self.host_bin,
                                                          self.final_images)
            self.run_command(e2fscheck, stderr=subprocess.PIPE,
                             stdout=subprocess.PIPE)
            self.print_success("===> %s" %
                               (os.path.join(self.final_images_r, "system.img")))
        else:
            self.goto_exit("No system dir exist.")

    def pab_genr(self):
        """ build recovery image """
        if os.path.exists(self.android_out + '/recovery/root'):
            cmds = []
            cmd = "%s/mkbootfs %s/recovery/root | %s/minigzip > %s/ramdisk-recovery.img" % \
                (self.host_bin, self.android_out, self.host_bin,
                 self.android_out)
            cmds.append(cmd)
            cmd = "/usr/bin/truncate -s %%4 %s/ramdisk-recovery.img" % self.android_out
            cmds.append(cmd)
            cmd = "%s/mkbootimg --kernel %s/arch/arm/boot/zImage \
                    --ramdisk %s/ramdisk-recovery.img --second %s/resource.img --output %s/recovery.img" % (
                self.host_bin, self.kernel_out, self.android_out, self.kernel_out, self.android_out)
            cmds.append(cmd)
            self.run_cmdlist(cmds)

            nicecopy.ncopy(pjoin(self.android_out,
                                 'recovery.img'), self.final_images)
            # print message
            self.print_success("===> " + self.final_images_r + "/recovery.img")

    def pab_genb(self):
        """ build boot image """
        if os.path.exists(self.android_out + '/root'):
            cmds = []
            cmd = "%s/mkbootfs %s/root | %s/minigzip > %s/ramdisk.img" % \
                (self.host_bin, self.android_out, self.host_bin, self.host_bin)
            cmds.append(cmd)
            cmd = "/usr/bin/truncate -s %%4 %s/ramdisk.img" % self.android_out
            cmds.append(cmd)
            cmd = "%s/mkbootimg --kernel %s/arch/arm/boot/zImage \
                    --ramdisk %s/ramdisk.img --second %s/resource.img --output %s/boot.img" \
                            % (self.host_bin, self.kernel_out,
                               self.android_out, self.kernel_out, self.android_out)

            cmds.append(cmd)
            self.run_cmdlist(cmds)

            nicecopy.ncopy(pjoin(self.android_out,
                                 'boot.img'), self.final_images)
            self.print_success("===> %s" %
                               (os.path.join(self.final_images_r, "boot.img")))
        else:
            self.goto_exit("No root dir exist.")

    def pab_genm(self):
        """ build misc image """
        nicecopy.ncopy(self.misc_img + "/misc.img", self.final_images)
        nicecopy.ncopy(self.misc_img + "/pcba_small_misc.img",
                       self.final_images)
        nicecopy.ncopy(self.misc_img + "/pcba_whole_misc.img",
                       self.final_images)
        # print message
        self.print_success("===> " + self.final_images_r + "/misc.img")
        self.print_success("===> " + self.final_images_r +
                           "/pcba_small_misc.img")
        self.print_success("===> " + self.final_images_r +
                           "/pcba_whole_misc.img")

    def pab_kclean(self):
        # clean all
        if os.path.exists(self.kernel_out):
            shutil.rmtree(self.kernel_out)

    def pab_make_target(self, src, out, target):
        """ wraper for make x """
        make_target = "make -C %s ARCH=arm CROSS_COMPILE=%s O=%s %s -j%d" \
            % (src, self.cross_compile,
               out, target, self.jobs_nr)
        return make_target

    def pab_kconfig(self):
        # no config file, generate it first
        make_config = self.pab_make_target(
            self.kernel_src, self.kernel_out, self.kernel_config_file)
        if not os.path.exists(pjoin(self.kernel_out, ".config")):
            self.run_command(make_config)

        # make menuconfig
        make_menuconfig = self.pab_make_target(
            self.kernel_src, self.kernel_out, "menuconfig")
        self.run_command(make_menuconfig)

    def run_cmdlist(self, cmd_list):
        for cmd in cmd_list:
            self.run_command(cmd)

    def append_modules_target(self, cmd_list):
        make_module = self.pab_make_target(
            self.kernel_src, self.kernel_out, "modules")
        cmd_list.append(make_module)

    def make_kernel_modules_only(self):
        l = []
        self.append_modules_target(l)
        self.run_cmdlist(l)

    def pab_genk(self):
        """ build kernel """
        # copy necessary file or dir
        prev_copy_filename = get_config_file("prevcp")
        with open(prev_copy_filename) as f:
            cp_list = f.read().splitlines()
        nicecopy.copy_stuffs(self.kernel_src, self.kernel_out, cp_list)

        # all the target cmd
        make_cmds = []

        # config cmd
        make_config = self.pab_make_target(
            self.kernel_src, self.kernel_out, self.kernel_config_file)

        # not config file? make one
        if not os.path.exists(pjoin(self.kernel_out, ".config")):
            make_cmds.append(make_config)

        # kernel cmd
        make_kernel = self.pab_make_target(
            self.kernel_src, self.kernel_out, self.kernel_target_image)
        make_cmds.append(make_kernel)

        # dtb cmd
        dtb_file = get_config_file("dtbs")
        k = []
        v = []
        with open(dtb_file) as f:
            dtb_list = f.read().splitlines()

        # dtb file not empty
        if not dtb_list == []:
            for dtb in dtb_list:
                k.append(dtb)
                v.append(dtb[len('rk3288-'):-len('.dtb')].swapcase() + '.dtb')
                make_dtb = self.pab_make_target(self.kernel_src,
                                                self.kernel_out, dtb)
                make_cmds.append(make_dtb)

            # map dtb to alias name
            # dtbs_d = {'rk3288-aaa.dtb' : AAA.dtb}
            dtbs_d = dict(zip(k, v))

        # modules cmd
        self.append_modules_target(make_cmds)

        # start make things we need
        self.run_cmdlist(make_cmds)

        # dtb file not empty
        if not dtb_list == []:
            # pack resource image
            # multi dtb supported
            fdt_res_dir = pjoin(self.android_top, "fdt_res")
            if not os.path.exists(fdt_res_dir):
                os.mkdir(fdt_res_dir)

            # copy dtbs to fdt_res_dir
            dtbs_dir = pjoin(self.kernel_out, "arch/arm/boot/dts/")

            for i in range(len(dtb_list)):
                nicecopy.ncopy(dtbs_dir + dtb_list[i], fdt_res_dir,
                               dtbs_d[dtb_list[i]])

            fdt_res = pjoin(self.android_top, "fdt_res")
            res_in = pjoin(self.kernel_out, "resource.img")
            res_out = pjoin(fdt_res, "resource_fdt.img")
            self.pab_packres(fdt_res, res_in, res_out)
            shutil.rmtree(fdt_res_dir)

        # Misc stuff
        post_copy_filename = get_config_file("postcp")
        with open(post_copy_filename) as f:
            misc_stuff = f.read().splitlines()
        nicecopy.copy_stuffs(self.kernel_out, self.kernel_src, misc_stuff)

        # final copy
        final_copy = [
            "kernel.img",
            "resource.img"
        ]
        nicecopy.copy_stuffs(self.kernel_out, self.final_images, final_copy)
