Title: 我的VPS
Date: 2015-08-19 13:55
Category: vps
Tags: vps
Summary: 我的VPS的安全配置,邀请链接等.
Slug: my-vps

##前言

购买了digitalocean的VPS一台,乞丐版(一个月5刀: 1 core, 512 RAM, 20GB SSD)配置也还算够用了.  
最给力的是,他家所有vps目前均不限流量(虽然乞丐版每月1TB流量——平均每天30GB也足够使用的了,但是"不限量"的东西,心理上就很爽).  
这个Blog就是在这个VPS上面搭建的.

顺便附上[我的邀请链接](https://www.digitalocean.com/?refcode=0d2098ef174d "")  
如果你要注册的话,请使用上面的邀请链接,你可以直接得到10刀(乞丐版的VPS可以免费用两个月了).

##安全配置

vps到手后，除了部署一些自己的应用外(Nginx, ss, Java/Python web server)，还做了这样一些安全方面的配置。

###ufw

使用ufw(iptables的简化版)，仅启动了部分常用端口(22,3306,80以及ss专用端口).  
命令格式：ufw {allow|deny|delete allow|status} {host|port|app name} [from ip/host] [to ip/host port]  

但是事实证明上述措施远远不够，第二天看了下ssh的登陆日志，已经有同志们冲上来暴力破解了...  
(查看ssh auth log命令：grep sshd.\*Failed /var/log/auth.log | less)  
下面是一部分日志: 
````
Dec  2 03:10:13 rocky sshd[9144]: Failed password for invalid user dff from 122.225.36.12 port 60888 ssh2
Dec  2 03:10:18 rocky sshd[9146]: Failed password for invalid user oracle from 122.225.36.12 port 33685 ssh2
Dec  2 03:10:26 rocky sshd[9148]: Failed password for invalid user test from 122.225.36.12 port 35354 ssh2
Dec  2 03:10:31 rocky sshd[9150]: Failed password for invalid user oracle from 122.225.36.12 port 36404 ssh2
Dec  2 03:10:37 rocky sshd[9152]: Failed password for invalid user ubuntu from 122.225.36.12 port 37498 ssh2
Dec  2 03:10:42 rocky sshd[9154]: Failed password for invalid user git from 122.225.36.12 port 38742 ssh2
Dec  2 03:10:46 rocky sshd[9156]: Failed password for invalid user boot from 122.225.36.12 port 39760 ssh2
Dec  2 03:10:51 rocky sshd[9158]: Failed password for invalid user 123456 from 122.225.36.12 port 40899 ssh2
Dec  2 03:10:56 rocky sshd[9160]: Failed password for invalid user 123 from 122.225.36.12 port 42168 ssh2
Dec  2 03:11:02 rocky sshd[9162]: Failed password for invalid user r from 122.225.36.12 port 43439 ssh2
Dec  2 03:11:07 rocky sshd[9164]: Failed password for invalid user test from 122.225.36.12 port 48964 ssh2
Dec  2 03:11:11 rocky sshd[9166]: Failed password for invalid user gheghe from 122.225.36.12 port 50117 ssh2
Dec  2 03:11:15 rocky sshd[9168]: Failed password for invalid user nagios from 122.225.36.12 port 51262 ssh2
Dec  2 03:11:19 rocky sshd[9170]: Failed password for invalid user farid from 122.225.36.12 port 52387 ssh2
Dec  2 03:11:24 rocky sshd[9172]: Failed password for invalid user tomcat from 122.225.36.12 port 53576 ssh2
Dec  2 03:11:28 rocky sshd[9174]: Failed password for invalid user cgi from 122.225.36.12 port 54724 ssh2
Dec  2 03:11:33 rocky sshd[9176]: Failed password for root from 122.225.36.12 port 55828 ssh2
Dec  2 03:11:37 rocky sshd[9178]: Failed password for root from 122.225.36.12 port 57070 ssh2
Dec  2 03:11:42 rocky sshd[9180]: Failed password for root from 122.225.36.12 port 58269 ssh2
````
随后,更换了SSH端口号,从默认的22改为较大的端口后,基本上就没有暴力破解的连接了.

###fail2ban

好用的防暴力破解的工具.  
虽说更换端口号可以很大程度上缓解暴力破解的问题,但为了保险起见,还是装上了fail2ban.  

之前也用过denyhost，缺点是只能针对ssh端口的暴力破解,而fail2ban可以对更多端口的暴力破解进行检测.

简单点说,fail2ban其实是一个日志正则解析和处理工具，所以只要有日志的，可以用正则解析的，就可以设定iptables规则进行处理。

使用方式也很简单，修改配置文件，打开ssh, mysql, nginx等的检查就行了.
要注意的是，上述每一项配置中，应用log的路径要检查核对正确.  


ok，暂时就这样，后面会持续更新的。