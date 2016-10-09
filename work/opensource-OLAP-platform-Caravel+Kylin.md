Title: 开源实时OLAP平台之Caravel+Kylin
Date: 2016-06-15 18:20
Category: work
Tags: olap, caravel, kylin
Summary: 开源实时OLAP平台之Caravel+Kylin.
Slug: opensource-OLAP-platform-Caravel+Kylin

最近和好友**[lxw](http://lxw1234.com/archives/2016/06/688.htm "")**一起实践了使用Caravel + Kylin构建的准实时OLAP平台，

经过一段时间的修改和测试，效果非常不错，现在将修改后的代码开源出来，希望有更多的人一起来使用和完善这个方案。

搭建过程和效果的详细说明，也可以参见他的个人博客，地址如下：  
http://lxw1234.com/archives/2016/06/681.htm  
http://lxw1234.com/archives/2016/06/688.htm  

下面对该平台所使用的各个开源项目进行一个简要说明。

##Kylin
Kylin作为底层数据引擎使用，支持对大量数据的SQL查询，并能快速返回结果，是整个平台的核心。

[Kylin官网](http://kylin.apache.org/ "")对安装和使用有详细的介绍，这里不再赘述。

需要特别说明的是，这是Apache顶级项目中第一个由国人发起，并且主要由国人维护的项目。

本次平台搭建使用Kylin 1.5.1版本，没有做任何定制化修改。

##Caravel
Caravel作为数据展示前端使用：Caravel最早作为Druid的前端开发，后来通过SQLAlchemy ORM扩展，  

方便地支持了PostgreSQL, MySQL等传统关系型数据库。

[Caravel官网](http://airbnb.io/caravel/ "")对安装和使用有详细的介绍，这里不再赘述。

因为Caravel并不天然支持Kylin，因此对Caravel有一些小修改（基于0.8.9版本），修改后的代码地址如下：

https://github.com/rocky1001/caravel/tree/caravel-kylin

##PyKylin
PyKylin作为数据库中间件使用。

基于已有的[开源项目](https://github.com/wxiang7/pykylin "")修改：  
原始的项目是一个写给SQLAlchemy的kylin dialect：  
底层通过RESTful API与Kylin交互并且完成数据查询，  
然后将数据查询结果封装后返回给Caravel使用。

平台搭建中，对该项目修改较多，修改后的代码地址如下：

https://github.com/rocky1001/pykylin/tree/caravel-kylin

##使用
上述工具安装配置完毕后，就可以在Caravel的datasource中添加Kylin作为数据源了，db url如下：  
kylin://ADMIN:KYLIN@172.16.212.xxx:xxx/kylin/api?project=kylin_test_prj

在加载了正确的数据后，就可以配置table和slice，并且方便地使用Caravel进行各种美观的图表展示分析了。

##PyHive
借鉴上面PyKylin的ORM，通过安装PyHive中间件，Caravel也可以方便地支持Hive数据源。

如果底层使用Spark-Hive的话，查询效率也还可以接受 :)


##最后

在Kylin的1.5.2版本中，已经支持了从Kafka实时接入数据，然后加载进底层的HBase（大约有5-10分钟的延时），

从而使得准实时的OLAP分析成为可能，这也是本篇文章标题“实时”两个字的底气所在。