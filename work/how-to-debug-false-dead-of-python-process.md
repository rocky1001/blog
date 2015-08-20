Title: Python进程假死如何debug
Date: 2015-08-19 16:30
Category: Work
Tags: python, false dead, debug
Summary: linux下面使用python编写的一个service挂死了,进程写入的日志文件不更新,所有发到该进程的消息都没有响应,这时该如何debug?

今天遇到一个问题，linux下面使用python编写的一个service挂死了,  
进程写入的日志文件不更新，所有发到该进程的消息都没有响应。

###这时该如何debug？

下面简单描述下，抛砖引玉：

##使用python -m trace模块进行debug
用法：python -m trace --trace python_file_path  
参考：https://docs.python.org/2/library/trace.html

通过这种方式，发现进程挂死在了socket recv的代码里面，有可能是由于网络连接不稳定导致的。  
但是，现在问题就来了，以后再遇到这种情况，如何及时发现并且自动恢复呢？

##使用gdb
用法：gdb python python_process_pid  
参考：https://wiki.python.org/moin/DebuggingWithGdb

进到gdb命令行后，继续敲bt ，看能否找到程序挂死的地方。  
因为我个人对gdb不是很熟悉，所以就没有继续尝试了。