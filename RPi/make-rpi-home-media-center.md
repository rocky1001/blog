Title: 将树莓派2打造为家庭多媒体中心(电视盒子)
Date: 2015-09-02 08:30
Category: rpi
Tags: raspberry pi, home media center
Summary: 介绍如何将树莓派2改造为家庭多媒体中心.
Slug: make-rpi-home-media-center

将树莓派改造成电视盒子,应该算是入门级别的应用,因为使用现成的OS实在是太简单了.

##选什么OS

适用于树莓派家庭多媒体中心的OS,目前主流的有两款:  

* OpenELEC([官网](http://openelec.tv/get-openelec "OpenELEC官网"))
* OSMC([官网](https://osmc.tv/download/ "OSMC官网"))

两者的界面,功能比较类似,任意选择一款就好.

我最开始使用的是OSMC,但是烧进tf卡后,rpi启动时卡在OSMC的logo页面一直loading无法进入(该问题目前没有定位解决),

后来换成最新版本的OpenELEC就正常了.

##如何安装OS

推荐看[这篇文章](http://mymediaexperience.com/raspberry-pi-xbmc-with-raspbmc/ "RPi media center OS install"),对于OS的安装方式说的非常详细,这里不在赘述.

##OpenELEC的设置

因为我仅安装试用过OpenELEC系统,这里就以该系统的设置为例进行下说明.

在系统成功安装并且顺利进入后,需要做如下一些修改:

1. 在设置中,修改系统语言为中文(如果不修改后面安装的中文视频网站插件几乎都会因为乱码无法使用) 
 
    这里貌似还有个小bug,在修改系统语言之前,需要先设置系统字体为arial,不然的话语言修改不会生效.
    
2. 安装各种在线视频插件  
    我安装的一些视频插件(国内的优酷等视频网站,百度云等网盘,国外主要是youtube等)可以点[这里]({attach}/files/video-addons.zip)下载到. 
     
    PS: 可能因为rpi这种电视盒子已经不太流行的原因(毕竟现在市面上买个主流的电视盒子也就200块左右,直接用不折腾),
    
    网上能找到的视频插件大多比较老.后面有机会的话也会尝试自己去开发或更新视频插件.
    
3. 设置网络连接(有线无线SSH等)  

    配置有线,无线网络连接;设置允许SSH连接(默认端口22,用户名root,密码openelec)  
    
    推荐打开SSH连接方式,这样可以很方便地在headless的情况下,用各种ssh client连接到rpi的openelec系统中,方便地进行各种配置修改(后面会详细说).


4. 设置无线播放方式

    系统支持UPnP(DLNA)和AirPlay播放方式.

5. 设置允许UPnP控制

    这样就可以方便地使用手机上的app遥控操作了.  
    实测可用的app有两款:Yatse, Kodi Remote

以上设置全部结束后,现在rpi上面的openelec已经可以:  

* 播放USB设备中的媒体
* 播放samba server中的媒体
* 使用手机,pad的DLNA或AirPlay功能播放媒体
* 播放在线视频网站的视频
* 播放百度云上面的视频(需要进行账号设置)  
     
 
##Headless Opt on OpenELEC 

如前所述,打开了SSH连接开关后,可以使用:

默认端口22,用户名root,密码openelec

连接OpenELEC系统.

我之所以想要这么做,主要是因为rpi连接家里的wifi总是有问题,在OpenELEC设置界面上点击wifi后无法弹出密码输入窗口,导致总是连不上wifi;

于是,就转而先用网线将rpi与路由器连接,从路由器控制台查看分配到的ip,再用ssh连接rpi的OpenELEC,在命令行下直接进行wifi设置.

###登录

手机上使用JuiceSSH客户端,配置好地址,端口用户名和密码,即可成功登录.

###wifi设置命令

主要内容来自于[这篇文章](https://gist.github.com/maoueh/8260199 "openelec-setting up wifi in cli").

OpenELEC wifi配置文件存储在这个路径:
````
/storage/.cache/connman
````

常用命令有如下一些:  

* connmanctl enable wifi  
    启用wifi功能

* connmanctl scan wifi  
    查找当前环境可用wifi
    
* connmanctl services  
    列出当前环境所有可用的wifi名称    
    
````  
    *AR uniclick-8f  wifi_e84e062b8cbc_756e69636c69636b2d3866_managed_psk  
    *A  hylinkad     wifi_e84e062b8cbc_68796c696e6b6164_managed_psk  
    360å…è´¹WiFi-19  wifi_e84e062b8cbc_333630e5858de8b4b9576946692d3139_managed_psk 
    7777777          wifi_e84e062b8cbc_37373737373737_managed_psk  
    E7E7             wifi_e84e062b8cbc_45374537_managed_psk  
    HomeNight        wifi_e84e062b8cbc_486f6d654e69676874_managed_psk 
````  

    *A表示已知用户名和密码的wifi; R表示当前正在使用的wifi
    
* 在/storage/.cache/connman路径下, nano/vi \<ssid>.config file   
    新建一个未知wifi的配置文件, 文件内容如下:  
    
````
    [global]
    Name = E7E7
    Description = E7E7 Wifi service config file

    [service_wifi_E7E7]
    Type = wifi
    Name = E7E7
    Passphrase = <passphrase>
````    

* connmanctl connect [service id--wifi_xxxx_xxxx_psk]  
    指定要使用的wifi名称(这里不能使用ssid name, 而要用services list中的service id) 
    
经过以上几步, 就完成了headless时,命令行下设置OpenELEC wifi连接.