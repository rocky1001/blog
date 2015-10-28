Title: 使用Hive操作HBase数据表
Date: 2015-10-15 11:16
Category: work
Tags: hbase, hive
Summary: 介绍在Hive中如何操作(读写)HBase数据库.
Slug: using-hive-on-hbase

对于HBase的操作, 常用的做法有如下几种:  

1. 使用CLI,即在hbase shell命令行中操作hbase数据
2. 使用API,在代码中进行hbase的操作
3. 借助Phoenix(hbase的sql封装层)使用sql对hbase进行查询和操作
4. 借助Hive使用sql对hbase中的表进行查询

关于3和4, 之前有写过blog提到过两者的区别(Hive是基于MR的, 而Phoenix是基于hbase API的),  
这里不再赘述.

这篇blog主要介绍如何使用Hive读取HBase数据.

##基本数据流程

实例的基本数据流程如下:

1. Mapper从HDFS上面读入文本数据
2. 在HBase中进行相应的查询
3. (有需要的话)新增/更新/删除HBase中的数据  

任务比较简单,没有用到Reducer.

因为涉及到稍微复杂点的HBase操作(包括操作大于一个HBase表),  
也就没有用MR输出直接写入HBase库的方案.

##Main输入参数

使用ToolRunner.run方法执行MR时,可以在命令行中传入任意KV参数供代码使用,

这一特性比原始的写法(一个简单main函数的写法)里面,一个个去解析args参数要简单方便的多.

Main代码示例如下:


此时,命令行执行参数如下:


##Mapper的处理

在Mapper的setup方法中建立与HBase的连接(拿到**HBase操作实例**),

在map方法中,完成具体的业务逻辑处理即可.

##HBase的操作

即前面提到的HBase操作实例,是我自己对HBase操作的一个简单封装(异常处理部分还需要优化),  


##HBase的rowkey模糊查询

HBase本身支持filter查询,但是效率不高.

常见的做法是利用HBase的rowkey设置起始和结束key值, 来达到模糊查询的目的.

不过有个限制是:只能使用key的任意**prefix** value, 而不能从中间截取key进行查询.

举例:假设HBase数据表结构和数据为:

|part1_part2_part3|data  |
|-----------------|----  |
|abc_123_321      |value1|
|abc_321_xyz      |value2|
|abc_987_xyz      |value2|
|abc_abc_xyz      |value2|
|abz_921_xyz      |value3|
|xyz_abc_123      |value4|
|123_abc_xyz      |value5|
|...              |...   |

那么我们只能用part1开头的组合(part1_part2, part1_part2_part3等)进行模糊查询,

而不能直接用part2,或part3去查询.

例如:

输入start key=abc_1, end key=abc_9, 可以查出上表中的如下数据:  

|part1_part2_part3|data  |
|-----------------|----  |
|abc_123_321      |value1|
|abc_321_xyz      |value2|
|abc_987_xyz      |value2|

如果想查出所有以"abc"开头的数据,可以输入:  
start key=abc, end key=abc~

**~** 代表ascII中常用字符的最大值.


##参考文档

123


借助HBase操作帮助类, 在Mapper(或是Reducer)中就可以很方便地完成对HBase的所有操作了.