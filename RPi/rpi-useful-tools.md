Title: 树莓派上面一些常用工具的安装
Date: 2015-09-11 17:32
Category: rpi
Tags: rpi, samba, windows, android, xrdp
Summary: 介绍树莓派上面一些常用工具的安装
Slug: rpi-useful-tools


##samba
分享下如何使用samba使得树莓派和其他设备之间可以方便地进行文件数据交换.

###安装samba
安装命令如下:
````
sudo apt-get install samba samba-common-bin
````

修改配置文件(之前最好先备份原有的):
````
sudo vim /etc/samba.conf 
````

我的samba配置文件见下:
````
(待补充)
````

设置samba用户名和密码:
````
smbpasswd -a pi
````

samba server启动与停止
````
sudo service smbd restart
````

###rpi访问其他设备的文件系统

首先在设备(以windows为例)上面设置共享目录并设置用户名和密码, 

在rpi上直接mount windows的共享路径到本地某个目录即可.
````
mount –t smbfs ipadd:/sharename /mountpoint –o username=userid,workgroup=workgroupname
````

###其他设备访问rpi的文件系统

其他设备可以直接在网络环境中查找rpi的ip,并打开rpi分享的目录,

我尝试了下面两种访问方式都是正常的:  

* windows访问  
* 使用Android手机的ES文件浏览器App访问  
  
  
##xrdp
在没有显示器的情况下,推荐在rpi上面安装xrdp server,  
安装操作非常简单:
````
sudo apt-get install xrdp
````

然后就可以在windows环境上面很方便地使用远程桌面(mstsc)工具直接连接并操作rpi的桌面环境了.

