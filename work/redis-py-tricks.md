Title: redis-py使用中的一点小窍门
Date: 2015-12-2 18:22
Category: work
Tags: redis, redis-py, tricks
Summary: 分享redis-py使用中的一点小窍门.
Slug: redis-py-tricks


之前有文章对redis及其简单应用做过介绍, 

这篇合集文章介绍使用redis和redis-py包时收集整理的一点小技巧.

##scan和scan_iter

从2.8.0版本起, Redis提供了SCAN命令对db中的所有key进行迭代, 

该命令:  
需要输入迭代起始参数  
可选输入过滤参数(可实现类似于KEYS(*)中的 * 这样的模糊查询)  
可选输入COUNT参数, 指定一次查询返回的key的数量

稍微有点麻烦的是迭代起始参数:  
先要指定一个起始值, 例如0,  
每次调用会返回一个新的迭代序号, 以及本次查询结果数据,  
下一次迭代需要输入上次迭代返回的序号, 直到迭代的返回序号等于起始值时, 完成所有key的遍历.

redis-py中提供了scan_iter这个方法可以让使用者不用关心迭代序列号, 只关心返回的数据即可.

这个方法的源码如下:
````python
def scan_iter(self, match=None, count=None):
        """
        Make an iterator using the SCAN command so that the client doesn't
        need to remember the cursor position.

        ``match`` allows for filtering the keys by pattern

        ``count`` allows for hint the minimum number of returns
        """
        cursor = '0'
        while cursor != 0:
            cursor, data = self.scan(cursor=cursor, match=match, count=count)
            for item in data:
                yield item
````

在实际使用时, 发现scan_iter中, 输入的count参数是无效的.

从上面的代码可以看出, scan请求虽然指定了count数目, 但是scan_iter这个迭代器每次都固定返回一个数据, 

造成scan_iter应用时count参数失效的效果.

可以对上述代码进行下简单的修改, 直接返回data数组, 使得count参数生效, 修改后的代码如下:
````python
def _scan_iter(_redis_ins, match=None, count=None):
    cursor = '0'
    while cursor != 0:
        cursor, data = _redis_ins.scan(cursor=cursor, match=match, count=count)
        yield data
````

