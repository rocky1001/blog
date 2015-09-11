Title: 树莓派的基本操作
Date: 2015-09-11 16:10
Category: rpi
Tags: rpi, basic opt
Summary: 介绍树莓派的一些基本命令与参数.
Slug: rpi-basics

之前的blog已经对[树莓派的硬件,软件和应用场景](<{filename}/rpi/my-raspberry-pi-2.md> "my-raspberry-pi-2")进行过介绍,

还介绍过如何[将树莓派作为电视盒子](<{filename}/rpi/make-rpi-home-media-center.md> "make-rpi-home-media-center")使用.

这篇blog准备从另一个角度入手,记录并分享下树莓派(raspbian os)的一些常用设置和命令等.

##raspbian

raspbian是树莓派官方推荐的操作系统,基于debian.

一些常用操作系统命令(可以参见[这里](https://www.raspberrypi.org/documentation/linux/usage/commands.md ""))与debian和ubuntu等都是一样的(例如apt-get等),  
不再赘述.

##raspbian中树莓派特有的配置命令

###基础配置
````
raspi-config
````
(重新)打开第一次启动时出现的树莓派配置图形命令行界面,

可以进行对树莓派进行各项设置:
````
                        Raspberry Pi Software Configuration Tool (raspi-config)

Setup Options

    1 Expand Filesystem              Ensures that all of the SD card storage is available to the OS
    2 Change User Password           Change password for the default user (pi)
    3 Enable Boot to Desktop/Scratch Choose whether to boot into a desktop environment, Scratch, or the command line
    4 Internationalisation Options   Set up language and regional settings to match your location
    5 Enable Camera                  Enable this Pi to work with the Raspberry Pi Camera
    6 Add to Rastrack                Add this Pi to the online Raspberry Pi Map (Rastrack)
    7 Overclock                      Configure overclocking for your Pi
    8 Advanced Options               Configure advanced settings
    9 About `raspi-config`           Information about this configuration tool

                                   <Select>                                  <Finish>
````

###固件升级
````
rpi-update
````
树莓派固件(firmware)更新工具.

例如,需要使用树莓派摄像头的一些[新功能](https://www.raspberrypi.org/blog/new-camera-mode-released/ "")时,就需要用此命令更新固件.

固件与os的区别:

1. 固件用于驱动硬件设备(例如,启动时会被加载到GPU,用于驱动GPU)
2. 固件有点类似于PC的BIOS
3. 固件(包括更新的固件)是存储在TF卡中的

###参数查看
````
vcgencmd 
````

树莓派(实际上是Broadcom)特有的[系统参数查看命令](http://elinux.org/RPI_vcgencmd_usage ""),可使用的参数如下:

````
>vcgencmd commands
commands="vcos, ap_output_control, ap_output_post_processing, vchi_test_init, vchi_test_exit,
pm_set_policy, pm_get_status, pm_show_stats, pm_start_logging, pm_stop_logging, version, commands,
set_vll_dir, led_control, set_backlight, set_logging, get_lcd_info, set_bus_arbiter_mode,
cache_flush, otp_dump, codec_enabled, measure_clock, measure_volts, measure_temp, get_config,
hdmi_ntsc_freqs, render_bar, disk_notify, inuse_notify, sus_suspend, sus_status, sus_is_enabled,
sus_stop_test_thread, egl_platform_switch, mem_validate, mem_oom, mem_reloc_stats, file,
vctest_memmap, vctest_start, vctest_stop, vctest_set, vctest_get"
````  

常用参数:

1. 查看当前系统主要参数 vcgencmd get_config
2. 查看CPU温度 vcgencmd measure_temp
3. 查看CPU运行频率 vcgencmd measure_clock arm
4. 查看CPU和GPU的内存分配情况 vcgencmd get_mem arm && vcgencmd get_mem gpu

##如何延长TF卡的使用寿命

树莓派使用普通TF卡作为主存储器,而TF本身是有一定的读写寿命的,下面分享下如何有效延长TF卡的使用寿命.

###常用缓存目录挂载到内存
修改/etc/fstab文件,将硬盘的一些缓存目录指向内存中:
````
>vi /etc/fstab
tmpfs    /tmp    tmpfs    defaults,noatime,nosuid,size=100m    0 0
tmpfs    /var/tmp    tmpfs    defaults,noatime,nosuid,size=50m    0 0
tmpfs    /var/log    tmpfs    defaults,noatime,nosuid,mode=0755,size=50m    0 0
tmpfs    /var/run    tmpfs    defaults,noatime,nosuid,mode=0755,size=5m    0 0
tmpfs    /var/cache/apt/archives tmpfs size=100M,defaults,noexec,nosuid,nodev,mode=0755 0 0
````

###关闭swap分区

在raspbian上面，可以执行：
````
sudo apt-get remove dphys-swapfile
sudo dphys-swapfile uninstall
sudo swapoff --all
````

###将频繁操作的目录挂接到外接移动存储设备
修改/etc/fstab文件(sdb是外接硬盘，1，2，3是对应的分区):

````
>vi /etc/fstab
/dev/sdb1       /var        ext4   defaults    0  1
/dev/sdb2       /home       ext4   defaults    0  1
/dev/sdb3       /tmp        ext4   defaults    0  1

````

###将pi设置为从usb挂载的移动存储设备启动

我并没有做这样的设置,配置方法可以参见下面的两个blog:

[Booting a Raspberry Pi reliably from USB in the presence of multiple USB](http://blog.krastanov.org/2014/01/30/booting-pi-reliably-from-usb/ "")

[Raspberry Pi Root FS on USB Drive - MitchTech | MitchTech](http://mitchtech.net/raspberry-pi-root-fs-on-usb-drive/ "")
