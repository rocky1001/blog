Title: 树莓派与其他设备的文件交互
Date: 2015-09-11 17:32
Category: rpi
Tags: rpi, samba, windows, android
Summary: 介绍树莓派如何与其他设备(windows, android等)方便地进行文件交互.
Slug: rpi-samba

分享下如何使用samba使得树莓派和其他设备之间可以方便地进行文件数据交换.

samba是什么?

##rpi访问其他设备的文件系统

首先在设备(以windows为例)上面设置共享目录并设置用户名和密码, 

在rpi上直接mount windows的共享路径到本地某个目录即可.

##其他设备访问rpi的文件系统

首先在rpi上面安装samba server并进行简单的配置:

1. 安装
2. 配置/etc/samba.conf
3. 设置用户名和密码
4. windows访问
5. 使用手机ES文件浏览器工具访问  
  
  
##我的配置文件见下:


