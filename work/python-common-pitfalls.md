Title: Python coding中遇到的一些坑
Date: 2015-12-4 10:35
Category: work
Tags: python, pitfall
Summary: 分享Python coding中遇到的一些坑.
Slug: python-common-pitfalls


这篇合集文章分享Python coding中遇到的一些坑.

##zipfile
zipfile是python自带的zip文件生成包,

这个包的使用非常简单, 可以参考[官方文档](https://docs.python.org/2/library/zipfile.html "zipfile").

可是在使用这个包生成zip文件时却遇到了一个坑:

这个包提供了ZipFile对象用于打开, 读取, 写入zip文件, 

其中, 写入zip文件的方法有两个:

1. write方法: 传入待压缩文件路径参数(带文件名), 可以把已经存在的文件写入zip file
2. writestr方法: 传入字符串参数, 可以将内存中的字符串数据写入zip file

问题就出在第二个方法里面. 

在应用时, 为了提高效率, 想直接把大量的数据流分批写入zip file, 例如:
````python
zf = zipfile.ZipFile(file_to_write, mode='w', compression=zipfile.ZIP_DEFLATED)
try:
    for data in data_to_write:
        zf.writestr(basename(file_to_write), data.encode('utf-8'))
finally:
    zf.close()
````
但是上面这种用法, 却完全行不通!

因为这个方法**仅支持将完整的数据全文, 一次性写入zip file**, 

想要以ZipFile先open file, 再通过多次调用writestr方法写入不同数据内容的尝试最终失败了, 

这样只会在zip file里面重复生成多个**同名**的原始数据文件而已...

最后只能把所有待写入的数据全部拼起来后, 调用writestr方法一次性写入.

##datetime
datetime是用来处理日期, 时间, 时间间隔(timedelta)的包, 

其中对于日期和时间的处理, 比较常用的是datetime包中的datetime类.

使用中遇到的问题是, 在代码最开始处: 
````python
from datetime import datetime 
````
有时会无效! 

下面的代码在使用时, 会提示找不到datetime这个包.

最后的解决办法是, 仅在代码头部做这样的引用:
````python
import datetime 
````

使用时一律使用完整路径, 例如:
````python
datetime.datetime.now()
````

该问题的触发原因不明, 也并不是经常出现.


