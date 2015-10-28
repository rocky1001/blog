Title: 解决Django读取数据库数据不同步的问题
Date: 2015-10-28 16:36
Category: work
Tags: django, database, phantom reads
Summary: 解决Django读取数据库数据不同步的问题.
Slug: django-database-phantom-reads-problem

在移动端广告WEB管理平台的项目中, 应用了Django框架, 

作为一款"开箱即用"型的框架, Django的功能实在是太强大了,

提供的功能基本涵盖了web开发的方方面面.

这篇blog仅仅分享一下我在使用Django框架中遇到并解决的一个小问题,  
并不会涉及到过多的Django应用的基础知识.


##问题现象

伪代码流程如下:

````
整体流程由两个消息处理流程组成,以下简称为消息A和消息B(这两个消息理论上来说是串行触发的);

消息A的处理:
1. 解析消息体本身;
2. 与数据库交互, 存储消息数主要数据;
3. 操作X字段, 将该字段的状态由初始态设置为"已经收到消息A"的状态;

消息B的处理:
1. 解析消息体本身;
2. 检查X字段, 若将该字段的状态为"已经收到消息A", 则认为可以处理消息B, 流程继续向下; 
   否则认为B消息非法, 直接丢弃;

````

上述为简化的业务消息流程, 但是就在这个看似简单的流程中却出现了奇怪的问题:

在本地测试时, 另外写好了桩代码, 模拟消息A和B的生成动作并发送到上述应用;

明明先发送了消息A, 并检查了数据库状态确实被置为了"已经收到消息A",

但是在发送消息B时, 却时有发生检查数据库发现字段的状态为初始态(也就是没有收到消息A的状态), 导致正常业务流程无法继续往下走.

这个问题也不是每次出现, 而是以较小概率时不时地出现 -- 这种bug才是最让人头疼的.

##问题定位

既然问题不是每次必然出现, 在反复检查和单步调试过自有代码后, 基本可以**排除自有代码本身的问题**;

那么, 剩下的就是django代码中与数据库交互的部分了, 初步估计是django对数据库的缓存之类的问题导致的

(缓存了之前的旧数据, 而下一次消息B处理时使用的是缓存旧数据)

使用的django版本是1.5.4, 使用django mysql confuse result  cache 等等关键字反复组合google之后,

找到了下面这篇文章:

http://www.ewencp.org/blog/django-and-mysql-isolation-levels/

里面提到的问题很类似, 解决方案也很简单.

##问题解决

在django setting 文件中, 修改数据库配置部分, 增加下面init_command的配置:
````
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '##DATABSE_NAME##',
        'USER': '##DATABSE_USER##',
        'PASSWORD': '##DATABSE_PASSWORD##',
        'HOST': '##DATABSE_HOST##',
        'PORT': '3306',
        'OPTIONS' : {
            'init_command': 'SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED'
        },
    }
}

````

增加上述配置后, 问题解决.
