Title: 高性能Web App实践之OpenResty conf配置文件编程[3]
Date: 2016-04-26 18:31
Category: work
Tags: openresty, conf
Summary: 为了解决工作中遇到的高性能Web App实现问题，考虑采用openresty和lua的方案，本篇为系列文章的第二篇，Lua的语法与使用.
Slug: high-performence-web-app[3]-openresty-conf

OpenResty需要对Nginx的conf配置文件进行相应的coding，以处理一些简单的业务逻辑（复杂的业务逻辑还是推荐放到Lua中实现）。

而Nginx的配置文件使用的就是一门微型的编程语言，许多真实世界里的 Nginx 配置文件其实就是一个一个的小程序。

本篇文章主要对conf编程进行简单的介绍。

##nginx processing phase
nginx处理共有11个phase：

1. 



##openresty module
不要使用module关键字，而是做如下定义：

```lua
local _M = {}

funciton _M.func1()
    ...
end

return _M
```

尽可能在所有定义变量的地方使用local关键字，避免全局变量。

##遇到的问题



##log记录要求


