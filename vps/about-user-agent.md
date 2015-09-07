Title: 关于UserAgent的那点事
Date: 2015-09-07 16:28
Category: vps
Tags: user agent, browser, ua
Summary: 记录博客日常维护中发现的一些UA数据,会不定期更新.
Slug: about-user-agent

在vps上面博客的日常维护中发现了一些有意思的UA数据,这里简单记录下.


##微信内置浏览器的UA

微信使用wifi网络时的UA

````
"Mozilla/5.0 
(Linux; U; Android 4.4.4; zh-cn; 
Che1-CL10 Build/Che1-CL10) 
AppleWebKit/533.1 
(KHTML, like Gecko)Version/4.0 
MQQBrowser/5.4 TBS/025440 Mobile 
Safari/533.1 
MicroMessenger/6.2.5.51_rfe7d7c5.621 
NetType/WIFI 
Language/zh_CN"
````

微信使用西安电信4G网络时的UA

````
123.151.42.49 - 
"Mozilla/5.0 
(Linux; U; Android 4.4.4; zh-cn; 
Che1-CL10 Build/Che1-CL10) 
AppleWebKit/533.1 
(KHTML, like Gecko)Version/4.0 
MQQBrowser/5.4 TBS/025440 Mobile 
Safari/533.1 
MicroMessenger/6.2.5.51_rfe7d7c5.621 
NetType/ctlte 
Language/zh_CN"
````


##QQ内置浏览器的UA

QQ使用wifi网络时的UA

````
"Mozilla/5.0 
(Linux; U; Android 4.4.4; zh-cn; 
Che1-CL10 Build/Che1-CL10) 
AppleWebKit/533.1 
(KHTML, like Gecko)Version/4.0 
MQQBrowser/5.4 TBS/025442 Mobile 
Safari/533.1 V1_AND_SQ_5.8.0_264_YYB_D 
QQ/5.8.0.2505 
NetType/WIFI 
WebP/0.3.0"
````

QQ使用西安电信4G网络时的UA

````
36.45.33.47 - 
"Mozilla/5.0 
(Linux; U; Android 4.4.4; zh-cn; 
Che1-CL10 Build/Che1-CL10) 
AppleWebKit/533.1 
(KHTML, like Gecko)Version/4.0 
MQQBrowser/5.4 TBS/025442 Mobile 
Safari/533.1 V1_AND_SQ_5.8.0_264_YYB_D 
QQ/5.8.0.2505 
NetType/4G 
WebP/0.3.0"
````


##简单分析:

* QQ和微信使用的都是QQ移动浏览器内核,但是版本稍有不同;

* 两者都上传了Android系统版本号和语言;

* 两者都上传了设备本身的识别编号;

* 两者都上传了自身的软件版本号;

* 两者都上传了连网方式(WIFI或移动),  
不同的是微信记录的上网方式更为细致(见上例, ctlte应该是china telecom lte, 即中国电信4G的缩写).