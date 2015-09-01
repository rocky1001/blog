Title: 监测VPS的运行状态
Date: 2015-09-01 09:45
Category: VPS
Tags: vps, status, monitor
Summary: 监测VPS的运行状态(CPU,内存,系统负载等等).
Slug: monitor-vps-running-status

##前言

因为是乞丐版的vps(1 core, 512 RAM, 20GB SSD), 而运行的应用又稍多一点(其实也还好了: 一个blog,两个web app),

对vps运行状态的监控就要提上日程了.

下面先讨论如何做好单步监控,再考虑写到脚本中定期执行,并将记录数据写入数据库,  
最终可以在web app的图形界面上面查看监控数据(以直观的图表的形式),  
并在监控数据超出阈值时给出告警(邮件)通知.

上述描述的实现其实就是一个mini的linux通用监控平台的原型.

##监控参数

监控的主要参数有如下一些(在尽量不安装第三方工具的基础上进行):  

* cpu
* 内存
* 硬盘
* 系统负载
* 系统io
* 网络连接

##使用命令

详细用法可以查看man page.

以下仅摘录常用的命令或参数.

###top
查看系统启动时间, 当前用户数, 系统负载

正在运行的任务数

CPU使用情况

MEM使用情况

````
top - 09:55:53 up 13 days, 17:21,  2 users,  load average: 0.00, 0.01, 0.05
Tasks:  83 total,   2 running,  81 sleeping,   0 stopped,   0 zombie
%Cpu(s):  0.3 us,  0.0 sy,  0.0 ni,99.7 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
KiB Mem:    501808 total,   442648 used,    59160 free,    55696 buffers
KiB Swap:  1048572 total,    11828 used,  1036744 free.   198784 cached Mem

  PID USER      PR  NI    VIRT    RES    SHR S %CPU %MEM     TIME+ COMMAND                                                                                                                   
 xxxx xxxx      20   0  891068  42188   1348 S  0.0  8.4   x:xx.xx xxxx
1xxxx xxxx      20   0  160828  27580   2204 S  0.0  5.5   x:xx.xx xxxx                                                                                         
1xxxx xxxx      20   0   64896  14396   1796 S  0.0  2.9   x:xx.xx xxxx                                                                                                                  
 xxxx xxxx      20   0   56148  12104   2764 S  0.0  2.4   x:xx.xx xxxx
2xxxx xxxx      20   0  728144  11292   2820 S  0.0  2.3   x:xx.xx xxxx                                                                                                           
 xxxx xxxx      20   0   57012   5688   1600 S  0.0  1.1   x:xx.xx xxxx
2xxxx xxxx      20   0   23428   4684   1816 S  0.0  0.9   x:xx.xx xxxx                                                                                                                      
2xxxx xxxx      20   0   23348   4496   1716 S  0.0  0.9   x:xx.xx xxxx                                                                                                                      
2xxxx xxxx      20   0  105632   4364   3296 S  0.0  0.9   x:xx.xx xxxx
 xxxx xxxx      20   0   35164   3812   2496 S  0.0  0.8   x:xx.xx xxxx
2xxxx xxxx      20   0  100712   2788    872 S  0.0  0.6   x:xx.xx xxxx
2xxxx xxxx      20   0   87744   2692    996 S  0.0  0.5   0:00.36 xxxx
1xxxx xxxx      20   0   87744   2664   1212 S  0.0  0.5   0:00.03 xxxx
 xxxx xxxx      20   0   33464   2380   1228 S  0.0  0.5   x:xx.xx xxxx                                                                                                                      
 xxxx xxxx      20   0  255840   2184    912 S  0.0  0.4   x:xx.xx xxxx
 xxxx xxxx      20   0   61364   1732   1592 S  0.0  0.3   0:00.06 xxxx
