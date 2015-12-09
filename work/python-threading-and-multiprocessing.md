Title: Python中的多线程与多进程
Date: 2015-12-9 13:14
Category: work
Tags: python, threading, multiprocessing
Summary: Python中多线程与多进程的应用与问题.
Slug: python-threading-and-multiprocessing

多线程(thread)和多进程(process), 这是几乎所有编程语言中都绕不开的话题, 

本文将对Python(2.6 and 2.7.x)中的多线程和多进程做一综述, 并分享一些我在应用中遇到的问题和解决方案.

首先, 列出几篇参考文档,

如果看完了下面这些文档, 在应用多线程或多进程时, 还是有问题, 那么不妨继续往下看.

##参考文档
多线程相关(threading模块对thread模块进行了封装, 应用中多使用threading模块)

[threading – Manage concurrent threads](https://pymotw.com/2/threading/#module-threading "")

[Python threads synchronization: Locks, RLocks, Semaphores, Conditions, Events and Queues](http://www.laurentluce.com/posts/python-threads-synchronization-locks-rlocks-semaphores-conditions-events-and-queues/ "")

[Python线程指南](http://www.cnblogs.com/huxi/archive/2010/06/26/1765808.html "Python线程指南")

多进程相关

[multiprocessing – Manage processes like threads](https://pymotw.com/2/multiprocessing/index.html#module-multiprocessing "")

[Python多进程编程](http://python.jobbole.com/82045/ "")

##多线程与多进程的优劣
多线程与多进程各自的优势与劣势在哪里?

SO上面的[一个答案](http://stackoverflow.com/a/3046201 "")对此有很好的总结, 翻译如下:

|   |Multiprocessing|Threading|
|---|---------------|---------|
|优点|1. 独立的内存空间<br/> 2. 充分利用多核(多个)CPU<br/> 3. 避免了CPython解释器中的GIL限制<br/> 4. 使用进程间通信IPC模型, 避免了同步问题(除非使用共享内存)<br/> 5. 代码通常相对简单<br/> 6. 子进程可以被中断或杀死<br/> 7. CPU密集型任务的首选(CPython解释器下)|1. 轻量, 占用较少的内存<br/> 2. 使用共享内存模型通信, 可以方便地获取线程内的数据或状态<br/> 3. 使用Jython, IronPython等解释器时, 没有GIL限制 <br/> 4. IO密集型任务的首选<br/>|
|缺点|1. 进程间通信IPC模型相对共享内存方式较为复杂<br/> 2. 占用较多的内存|1. 在CPython解释器中受到GIL的限制<br/> 2. 线程不可中断或杀死<br/> 3. 如果不使用线程安全的队列/消息模型(例如Queue模型), 则需要自行处理同步等问题(例如加锁,及加锁的粒度等)<br/> 4. 存在线程安全问题, 代码中对共享部分的处理要非常小心|


简而言之, **IO密集型任务使用多线程, CPU密集型任务使用多进程**.

上面列表中反复提到的GIL(Global Interpreter Lock)是CPython解释器中特有的[限制](https://wiki.python.org/moin/GlobalInterpreterLock "GlobalInterpreterLock"):

因为CPyhton的内存管理模型不是线程安全的, GIL作为一个全局锁, 保证同一时刻仅有一个线程在执行(也可参见[wikipedia](https://zh.wikipedia.org/wiki/GIL "wiki/GIL")).

在GIL之下(使用CPU单核, 无法有效利用多核), 单个python进程中:
* 无法并行(parallel)地执行多个线程, 
* 只能并发(concurrently)地执行多个线程(等待IO操作期间切换上下文, 使得CPU单核的效率最大化)

想要并行(parallel)处理只能使用多进程.

##多线程与多进程的使用
最开始给出的参考文档中, 对多进程和多线程的基本使用已经有了详细的介绍, 这里不再赘述.

比较有趣的是, multiprocessing中提供了一个[dummy module](https://docs.python.org/2/library/multiprocessing.html#module-multiprocessing.dummy ""), 以multiprocessing API的方式提供了对threading模块的封装, 

这就意味着使用如下代码时:
````python
from multiprocessing.dummy import Pool, Process
````

Pool和Process的底层其实都是使用threading的实现(即ThreadPool和Thread),

这时, 如果我们将import中的dummy module删掉:
````python
from multiprocessing import Pool, Process
````
 
应用没有做任何修改, 就直接切换成multiprocessing实现了.

上述代码实现了**多线程和多进程对外API的统一**, 

下面的常用方法说明中, 将不再区分是多线程的API还是多进程的API, 而是进行统一的说明.


##常用方法与问题

###pool.map
pool提供了map方法(类似于buildin中的map), 可以传入function和iterator, 

并对iterator中的所有数据执行function(当然是多线程或多进程的执行方式), 并获取function的返回值(若存在).

同时, pool还提供了map_async方法, 与上面map方法的区别是:
* map是阻塞的, 会一直等到iterator中的所有数据执行完毕才会继续往下运行
* map_async是非阻塞的, 在需要获取结果的地方执行pool.join()后, 才会阻塞等待执行完毕

####如何给function传入多个参数?  
有两个解决办法:

如果其中一个或多个参数固定, 则可以使用functools.partial来传入固定参数, 使得可变参数只有一个;

使用zip将多个参数打包为元组(还需要用到itertools.repeat), function的参数签名也写为元组, 传入后直接使用即可.

此外在python3.3中, 提供了[Pool.starmap()](https://docs.python.org/dev/library/multiprocessing.html#multiprocessing.pool.Pool.starmap "")方法, 可以直接传入元组参数列表

####给map传入Queue这样的队列可以吗?
不行, 因为Queue不是可迭代的对象.

Queue作为不同进程(或是线程)间通信的重要方式, 

居然无法应用在map中, 这是很让人沮丧的一件事. But it is life, right? :)

###Queue
以生产者-消费者模型为例, Queue作为队列, 沟通了生产者和消费者.

生产者调用Queue.put()方法放入待处理数据;  
消费者调用Queue.get()方法处理队列中的数据.

####生产者-消费者如何结束?
因为Queue.get()方法默认是阻塞的, 当队列中数据为空时, 消费者会进入无限等待.

假如生产者只生产有限的数据, 而我们期望消费者处理完毕后结束整个流程, 此时就需要杀死消费者.

有两种办法:

下毒药: 在Queue中加入毒药片(poison pill), 消费者对从Queue中拿出的数据进行判断, 如果是毒药就终止处理;
这种方法的缺点是, 有多少个消费者进程, 就需要在Queue中放入对应数量的毒药片.

设置超时: 调用Queue.get(timeout=xxx), 其中xxx设置为等待时间, 当队列为空, 等待相应的时间后会抛出Empty异常, 捕捉到该异常后消费者退出.

###Lock
Lock对象提供了acquire()和release()方法, 

在使用非线程安全的资源时(例如文件句柄等), 

需要在使用前对资源及其操作加锁, 并在使用后释放锁, 使得其他进程/线程可以使用该资源.

##多线程与多进程的简单性能测试


