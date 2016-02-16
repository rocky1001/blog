Title: Python中记录log的一些实践
Date: 2016-02-04 18:09
Category: work
Tags: python, logging
Summary: 分享Python中logging的应用.
Slug: logging-in-python


这篇文章分享Python logging的一些实践.

##log的意义
凡是有过真正的生产系统开发经验的人, 应该都理解log的意义及其重要性:

在线上系统出现问题时, 有时一行有效的log打印数据, 就能解救人于水火之中.


##log的实现
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
