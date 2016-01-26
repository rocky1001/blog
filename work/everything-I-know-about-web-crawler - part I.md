Title: 关于爬虫的那些事 - 第一部分
Date: 2016-01-27 16:30
Category: work
Tags: web crawler, web spider
Summary: 介绍我所理解的网络爬虫.
Slug: everything-I-know-about-web-crawler - part I

之前看到过一个调查, 互联网上爬虫的流量占总流量的多少呢?

在2013年, 这个比例是大于60%, 如下图所示:  
<div class="picture">
![2013年互联网爬虫流量报告]({filename}/images/work/2013-web-spider-traffic-report "2013年互联网爬虫流量报告")  
</div> 

可以看出爬虫流量的比例呈逐渐上升的态势.

这个系列的文章计划分为两篇, 第一部分从定义, 关键技术点上进行介绍;

第二部分则给出一些爬虫的具体实现.

##我所理解的爬虫
###web crawler和web spider的区别

* spider: 以遍历为目的的网络爬虫(可以想象为蜘蛛走在蜘蛛网上), spider会遍历每个URL进行抓取, 同时从抓取到的内容中, 提取新的URL继续抓取, 直到没有新的URL为止
* crawler: 不以遍历为目的的爬虫, 即给出一组URL及其格式, 抓取URL内容, 按照固定格式再次进行URL获取(而不像spider那样获取所有URL), 然后继续抓取URL内容, 直到固定格式的URL不再继续增加为止

###爬虫的定义

* 出于学习, 研究, 应用等目的的, 对公开信息的获取(爬取网易新闻网页, 汽车之家车型文章, 微博数据等)
* 无恶意: 爬虫的频率不影响目标站点的正常运营, 也不会伪造一些曝光或点击数据从而不合规则地获利

##爬虫的关键技术点
###浏览器伪装



###代理IP地址池



###模拟登录/Cookies伪装



###欲速则不达




##一些开源的爬虫框架

* crawler4j(Java)
* scapy(Python)
* pyspider(Python)

##爬虫框架的基本结构

原始输入（种子URL）

生产者：种子URL解析并存储入待爬取列表

消费者：读取待爬取列表URL，完成爬取，并调用生产者的模块，解析新的URL继续存入待爬取列表中

输出爬取结果

