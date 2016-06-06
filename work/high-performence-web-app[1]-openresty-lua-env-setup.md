Title: 高性能Web App实践之Openresty和Lua[1]
Date: 2016-04-25 18:02
Category: work
Tags: openresty, lua, setup
Summary: 为了解决工作中遇到的高性能Web App实现问题，考虑采用openresty和lua的方案，本篇为系列文章的第一篇，环境安装部署。
Slug: high-performence-web-app[1]-openresty-lua-env-setup


在cookie mapping项目中，随着对接的媒体平台和cm流量的增加，继续使用原有的flask框架做cm server的实现，显然在效率上已经无法满足要求（期望单机可以处理5K-8K QPS的cm流量）。

最近考虑使用openresty框架重构现有的流程，  
将QPS要求较高的流量改为使用openresty框架处理（主要是由媒体发起的cm流量），  
而我们自己发起的cm流量仍然使用原来的flask框架处理。

这个系列的文章将会分享openresty工具的安装，lua语言（openresty使用的业务逻辑处理动态脚本语言）的使用，  
以及应用openresty后，cm处理的真实压力测试结果。

本篇为这个系列文章的第一篇，openresty和lua的安装。

##是什么
openresty官网给出的[定义](https://openresty.org/cn/ "")如下：

```shell
OpenResty 是一个基于 Nginx 与 Lua 的高性能 Web 平台，其内部集成了大量精良的 Lua 库、第三方模块以及大多数的依赖项。用于方便地搭建能够处理超高并发、扩展性极高的动态 Web 应用、Web 服务和动态网关。

OpenResty 通过汇聚各种设计精良的 Nginx 模块（主要由 OpenResty 团队自主开发），从而将 Nginx 有效地变成一个强大的通用 Web 应用平台。这样，Web 开发人员和系统工程师可以使用 Lua 脚本语言调动 Nginx 支持的各种 C 以及 Lua 模块，快速构造出足以胜任 10K 乃至 1000K 以上单机并发连接的高性能 Web 应用系统。

OpenResty 的目标是让你的Web服务直接跑在 Nginx 服务内部，充分利用 Nginx 的非阻塞 I/O 模型，不仅仅对 HTTP 客户端请求,甚至于对远程后端诸如 MySQL、PostgreSQL、Memcached 以及 Redis 等都进行一致的高性能响应。
```

简单点说，  
OpenResty框架将Nginx（nginx.conf programming :)）与Lua programming结合在一起，提供了一个超高并发，扩展性极好的
WEB开发框架。

##安装
正因为log的重要性, 在大多数编程框架中, 都提供了现成的, 方便好用的log工具包.

Java中有commons.logging, log4j等, 

Python中有自带的logging模块.

这些log实现有这样一些共性:

* 自定义log配置文件: 指定log字段的格式, 输出方式, 持久化地址
* 若是写入文件系统, 需要可以指定写入文件最大数目, 并带有回转写入功能
* 足够多的log级别
* log记录不会明显地影响原有业务代码执行效率


##Python中logging的使用
python中的logging模块用起来非常简单,

下面直接给出一段将log存储在本地文件系统的代码demo.

配置文件:
```python
logging_config.py

LOG = {
    'log_format': '[%(asctime)s] [%(filename)s:%(lineno)d] [%(levelname)s] - %(message)s',
    'log_path': '/tmp/test.log',  # log文件地址
    'log_level': logging.DEBUG,  # log级别
    'max_bytes': 10485760,  # log文件尺寸
    'backup_count': 10  # log文件个数
}
logging.basicConfig(format=LOG.get('log_format'), level=LOG.get('log_level'))
formatter = logging.Formatter(LOG.get('log_format'), '%m-%d %H:%M:%S')
logFileRotatingHandler = RotatingFileHandler(LOG.get('log_path'), mode='a',
                                             maxBytes=LOG.get('max_bytes'),
                                             backupCount=LOG.get('backup_count'))
logFileRotatingHandler.setFormatter(formatter)
```

在需要记录log的模块中, 使用如下代码引入logging即可:
```python
logging_test.py

logger = logging.getLogger(__name__)
logger.addHandler(logging_config.logFileRotatingHandler)

if __name__ == '__main__':
    logger.debug('debug log test')
    logger.info('info log test')
    logger.warn('warn log test')
    logger.error('error log test')
    logger.exception('exception log test')  # 主要用于except语句块中,可以自动记录stack trace
```


##log记录要求

* 尽量避免无意义的'begin', 'finished', 'invalid params', 'error happened'等内容
* 对数据进行log记录时, 要记录:数据名称, 数据类型, 数据长度, 数据内容等信息
* 方法进出可以以debug级别打印方法名称+'begin', 方法名称+'finished'
* 异常打印一定要记录异常名称, 异常消息, 异常数据内容以及异常堆栈数据等, 而不是只记录何时何地发生了异常, 这对解决问题帮助很小
* 打印时要注意数据是否为空或者变量是否未定义, 不要让log打印引入bug
* log打印的格式要统一, 最好有二次封装log类供项目内部统一使用, 避免每个人记录log的不同风格和语法, 为查看log带来困难
