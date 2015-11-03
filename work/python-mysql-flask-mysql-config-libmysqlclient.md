Title: 解决flask+mysql应用在环境部署时遇到的一些问题
Date: 2015-11-03 10:15
Category: work
Tags: python, mysql, SSL, MySQL-python, libmysqlclient, mysql_config
Summary: 解决新环境安装部署flask应用时, 安装MySQL-python包后, flask应用启动时报错的问题
Slug: python-mysql-flask-mysql-config-libmysqlclient

新环境的部署从来都是让人稍微有点头疼的过程.

全新的环境还好, 要是遇到已经运行了3,4年的老机器, 还要在上面部署安装新的环境和应用就愈发困难.

最近在工作中就遇到了类似的问题.

##目标描述

有一台从其他生产环境退下来的服务器, 

uptime：964 days

OS: CentOS release 5.6 (Final)  
Linux xxx.com 2.6.18-238.el5 #1 SMP Thu Jan 13 15:51:15 EST 2011 x86_64 x86_64 x86_64 GNU/Linux

已有:  
Python 2.6.5 (r265:79063, Feb  8 2012, 16:35:56)   
MySQL Server version: 5.1.59-log Source distribution

可见, 无论是系统还是软件环境都是很老的.

现在需要在这台机器上面安装: pip, flask(以及配套的ORM - SQLAlchemy, MySQL-python等),

用于发布一个简单的WEB APP.

##解决的主要问题

###SSL验证问题

这个服务器的SSL证书出了问题, 在使用get-pip.py安装pip时报错(具体报错信息跟SSL有关), 

当时急着解决问题, 没有将报错信息记录下来.

通过报错信息google搜索后, 找到了[这篇文章](http://eric.lubow.org/2011/security/fixing-centos-root-certificate-authority-issues/ "fixing-centos-root-certificate-authority-issues")

为了防止链接失效, 原文转载如下:
````
Fixing CentOS Root Certificate Authority Issues
1 Jun 2011 — eric

While trying to clone a repository from Github the other day on one of my EC2 servers and I ran into an SSL verification issue. As it turns out, Github renewed their SSL certificate (as people who are responsible about their web presence do when their certificate is about to expire). As a result, I couldn’t git clone over https. This presents a problem since all my deploys work using git clone over https.

The error looks something like this:

*** error: SSL certificate problem, verify that the CA cert is OK. Details:
*** error:14090086:SSL routines:SSL3_GET_SERVER_CERTIFICATE:certificate verify failed while accessing https://github.com/indexzero/daemon.node.git/info/refs
*** fatal: HTTP request failed
*** Clone of 'https://github.com/indexzero/daemon.node.git' into submodule path 'support/daemon' failed
The reason for the error is because CentOS (at least the RightScale version 5.6.8.1 has an old certificate authority bundle: /etc/pki/tls/certs/ca-bundle.crt.

I backed up the existing certificate file just to be on the safe side.
# cp /etc/pki/tls/certs/ca-bundle.crt /root/backup/

To fix the issue, just download a new certificate bundle. I used the one from haxx.se.
# curl http://curl.haxx.se/ca/cacert.pem -o /etc/pki/tls/certs/ca-bundle.crt

````

更新SSL文件后, 问题解决.

###找不到libmysqlclient的问题

这个问题有几种表现形式, 常见错误log如下:

````
Error loading MySQLdb module: libmysqlclient.so.18: cannot open shared object file: No such file or directory
````

````
Error loading MySQLdb module: libmysqlclient_r.so.18: cannot open shared object file: No such file or directory
````

````
Error loading MySQLdb module: libmysqlclient_r.so.16: cannot open shared object file: No such file or directory
````

在网上查找了很久, 有的解决方案很笨,

就是先find到上面缺失的so文件, 然后copy到/usr/lib, /usr/lib64等等目录下面去,

但是[这篇文章](http://mdblog.sinaapp.com/page/%E8%A7%A3%E5%86%B3django%20syncdb%E5%87%BA%E7%8E%B0%E5%8A%A8%E6%80%81%E5%BA%93libmysqlclient.so%E6%89%BE%E4%B8%8D%E5%88%B0%E9%94%99%E8%AF%AF/ "")
的解决办法就很灵活, 就是找到缺失的so文件所在的目录, 

然后将这个路径追加到动态链接库配置文件即可, shell见下(/usr/local/mysql/lib是包含所需so文件的路径):

````
# echo "/usr/local/mysql/lib" >> /etc/ld.so.conf.d/mysql-x86_64.conf 
# ldconfig
````

###找不到mysql_config的问题

是没有安装mysql-devel包引起的,

直接
````
sudo yum install mysql-devel*
````
问题解决.
