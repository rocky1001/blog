Title: redis高级特性
Date: 2016-3-2 18:02
Category: work
Tags: redis, redis-py, advanced
Summary: 分享redis高级特性的知识.
Slug: redis-advanced-features


之前有文章对redis及其简单应用做过介绍, 

这篇文章介绍redis的一些高级特性.

## 基本数据结构

Redis提供了五种基础数据结构:

1. key-value(string,integer,float)
2. key-hashmap(field, value)
3. key-list(value)
4. key-set(unique member)
5. key-sortedset(unique member with score)

其中, hashmap, list, set分别与python中的dict, list, set类型类似.

在这些基础结构之上, 可以通过使用序列化, JSON化等手段, 衍生出更多的数据结构, 这里就不再赘述了.

此外，还有对key数据本身的一些操作。

###key-value(string,integer,float)
高级应用：
setrange/getrange

append



因为有了SETRANGE和GETRANGE 命令，

可以将 Redis 字符串用作具有 O(1) 随机访问时间的线性数组（最可大存储512MB的数据），

这在很多真实用例中都是非常快速且高效的储存方式，具体请参考APPEND 命令的[模式：时间序列]部分。

####setbit




###key-list(value)
高级应用：
rpoplpush/brpoplpush

用于实现消息传递和任务队列

####安全的消息队列：
使用RPOPLPUSH 命令 (或者它的阻塞版本BRPOPLPUSH )，

不仅返回一个消息，同时还将这个消息添加到另一个备份列表当中，

如果一切正常的话，当一个客户端完成某个消息的处理之后，可以用LREM 命令将这个消息从备份表删除。

最后，还可以添加一个客户端专门用于监视备份表，它自动地将超过一定处理时限的消息重新放入队列中去(负责处理该消息的客户端可能已经崩溃)，

这样就不会丢失任何消息了。

####循环列表
通过使用相同的 key 作为RPOPLPUSH 命令的两个参数，

客户端可以用一个接一个地获取列表元素的方式，取得列表的所有元素，

而不必像LRANGE 命令那样一下子将所有列表元素都从服务器传送到客户端中(两种方式的总复杂度都是 O(N))。

###key-set(unique member)
高级应用：
集合的交、并、差的运算

###key-hashmap(field, value)
高级应用：
集合的交、并、差的运算

###key-sortedset(unique member with score)
高级应用：
zinterstore，类似于集合的交际运算，同时默认使用sum进行score的聚合（也可以使用min，max）

zunionstore，类似于集合的并集运算

同时，上述src集合可以携带weights参数

###pub-sub
在以下两种情况下，有可能会丢失消息，不建议使用。
1. 订阅端读取消息不够快，导致发布端消息积压，使得redis的输出缓冲区被占满，导致redis崩溃；
2. 网络断线时，订阅端会丢失断线期间的所有消息


###key
####sort
高级应用：

sort uid by non-esist-key get # get user_level_* get user_name_*

不排序，仅使用uid做join，并拿出所有join到的数据。

SORT uid BY user_info_*->level GET user_info_*->name

应用hashmap中的field字段的值进行排序，并取出其他field字段的值。


## 使用（pipeline，scan等）


## 高级特性

###持久化
两种方案：
* 时间点转储，两个方法：
    1. 指定时间段内有指定数量的写操作执行
    2. 调用转储到硬盘的命令
* 记录修改命令到append-only日志中，日志文件可配置为：
    1. 从不同步
    2. 每秒同步
    3. 每个指令同步







###复制

sentinel



###分片





## 其他应用


###锁



###LUA扩展




###总结


