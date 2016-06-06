Title: 高性能Web App实践之Lua初试[2]
Date: 2016-04-26 18:31
Category: work
Tags: lua
Summary: 为了解决工作中遇到的高性能Web App实现问题，考虑采用openresty和lua的方案，本篇为系列文章的第二篇，Lua的语法与使用.
Slug: high-performence-web-app[2]-lua-hello-world

OpenResty使用Lua作为嵌入式脚本语言，处理在nginx.conf中不方便实现的复杂业务逻辑、数据库（sql/nosql）交互等操作。

本篇为这个系列文章的第二篇，介绍lua的版本，语法特性等内容。


##openresty conf文件




##使用lua设置cookie



##遇到的问题
####attempt to set ngx.header.HEADER after sending out response headers
在编写代码并测试的时候，使用了ngx.say进行部分信息的打印。

随后，在使用resty.cookie.set设置cookie时没有成功，在错误日志中看到：  

```shell
[error] 31627#0: *1 attempt to set ngx.header.HEADER after sending out response headers, client: xxx, server: , request: "GET /gen_cookie_test HTTP/1.1", host: "xxx"
```

经过排查发现：  
ngx.say，ngx.print等function会把header发送出去，随后即无法设置header。


##log记录要求


