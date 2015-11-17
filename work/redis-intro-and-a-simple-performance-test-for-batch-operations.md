Title: Redis简介和批量操作的性能对比测试
Date: 2015-11-16 16:17
Category: work
Tags: redis, pipeline, get, scan, performance, python
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

另外, 在redis 2.8.0版本中, 新增了SCAN命令, 可以按照指定数目(也可以指定key符合的pattern), 遍历查询所有key,

对于scan, 应该是之前KEYS命令的一个生产环境可用版本, 

因为keys命令(可以带通配符*进行模糊key查询)返回的是所有key的列表, 

在返回的列表极大时, 有可能会造成redis server响应延迟, 因此不建议在生产环境使用,

现在有了scan后, 就可以很方便地遍历整库数据了.

##测试

###测试环境
redis版本: 2.8.16

redis server: Intel E5-2620@2.00GHz 24 core, 48GB Ram

redis-py版本: 2.10.3

###get测试代码

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

###get测试结果

不使用pipeline:  
时间长到无法忍受, 在经过10分钟漫长的等待后, 最终不得不kill掉进程...

使用pipeline:  
scan查询总行数: 246,455 行
Duration:22.121999979 秒

###使用pipeline,查看批量查询结果代码

````python
result = redis_pipe.execute()
for data in result:
    print data
````

###scan测试代码

````python
def scan_by_instance(_redis_ins, _count=1000):
    start_time = time.time()
    start_index = 0
    
    new_index, scan_result_l = _redis_ins.scan(cursor=start_index, count=_count)
    # print new_index, scan_result_l
    while new_index != start_index:
        new_index, scan_result_l = _redis_ins.scan(cursor=new_index, count=_count)
        # print new_index, scan_result_l

    end_time = time.time()
    print 'Duration:{}'.format(end_time - start_time)
    
    
def scan_by_pipe(_redis_pipe, _count=1000):
    start_time = time.time()
    start_index = 0

    _redis_pipe.scan(cursor=start_index, count=_count)
    # pipeline.execute will return a list, so we need index 0 to get the real result
    new_index, scan_result_l = _redis_pipe.execute()[0]
    # print new_index, scan_result_l
    while new_index != start_index:
        _redis_pipe.scan(cursor=new_index, count=_count)
        new_index, scan_result_l = _redis_pipe.execute()[0]
        print new_index, scan_result_l

    end_time = time.time()
    print 'Duration:{}'.format(end_time - start_time)
````

###scan测试结果

|数据总行数(行)|每次返回(条)|不使用pipeline, 花费时间(秒)|使用pipeline, 花费时间(秒)|
|----:|----:|----:|----:|
|484,074|1,000|25.015|24.137|
|2,253,861|1,000|178.357|185.082|
|2,253,861|10,000|164.241|175.772|
|2,253,861|50,000|163.962|163.033|
|2,253,861|100,000|203.056|288.501|

###总结

* 使用get进行批量操作时, 一定要在pipeline之下进行

* 使用scan进行数据库遍历时, pipeline对效率提升非常有限,   
在上面的测试中, 数据量较大的情况下, 使用pipeline反而会稍慢一点

* scan中一次性获取的数据并不是越多越好