2xxxx xxxx      20   0   21964   1580   1148 R  0.3  0.3   x:xx.xx xxxx                                                                                                                       
 xxxx xxxx      20   0   43448   1476   1308 S  0.0  0.3   0:00.14 xxxx                                                                                                            
 xxxx xxxx      20   0   39224   1040    848 S  0.0  0.2   0:00.22 xxxx                                                                                                               
 xxxx xxxx      20   0   23652    936    768 S  0.0  0.2   x:xx.xx xxxx
````

可见:

系统已经运行了13天; 当前有两个用户登录; 1分钟,5分钟和15分钟的CPU平均负载分别是0.00, 0.01, 0.05;

(关于load average,可以参见[这篇文章](http://blog.scoutapp.com/articles/2009/07/31/understanding-load-averages "understanding-load-averages")的介绍,这里是[中文翻译版本](http://os.51cto.com/art/200911/164410.htm "中文翻译版本").)

当前系统中有83个进程在运行;

Cpu运行状态: 用户进程（user）占用CPU的0.3%，系统进程（system）占用CPU的0.0%，用户进程没有改变过优先级的进程，所以user nice值为0.0%，99.7%的CPU处于空闲状态（idle）,没有等待的输入输出，所以iowait的值也为0.0%，硬件请求终端时间（hardware interrupt）占CPU的0.0%，软终端请求时间占CPU的0.0%;

内存总量为501808k，已使用的内存总量为442648k，59160k为空闲内存总量，55696k用作内核缓存的内存总量  
(系统总的空闲内存数量=top的free mem + top的cached mem);

交换分区总量为1048572k，使用的交换分区总量为11828k，空闲交换分区总量为1036744k，198784k为内存缓冲区用量（cached）;

执行top后, 可以继续输入如下一些命令:

* 1(数字one,不是小写英文字母L) 显示多核CPU(若有)的使用情况
* M 按照内存占用量由多到少排序(上例中的打印就是执行了M命令的结果)
* P 按照CPU占用量由多到少排序
* W 将当前设置写入~/.toprc文件中(这是写top配置文件的推荐方法)
* k 终止一个进程(默认发送信号15,如果不能结束会发送信号9强制杀掉进程)
* L 输入进程名称进行查找


###free
查看内存使用和剩余情况

通常用法free -h or free -m, 以MB为单位显示内存数字.

下面是我的虚拟机上面的执行结果:
````
             total       used       free     shared    buffers     cached
Mem:          490M       429M        60M       416K        56M       188M
-/+ buffers/cache:       185M       304M
Swap:         1.0G        11M       1.0G
````

初看free内存很少,

其实当前系统的剩余内存应该=free+cached,即60+304=360MB, 剩余内存还是很多的.


###df
查看内存使用和剩余情况

通常用法df -h or df -m, 以MB为单位显示内存数字.

下面是我的虚拟机上面的执行结果:
````
Filesystem      Size  Used Avail Use% Mounted on
/dev/vda1        20G  xxxG   xxG  xx% /
none            xxxK    xx  xxxK   x% /sys/xxx
udev            xxxM  xxxK  xxxM   x% /xxx
tmpfs            xxM  xxxK   xxM   x% /xxx
none            xxxM    xx  xxxM   x% /xxx/xxx
none            xxxM    xx  xxxM   x% /xxx/xxx
none            xxxM    xx  xxxM   x% /xxx/xxx
````


###vmstat
查看当前系统内存情况, 交换分区负载, io负载, 系统负载和CPU负载情况.

通常用法vmstat 3, 以3秒为时间间隔采集数据并进行展示.

下面是我的虚拟机上面的执行结果:
````
procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
 2  0  11828  61560  57996 192644    0    0     5     5   19   13  0  0 100  0  0
 0  0  11828  61552  57996 192644    0    0     0     0   22   58  0  0 100  0  0
 0  0  11828  61552  57996 192644    0    0     0     0   24   63  0  0 100  0  0
 0  0  11828  61552  57996 192644    0    0     0     0   34   74  0  0 100  0  0
````
参数详解参见[这里](http://www.ahlinux.com/start/cmd/22809.html "vmstat description")的内容,为了避免链接失效,摘录如下:

````
参数详解
Linux 内存监控vmstat命令输出分成六个部分:

1. 进程procs：
 
  r：在运行队列中等待的进程数 。
  b：在等待io的进程数 。
  
2. Linux 内存监控内存memoy： 

  swpd：现时可用的交换内存（单位KB）。 
  free：空闲的内存（单位KB）。
  buff: 缓冲去中的内存数（单位：KB）。
  cache：被用来做为高速缓存的内存数（单位：KB）。
  
3. Linux 内存监控swap交换页面 

  si: 从磁盘交换到内存的交换页数量，单位：KB/秒。
  so: 从内存交换到磁盘的交换页数量，单位：KB/秒。
  
4. Linux 内存监控 io块设备:

  bi: 发送到块设备的块数，单位：块/秒。
  bo: 从块设备接收到的块数，单位：块/秒。
  
5. in: 每秒的中断数，包括时钟中断。
  cs: 每秒的环境（上下文）转换次数。
  
6. Linux 内存监控cpu中央处理器：

  cs：用户进程使用的时间 。以百分比表示。
  sy：系统进程使用的时间。 以百分比表示。
  id：中央处理器的空闲时间 。以百分比表示。
  
常见诊断：

1. 假如 r 经常大于4 ，且 id 经常小于40，表示中央处理器的负荷很重。

2. 假如 bi，bo 长期不等于0，表示物理内存容量太小。

每个参数的具体意思如下：

r表示运行队列(就是说多少个进程真的分配到CPU)，我测试的服务器目前CPU比较空闲，没什么程序在跑，当这个值超过了CPU数目，就会出现CPU瓶 颈 了。这个也和top的负载有关系，一般负载超过了3就比较高，超过了5就高，超过了10就不正常了，服务器的状态很危险。top的负载类似每秒的运行队 列。如果运行队列过大，表示你的CPU很繁忙，一般会造成CPU使用率很高。

b表示阻塞的进程,这个不多说，进程阻塞，大家懂的。

swpd虚拟内存已使用的大小，如果大于0，表示你的机器物理内存不足了，如果不是程序内存泄露的原因，那么你该升级内存了或者把耗内存的任务迁移到其他机器。

free空闲的物理内存的大小，我的机器内存总共8G，剩余3415M。

buffLinux/Unix系统是用来存储，目录里面有什么内容，权限等的缓存，我本机大概占用300多M

cachecache直接用来记忆我们打开的文件,给文件做缓冲，我本机大概占用300多M(这里是Linux/Unix的聪明之处，把空闲的物理内存的 一部分拿来做文件和目录的缓存，是为了提高 程序执行的性能，当程序使用内存时，buffer/cached会很快地被使用。)

si每秒从磁盘读入虚拟内存的大小，如果这个值大于0，表示物理内存不够用或者内存泄露了，要查找耗内存进程解决掉。我的机器内存充裕，一切正常。

so每秒虚拟内存写入磁盘的大小，如果这个值大于0，同上。

bi块设备每秒接收的块数量，这里的块设备是指系统上所有的磁盘和其他块设备，默认块大小是1024byte，我本机上没什么IO操作，所以一直是0，但是我曾在处理拷贝大量数据(2-3T)的机器上看过可以达到140000/s，磁盘写入速度差不多140M每秒

bo块设备每秒发送的块数量，例如我们读取文件，bo就要大于0。bi和bo一般都要接近0，不然就是IO过于频繁，需要调整。

in每秒CPU的中断次数，包括时间中断

cs每秒上下文切换次数，例如我们调用系统函数，就要进行上下文切换，线程的切换，也要进程上下文切换，这个值要越小越好，太大了，要考虑调低线程或者进 程的 数目,例如在apache和nginx这种web服务器中，我们一般做性能测试时会进行几千并发甚至几万并发的测试，选择web服务器的进程可以由进程或 者线程的峰值一直下调，压测，直到cs到一个比较小的值，这个进程和线程数就是比较合适的值了。系统调用也是，每次调用系统函数，我们的代码就会进入内核 空间，导致上下文切换，这个是很耗资源，也要尽量避免频繁调用系统函数。上下文切换次数过多表示你的CPU大部分浪费在上下文切换，导致CPU干正经事的 时间少了，CPU没有充分利用，是不可取的。

us用户CPU时间，我曾经在一个做加密解密很频繁的服务器上，可以看到us接近100,r运行队列达到80(机器在做压力测试，性能表现不佳)。

sy系统CPU时间，如果太高，表示系统调用时间长，例如是IO操作频繁。

id空闲 CPU时间，一般来说，id + us + sy = 100,一般我认为id是空闲CPU使用率，us是用户CPU使用率，sy是系统CPU使用率。

wt等待IO CPU时间。
````


####iostat
查看系统io使用情况

通常用法iostat -m -x 1 1000

下面是我的虚拟机上面的执行结果:
````
Linux 3.13.0-37-generic (xxxxx)         09/01/15        _x86_64_        (1 CPU)

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           0.13    0.01    0.04    0.02    0.00   99.80

Device:         rrqm/s   wrqm/s     r/s     w/s    rMB/s    wMB/s avgrq-sz avgqu-sz   await r_await w_await  svctm  %util
vda               0.00     0.24    0.23    0.32     0.00     0.00    33.88     0.00    1.54    0.33    2.41   0.25   0.01

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           0.00    0.00    0.00    0.00    0.00  100.00

Device:         rrqm/s   wrqm/s     r/s     w/s    rMB/s    wMB/s avgrq-sz avgqu-sz   await r_await w_await  svctm  %util
vda               0.00     0.00    0.00    1.01     0.00     0.00     8.00     0.00    0.00    0.00    0.00   0.00   0.00
````

观察avg-cpu中的iowait数据,如果值较大,则说明io是当前系统的瓶颈,

另外两个比较重要的参数是:
````
avgqu-sz : The average queue length of the requests that were issued to the device. (磁盘队列的请求长度，正常的话2,3比较好。可以和cpu的load一样的理解)
await : The average time (in milliseconds) for I/O requests issued to the device to be served. (代表一个I/O操作从wait到完成的总时间)
````


###netstat
查看系统网络连接使况

通常用法netstat -natp或是netstat -an

下面是我的虚拟机上面的执行结果:
````
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 127.0.0.1:xx            0.0.0.0:*               LISTEN      xxxxx/xxxxxx  : MTA   
tcp        0      0 127.0.0.1:xx            0.0.0.0:*               LISTEN      xxxx/xxxxxx     
tcp        0      0 127.0.0.1:xx            0.0.0.0:*               LISTEN      xxxxx/xxxxxx  : MTA    
tcp        0      0 104.236.172.6:xxxxx     xxxxxxxxxxx:xxxxx       ESTABLISHED xxxx/xxxxxx     
tcp        0      0 104.236.172.6:xxxxx     xxxxxxxxxxx:xxxxx       ESTABLISHED xxxx/xxxxxx     
tcp        0      0 104.236.172.6:xxxxx     xxxxxxxxxxx:xxxxx       ESTABLISHED xxxx/xxxxxx     
tcp        0      0 104.236.172.6:xxxxx     xxxxxxxxxxx:xxxxx       ESTABLISHED xxxx/xxxxxx     
tcp        0      0 104.236.172.6:xxxxx     xxxxxxxxxxx:xxxxx       TIME_WAIT   -               
tcp        0      0 104.236.172.6:xxxxx     xxxxxxxxxxx:xxxxx       ESTABLISHED xxxx/xxxxxx     
tcp        0      0 104.236.172.6:xxxxx     xxxxxxxxxxx:xxxxx       ESTABLISHED xxxx/xxxxxx     
tcp        0      0 104.236.172.6:xxxxx     xxxxxxxxxxx:xxxxx       ESTABLISHED xxxx/xxxxxx     
tcp        0    404 104.236.172.6:xxxxx     xxxxxxxxxxx:xxxxx       ESTABLISHED xxxxx/xxxxx            
````