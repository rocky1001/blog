Title: 树莓派与摄像头
Date: 2015-09-11 17:46
Category: rpi
Tags: rpi, camera
Summary: 树莓派使用摄像头的一些概述.
Slug: rpi-camera

最初在购买树莓派时,考虑到家里有两个闲置的USB摄像头,因此没有购买配套的树莓派摄像头(CSI接口).

在将家里的两个USB摄像头跟树莓派连起来,并做了简单测试后,  
发现:

**这两个USB摄像头的效果极差...**  
(主要原因是摄像头的年龄较大,基本都是在08年前购买的用于视频聊天的)

随后,又去淘宝买了树莓派配套的CSI摄像头.

这里简单记录下折腾和测试这些摄像头的经过,

关于CSI摄像头的使用,后续会有专门的blog分享.

##USB摄像头

###硬件
将USB摄像头直接插到树莓派的USB接口,  使用:
````
lsusb
````
查看摄像头能否被正确识别(这里有一个[树莓派支持的摄像头列表](http://elinux.org/RPi_USB_Webcams "")),

不过我的两个古董级别的摄像头虽然都不在列表中,仍然被识别了...

此时可以找到这样一个设备:
````
/dev/video0
````

###软件
USB摄像头对应的工具有两款:

轻量级的fswebcam


全能选手motion


##官方CSI摄像头


###软件
树莓派提供了raspivid和raspistill两个摄像头应用工具,文档在这里:

此外,还有一个好用的python封装工具包picamera:
参考文档
http://picamera.readthedocs.org/en/release-1.10/quickstart.html



