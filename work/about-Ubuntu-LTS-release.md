Title: 关于Ubuntu版本的选择
Date: 2015-08-31 14:09
Category: work
Tags: ubuntu, release, lts
Summary: 关于Ubuntu版本的选择.
Slug: about-Ubuntu-lts-release

##关于Ubuntu的LTS版本

除了desktop/server的划分外(桌面环境建议使用desktop, 服务器建议使用server),  
 ubuntu的版本还有普通release和LTS release的区别.
 
LTS release指的是:长期支持(long-term support),  
主要是面向商务用户推出的版本, 可以提供长期的更新(主要是安全方面的).

下面是ubuntu最近一些版本的生命周期图:
![ubuntu release cycle](http://i.stack.imgur.com/GCQzW.png "ubuntu release cycle")

可见,LTS版本具有远远超过其他版本的生命周期.

大部分VPS提供的常用ubuntu版本都是LTS的,所以不会有什么大的问题.

那么, 如果不幸地在某些环境上面安装了非LTS版本的ubuntu会有什么问题呢?

12年底时,我在一台测试PC上面手动安装了当时最新的ubuntu 13.04版本的系统,  
近期在安装工具时,发现所有的源上面都没有13.04版本的软件可用了(当时安装完毕后,为了性能考虑,手动更换为国内网易的源),

查找了国内外的一些源,发现都没有13.04的软件可用.

所以,一个很直接的问题是:在超过生命周期后,通过apt-get安装软件时,软件源上面会找不到任何对应的软件可供安装.

##非LTS Ubuntu版本软件源的设置

多次google后,查找到ubuntu官方会有一个**old-releases.ubuntu.com**源专门供这些不再提供更新支持的非LTS版本使用,记录如下:    
(raring是13.04的官方代号)
````
cat /etc/apt/sources.list

deb http://old-releases.ubuntu.com/ubuntu/ raring main universe restricted multiverse
deb http://old-releases.ubuntu.com/ubuntu/ raring-security universe main multiverse restricted
deb http://old-releases.ubuntu.com/ubuntu/ raring-updates universe main multiverse restricted
deb http://old-releases.ubuntu.com/ubuntu/ raring-proposed universe main multiverse restricted
deb http://old-releases.ubuntu.com/ubuntu/ raring-backports universe main multiverse restricted
````

PS: 更换ubuntu的软件源也是修改上述同一个文件,将上述路径替换为找到的合适的源的路径即可.
````
网易源
deb http://mirrors.163.com/ubuntu/ trusty main restricted universe multiverse
deb http://mirrors.163.com/ubuntu/ trusty-security main restricted universe multiverse
deb http://mirrors.163.com/ubuntu/ trusty-updates main restricted universe multiverse
deb http://mirrors.163.com/ubuntu/ trusty-proposed main restricted universe multiverse
deb http://mirrors.163.com/ubuntu/ trusty-backports main restricted universe multiverse
deb-src http://mirrors.163.com/ubuntu/ trusty main restricted universe multiverse
deb-src http://mirrors.163.com/ubuntu/ trusty-security main restricted universe multiverse
deb-src http://mirrors.163.com/ubuntu/ trusty-updates main restricted universe multiverse
deb-src http://mirrors.163.com/ubuntu/ trusty-proposed main restricted universe multiverse
deb-src http://mirrors.163.com/ubuntu/ trusty-backports main restricted universe multiverse
````

````
搜狐源
deb http://mirrors.sohu.com/ubuntu/ trusty main restricted universe multiverse
deb http://mirrors.sohu.com/ubuntu/ trusty-security main restricted universe multiverse
deb http://mirrors.sohu.com/ubuntu/ trusty-updates main restricted universe multiverse
deb http://mirrors.sohu.com/ubuntu/ trusty-proposed main restricted universe multiverse
deb http://mirrors.sohu.com/ubuntu/ trusty-backports main restricted universe multiverse
deb-src http://mirrors.sohu.com/ubuntu/ trusty main restricted universe multiverse
deb-src http://mirrors.sohu.com/ubuntu/ trusty-security main restricted universe multiverse
deb-src http://mirrors.sohu.com/ubuntu/ trusty-updates main restricted universe multiverse
deb-src http://mirrors.sohu.com/ubuntu/ trusty-proposed main restricted universe multiverse
deb-src http://mirrors.sohu.com/ubuntu/ trusty-backports main restricted universe multiverse
````