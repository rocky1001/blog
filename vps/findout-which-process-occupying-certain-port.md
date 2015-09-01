Title: 查询系统端口占用情况
Date: 2015-09-01 12:43
Category: VPS
Tags: vps, port ,occupy, linux, windows
Summary: 查询OS下的端口占用情况.
Slug: findout-which-process-occupying-certain-port

需要使用的端口被占用是常见的应用启动失败原因.
简单记录下在出现该问题的时候如何查找定位.

##查找占用指定端口的进程

###Linux

使用命令查看端口被哪些进程所占用(将[port]替换为端口号):
````
lsof -i:[port]
````

例如:
````
>lsof -i:80
COMMAND   PID     USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
nginx   1xxxx     xxxx    6u  IPv4 114171      0t0  TCP *:http (LISTEN)
nginx   2xxxx     xxxx    6u  IPv4 114171      0t0  TCP *:http (LISTEN)
````

可见80端口目前是被nginx进程所使用的.

###Windows

使用命令查看端口被哪些进程所占用(将[port]替换为端口号):
````
netstat -aon|findstr "[port]"
````
上述命令可以查出进程id,

然后继续敲(将[pid]替换为前一步查出的进程号):
````
tasklist|findstr "[pid]"
````
即可找到对应的进程了.