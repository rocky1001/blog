Title: 我的树莓派2
Date: 2015-08-31 17:03
Category: rpi
Tags: raspberry pi
Summary: 介绍我的树莓派.
Slug: my-raspberry-pi-2

2015年8月中旬忍不住诱惑,剁手树莓派2一台(wifi网卡,tf卡,风扇等小配件这里略过不表),   
DHT11温湿度传感器一个, 因为家里有个旧的闲置USB摄像头,就暂时没有买摄像头.

目前已经用一张旧的8G tf卡刷了OpenELEC系统,并刷入了足够多的国内视频插件,  
将树莓派做成了一个机顶盒使用(会另外写篇blog[写篇blog](<{filename}/rpi/make-rpi-home-media-center.md> "make-rpi-home-media-center")描述下详细过程).

还另外准备了16G的tf卡,刷入了最新的raspbian系统,准备进行DHT11的相关开发.

##树莓派是什么

树莓派是什么,这里主要说一下我的理解:  

###硬件
1. 是一台具备900MHzCPU, 1G RAM, TF卡ROM的**mini pc**单板;
2. 一个HDMI接口,四个USB2.0接口,一个百兆LAN口,一个3.5mm音频口
3. 40个GPIO口(包括3.3v,5v电压,接地等接口)    

运行功率仅有3W.

###软件
1. 官方[raspbian](https://www.raspberrypi.org/downloads/raspbian/ "raspbian")(based on Debian)
2. 微软[Windows 10 IoT Core](http://ms-iot.github.io/content/en-US/Downloads.htm "Windows 10 IoT Core")
3. Ubuntu和其他专用OS(OpenELEC, OSMC等用于多媒体中心的专用系统)--参见[这里](https://www.raspberrypi.org/downloads/ "其他OS")  


##树莓派能干什么  

插上wifi网卡,接上hdmi输出 and power on, 你得到了一台mini pc;  

如果用的是OpenELEC或OSMC等OS,那么你得到的是一台即开即用的电视盒子(说好听点叫家庭多媒体中心).
  
纯软件的常用应用有:
##
* 电视盒子(OpenELEC, OSMC等均可)
* 网络资源下载机(使用aria2工具挂机下载)
* wifi网络抓包分析破解工具(因为树莓派功耗极低,实在是非常适合做这种需要长时间运行的工具)
* web server
* 家用nas(树莓派各项IO指数较低,用做家用nas稍显不足)

不过,以上这些都不是重点,重点是:

###树莓派通过GPIO接口,为物理世界(硬件世界)和网络世界(软件世界)架起了一座桥梁.

通过这座桥,可以方便地将硬件世界中的各种传感器或传动器,  
与软件控制连结起来,用高级语言(官方建议python)完成各种各样的魔法:

* 如何有摄像头,很好,可以做视频监控,运动物体检测,图片识别
* 如果有温湿度传感器,气压传感器,可以做实时天气监测
* 如果有电池给树莓派供电,有马达可以驱动,再加上四个轮子,可以实现可编程小车
* ...