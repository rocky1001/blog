Title: Linux下加载和卸载U盘
Date: 2015-09-02 15:55
Category: work
Tags: linux, udisk, mount, umount
Summary: Linux下加载和卸载U盘(包括强制卸载).
Slug: linux-mount-umount-udisk

在公司的测试机(ubuntu 13.04)上面使用U盘copy一些东西,

对于U盘在Linux系统中如何加载和卸载(包括busy的情况)进行一下记录.

##查看U盘的dev挂载名

常用命令:

````
lsusb 查看当前系统中usb总线和设备挂载情况

lsblk 在树状结构中查看所有块设备信息

fdisk -l 查看分区表信息(可以看到u盘是FAT格式还是NTFS格式的)
````

##挂载U盘到文件系统中

mkdir /media/udisk

对于fat格式:
sudo mount -t vfat /dev/sdb1 /media/udisk -o uid=1000,gid=1000,utf8,dmask=027,fmask=137

-o后面的参数的作用是:对挂载的目录赋予足够的读写权限,避免非root用户无法读写的问题.

对于ntfs格式:
sudo mount -t ntfs-3g /dev/sdb1 /media/udisk

##卸载u盘:

###普通卸载:  

````
umount /dev/sdb1
````

PS: 注意,命令**不是unmount**

有时候普通卸载会报错(device busy),此时可以使用:

````
lsof /dev/sdb1
````

查看使用该设备的进程信息,也可以使用:

````
ps aux|grep `fuser -m /dev/sdb1`
````

fuser的作用是查看占用某设备的进程id.

在等待该进程执行完毕,或者手动kill掉进程后,可以再尝试卸载;

###强制卸载:

可以使用如下命令强制卸载某个设备:
````
fuser -km /dev/sdb1

-k 杀掉占用设备的进程
-m 指定已加载的设备
````


