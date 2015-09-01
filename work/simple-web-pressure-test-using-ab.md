Title: 使用ab进行简单的压力测试
Date: 2015-08-20 09:21
Category: work
Tags: ab, pressure test, web
Summary: 介绍如何使用ab进行简单的web压力测试.
Slug: simple-web-pressure-test-using-ab

apache ab工具的使用教程在网上一搜一大把，因此使用该工具时，其参数的详细解释和用法就不在这里罗嗦了。

这篇文章主要分享了我个人在近期开发和测试中，使用ab工具遇到的问题和一些心得体会。希望对大家有帮助。

apache ab工具是apache服务器自带的静态web地址压力测试工具(这里为什么要强调静态？稍后详解).  
这里使用的是从网上下到的ab工具的windows版本(ab.exe 2.2.21.0),下载后可以直接在windows环境上面运行，非常方便。

##使用ab工具进行web压力测试(GET):

###适用于

测试类似这样：

http://192.168.80.210:8080/webcrawler/

或者这样：

http://192.168.80.210:8080/webcrawler/jsp/microBlogView.jsp

的页面。

###用法
ab.exe -c 1 -n 1 http://xxx

-c 每秒的并发数  
-n 连接总数

##使用ab工具进行web压力测试(POST):
(需要post参数，适用于需要填写form表单参数的页面)

###适用于
测试类似这样：


http://192.168.80.210:8080/webcrawler/MicroBlogServlet?jsoncallback=test&type=test&uid=3815126290742065170&count=20

的页面——即携带url参数的页面

###用法
ab.exe -c 1 -n 1 -T "application/x-www-form-urlencoded" -p post.txt http://xxx

post.txt的样式：

p1=xxx&p2=yyy&p3=zzz

例如：jsoncallback=test&type=test&uid=123456789&count=20

以上是两种最常用测试类型下,ab的基本用法。

##使用中遇到的问题：
在测试完成后，显示结果的页面，有如下显示

Failed requests: 99 (Connect: 0, Length: 99, Exceptions: 0)

为什么会有失败的请求？首先看下失败类型的含义：

Connect：无法发送请求，目标主机连接失败，要求的过程中链路中断  
Length：回应的内容长度不一致(以 Content-Length 头为判断依据)  
Exception：发生无法预期的错误

因为ab是一款**静态**页面测试工具，要求批量测试中，每次response返回值相同，

假如我们使用ab测试具有动态返回结果的页面，如果两次request得到的response不同，就会记录上面这样的一次失败。

因此在测试动态返回结果的页面时，上述错误类型可以忽略。