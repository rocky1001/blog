Title: redis高级特性
Date: 2016-3-2 18:02
Category: work
Tags: redis, redis-py, advanced features
Summary: 分享redis高级特性的知识.
Slug: redis-advanced-features


之前有文章对redis及其简单应用做过介绍, 

这篇文章分享redis的一些高级特性.

## 基本数据结构

Redis提供了五种基础数据结构:

1. key-value(string,integer,float)
2. key-hashmap(field, value)
3. key-list(value)
4. key-set(unique member)
5. key-sortedset(unique member with score)

除了上述基本结构外，还有对key数据本身的一些操作。

其中, key-value类似于python中的dict; 

key-hashmap/list/set类似于python中的defaultdict(dict/dequeue/set).

sortedset则类似于python中的 dict + sorted(list).

在这些基础结构之上, 可以通过使用序列化, JSON化等手段, 衍生出更多的数据结构, 这里就不再赘述了.


下面看一下每种基础数据结构中的一些中高级应用。

###key-value(string,integer,float)
####append/setrange/getrange
因为有了SETRANGE和GETRANGE 命令，

可以将 Redis 字符串用作具有 O(1) 随机访问时间的线性数组（最可大存储512MB的数据），

这在很多真实用例中都是非常快速且高效的储存方式，具体请参考APPEND 命令的[doc](http://redis.io/commands/append#pattern-time-series "")。

####setbit/getbit/bitcount
每个key支持存储的最大value尺寸为512MB，即2^32（42亿左右）个bit。

可应用于适用于各种bitmap解决问题的场景。

例如：记录每小时的去重活跃用户，并汇总成每天的去重活跃用户。即：

使用zset维护每个用户及其id-分值（先查找，存在则查询出分值；不存在则添加，初始分值为当前已有最大分值+1）

使用分值作为bit值，调用setbit记录当前小时该bit位为1，即为当前小时活跃。

对所有小时的bit-key做or操作（取并集），结果存储入小时汇总bit-key

然后bitcount上述小时汇总bit-key即可。

####构建分布式锁
使用setnx命令，构建一个带有超时自动释放功能的分布式锁。

redis-py中的lock module中，就是使用了该命令设置了锁，代码片段见下：
```python
def do_acquire(self, token):
    if self.redis.setnx(self.name, token):
        if self.timeout:
            # convert to milliseconds
            timeout = int(self.timeout * 1000)
            self.redis.pexpire(self.name, timeout)
        return True
    return False
```

###key-list(dequeue)
####RPOPLPUSH/BRPOPLPUSH实现安全的消息队列：
使用这些命令，不仅返回一个消息，同时还可以将这个消息添加到另一个备份列表当中，

如果一切正常的话，当一个客户端完成某个消息的处理之后，可以用LREM 命令将这个消息从备份表删除。

最后，还可以添加一个客户端专门用于监视备份表，它自动地将超过一定处理时限的消息重新放入队列中去(负责处理该消息的客户端可能已经崩溃)，

这样就不会丢失任何消息了。

例如：实现聊天群组功能，构建三个存储实体：

（1）聊天组（2）用户（3）消息数据

####循环列表
通过使用相同的 key 作为RPOPLPUSH命令的两个参数，

客户端可以用一个接一个地获取列表元素的方式，取得列表的所有元素，

而不必像LRANGE 命令那样一下子将所有列表元素都从服务器传送到客户端中(两种方式的总复杂度都是 O(N))。

####FIFO，优先级和延迟任务队列
使用RPUSH+LPOP实现一个FIFO队列；

*POP命令可以携带多个list名称，从左至右优先级从高到低，实现优先级队列；

使用zset维护所有任务及其执行时间戳（score），并不断检查时间戳来判断任务是否可以被执行，实现延迟任务队列。

###key-set(unique member)
高级应用：
集合的交、并、差的运算

###key-hashmap(field, value)
高级应用：
无

###key-sortedset(unique member with score)
高级应用：
zinterstore，类似于集合的交际运算，同时默认使用sum进行score的聚合（也可以使用min，max）

zunionstore，类似于集合的并集运算

同时，上述多个src集合可以携带weights参数。

应用场景：

对网页访问计数器数据进行简单的统计处理（加总，取平均等）

###pub-sub
在以下两种情况下，有可能会丢失消息，不建议使用。
1. 订阅端读取消息不够快，导致发布端消息积压，使得redis的输出缓冲区被占满，导致redis崩溃；
2. 网络断线时，订阅端会丢失断线期间的所有消息

可以使用key-list实现的消息队列对pub-sub功能进行替代。

###key
####sort
高级应用：

sort uid by non-esist-key get # get user_level_* get user_name_*

不排序，仅使用uid做join，并拿出所有join到的数据。

SORT uid BY user_info_*->level GET user_info_*->name

应用hashmap中的field字段的值进行排序，并取出其他field字段的值。

## 使用pipeline
批量执行命令，有效提高批量命令执行的效率；

pipeline默认调用MULTI/EXEC对批量进行进行包裹。

## 高级特性
###持久化

两种方案：

* RDB 即snapshot，两个方法：
    1. 指定时间段内有指定数量的写操作执行
    2. 调用转储到硬盘的命令
    
    可能丢失上次备份时间点之后的所有数据。
    
* AOF 记录修改命令到append-only file中，日志文件可配置为：
    1. 从不同步
    2. 每秒同步
    3. 每个指令同步

    使用每秒同步时，一般最多丢失2秒内的数据，但是也存在丢失大于2秒数的可能。
    AOF日志也可以调用bgrewriteaof来重写（重新记录当前数据库中的所有数据指令）
    
重启时，若存在AOF，则加载优先级高于RDB。

###主从复制

仅支持单主多从的结构，多个slave server可以分多层设置。

使用[sentinel](http://redis.io/topics/sentinel "")管理器进行主从集群中的：monitor,notify and failover 工作；

redis-py中有单独的sentinel模块，可以完成sentinel工作。


## 其他
###锁
pipeline默认使用transaction, 即multi/exec命令确保所有命令一次执行完毕

但是执行过程中发生任何异常时，**没有rollback功能**；

同时，pipeline可以调用watch/unwatch实现对资源的“乐观锁”  
——不阻止别的客户端对加锁资源的修改，在加锁资源被修改后，当前加锁的客户端会收到watcherror通知，此时可以重试。

watch/unwatch机制不是一种效率很高的加锁方案，因此redis in action中自己实现了：  
acquire_lock_with_timeout/release_lock 方法，可以对redis资源进行加锁。

另外，redis-py中也有单独的lock module给出了锁的实现。

###LUA扩展
可以使用script register 注册lua脚本；

也可以使用eval执行lua脚本并且获得执行结果。
