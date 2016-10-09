Title: 高性能Web App实践之Openresty和Lua[1]
Date: 2016-04-25 18:02
Category: work
Tags: openresty, lua, setup
Summary: 为了解决工作中遇到的高性能Web App实现问题，考虑采用openresty和lua的方案，本篇为系列文章的第一篇，环境安装部署。
Slug: high-performence-web-app[1]-openresty-lua-env-setup


在cookie mapping项目中，随着对接的媒体平台和cm流量的增加，继续使用原有的flask框架做cm server的实现，显然在效率上已经无法满足要求（期望单机可以处理5K-8K QPS的cm流量）。

最近考虑使用openresty框架重构现有的流程，  
将全部cookie mapping流量改为使用openresty框架处理。

这个系列的文章将会分享openresty工具的安装，lua语言（openresty使用的业务逻辑处理动态脚本语言）的使用，  
以及应用openresty后，cm处理的真实压力测试结果。

本篇为这个系列文章的第一篇，openresty和lua的安装。

##是什么
openresty官网给出的[定义](https://openresty.org/cn/ "")如下：

```doc
OpenResty 是一个基于 Nginx 与 Lua 的高性能 Web 平台，其内部集成了大量精良的 Lua 库、第三方模块以及大多数的依赖项。用于方便地搭建能够处理超高并发、扩展性极高的动态 Web 应用、Web 服务和动态网关。

OpenResty 通过汇聚各种设计精良的 Nginx 模块（主要由 OpenResty 团队自主开发），从而将 Nginx 有效地变成一个强大的通用 Web 应用平台。这样，Web 开发人员和系统工程师可以使用 Lua 脚本语言调动 Nginx 支持的各种 C 以及 Lua 模块，快速构造出足以胜任 10K 乃至 1000K 以上单机并发连接的高性能 Web 应用系统。

OpenResty 的目标是让你的Web服务直接跑在 Nginx 服务内部，充分利用 Nginx 的非阻塞 I/O 模型，不仅仅对 HTTP 客户端请求,甚至于对远程后端诸如 MySQL、PostgreSQL、Memcached 以及 Redis 等都进行一致的高性能响应。
```

简单点说，  
OpenResty框架将Nginx（nginx.conf programming :)）与Lua programming结合在一起，提供了一个高并发，高扩展性的
WEB开发框架。

##安装
参考OpenResty官网的[说明](https://openresty.org/cn/installation.html "")直接安装即可。

该安装包集成了Nginx和LuaJIT，以及很多常用的其他模块（redis,mysql,cjson等等）。

##测试
OpenResty默认安装路径为：/usr/local/openresty/

新建如下结构的测试目录：
```doc
openresty/
|-- conf
|   |-- test.conf
|   |-- mime.types
|   `-- nginx.conf
|-- logs
|   |-- access.log
|   `-- error.log
|-- lua
`   `-- test.lua
`-- index.html
```

简单测试nginx.conf配置文件如下:
```doc
worker_processes  1;        #nginx worker 数量
error_log logs/error.log;   #指定错误日志文件路径
events {
    worker_connections 1024;
}

http {
    server {
        #监听端口，若你的8090端口已经被占用，则需要修改
        listen 8090;
        location / {
            default_type text/html;

            content_by_lua_block {
                ngx.say("HelloWorld")
            }
        }
    }
}
```
然后执行：
```shell
nginx -p $INSTALL_DIR -c conf/nginx.conf
```

##生产环境的部署运行

* 尽量避免无意义的'begin', 'finished', 'invalid params', 'error happened'等内容
* 对数据进行log记录时, 要记录:数据名称, 数据类型, 数据长度, 数据内容等信息
* 方法进出可以以debug级别打印方法名称+'begin', 方法名称+'finished'
* 异常打印一定要记录异常名称, 异常消息, 异常数据内容以及异常堆栈数据等, 而不是只记录何时何地发生了异常, 这对解决问题帮助很小
* 打印时要注意数据是否为空或者变量是否未定义, 不要让log打印引入bug
* log打印的格式要统一, 最好有二次封装log类供项目内部统一使用, 避免每个人记录log的不同风格和语法, 为查看log带来困难
