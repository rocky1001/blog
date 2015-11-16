Title: Redis简介和批量操作的性能对比测试
Date: 2015-11-16 16:17
Category: work
Tags: redis, performance, python
Summary: 使用python版本的redis api进行批量操作的性能对比测试和记录.
Slug: redis-intro-and-a-simple-performance-test-for-batch-operations


## 简介
Redis, 内存数据库, 支持高并发操作并具有较好的响应时间,

支持以日志的方式对数据进行持久化.

## 数据结构

Redis提供了五种基础数据结构:

1. key-value
2. key-hashmap(field, value)
3. key-list(value)
4. key-set(unique member)
5. key-sortedset(unique member with score)

其中, hashmap, list, set分别与python中的dict, list, set类型类似.

在这些基础结构之上, 

可以通过使用序列化, JSON化等手段, 衍生出更多的数据结构, 这里就不再赘述了.

## 使用
在使用redis数据库时, 如果遇到需要批量读写数据的场景, 一般推荐使用pipeline这个API.

对于pipeline, 我的理解就是一个**输入和输出的缓冲区**: 

将对redis的多次操作命令先写入这个缓冲区中, 

然后只需要建立一次TCP连接, 就可以批量执行缓冲区中的所有命令;

在拿到执行结果后仍然放回缓冲区, 由调用的地方遍历缓冲区的数据进行查看.

##测试

###环境
redis版本: 2.8.16

redis server: Intel E5-2620@2.00GHz 24 core, 48GB Ram

redis-py版本: 2.10.3

###原始数据

总行数:  246,455 行

###代码

````python
pool = redis.ConnectionPool(host='172.x.x.x', port=6379, db=1)

redis_ins = redis.Redis(connection_pool=pool)
redis_pipe = redis_ins.pipeline()
print redis_ins.dbsize()

origin_list = list()
with open('/temp/246455_lines.txt', 'r') as f:
    for line in f:
        origin_list.append(line.replace('\n', ''))

start_time = time.time()
for data in origin_list:
    # redis_pipe.get(data.split(',')[0])
    redis_ins.get(data.split(',')[0])

# redis_pipe.execute()
end_time = time.time()
print 'Duration:{}'.format(end_time - start_time)
````

###结果

####不使用pipeline,直接get查询

时间长到无法忍受, 在经过10分钟漫长的等待后, 最终不得不kill掉进程...

####使用pipeline,再调用get查询

耗时: 22.121999979秒

####使用pipeline,查看批量查询结果

````python
result = redis_pipe.execute()
for data in result:
    print data
````