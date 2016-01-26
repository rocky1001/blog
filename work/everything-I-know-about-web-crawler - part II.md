Title: 关于爬虫的那些事 - 第一部分
Date: 2016-01-27 16:30
Category: work
Tags: web crawler, web spider
Summary: 介绍我所理解的网络爬虫.
Slug: everything-I-know-about-web-crawler - part II

这个系列的文章计划分为两篇, 本篇是第二部分：给出一些爬虫的具体实现.

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


