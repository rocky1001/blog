Title: 网页正文内容提取工具概述
Date: 2015-08-19 16:52
Category: Work
Tags: text extraction, tools, python, java
Summary: 现在需要将一些网页中的正文内容提取出来。即，将URL对应的HTML源码中的“正文内容”剥离出来。首先想到的，就是找一找有没有现成的网页正文内容提取工具。

##有哪些

这是quora上面的[一个问题](http://www.quora.com/Whats-the-best-method-to-extract-article-text-from-HTML-documents "")。

这是微博上面讨论形成的一个[资源链接](http://www.zhizhihu.com/html/y2013/4202.html "")。

为了防止上述链接失效，将主要内容摘录于下（版权归上述链接正文内容作者所有）：

````
@西瓜大丸子汤

总结我用过的网页正文抽取工具： decruft http://t.cn/S7bVEC python-readabilityhttp://t.cn/zYeoZ8b boilerpipe http://t.cn/h41EEs python-boilerpipehttp://t.cn/zYeoyPw pismo http://t.cn/zYeoyP2 Goose http://t.cn/zYeoZ8G Python Goose http://t.cn/zYeoZ8q

@丕子 :有个测试链接：http://jimplush.com/blog/goose 测试了个链接，goose没提出来，cx-ectractor提出来了；不过goose的metadata以及image等不错；谁有空写个吧，两者优点结合一下。

@52nlp: 转cx-ectractor(http://t.cn/hDO2xf )的维护者 @陈鑫Shin @王利锋Fandy //@陈阿荣: cx-extractor //@马少平THU: 这个确实有难度，我们也没有什么好方法。@王利锋Fandy: 在我的硕士论文中给出了形式化数学表示，详细请见：http://t.cn/zYeAJSc，希望对大家有帮助

木子海波：自吹自擂一下。http://blog.csdn.net/marising/article/details/6101101

开源中国：可看看这个开源项目 http://t.cn/zYeL9Jn

数据挖掘研究院：h2w.iask.cn

licstar：NReadability http://t.cn/zYewPMn

我不是勒瑟：搜一下这篇论文：DOM Based Content Extraction via Text Density

@梁斌 推一下，各大公司都有做这个的，搜狗这个叫PA，page analysis，我也短期维护过，目前是某哥们再搞

最后：http://tomazkovacic.com/blog/56/list-of-resources-article-text-extraction-from-html-documents/

@KissDev

正文抽取的开源代码，基于文本密度的html2article: http://t.cn/8FvHNOY 基于标签比例的机器学习Dragnet：http://t.cn/RhnDNg0 专注新闻类网页提取的Newspaper：http://t.cn/RhnDNgW 集成goose等三种算法的readbilitybundle http://t.cn/RhnDNgO 我觉得最好的方法还可能是视觉系方法
````

##哪些好

眼花缭乱地看过上面的工具列表后，如何选择适用的工具呢？

上面链接中提到的[一个博客](www.tomazkovacic.com/blog "")（www.tomazkovacic.com/blog），

有[一篇文章](http://www.tomazkovacic.com/blog/122/evaluating-text-extraction-algorithms/ "")对各大文本抽取算法和工具进行了测试，算是间接给出了答案。

不过，这个博主的博客最近挂掉了，我另外找到了这个文章的pdf版本（下面所有列表内容版权归属于tomaz kovacic），

现在将关键内容摘录一下：



上表列出了一些TE(text extraction)算法及实现了对应算法的工具（有部分工具是需要购买的）。



上表是对各个工具的测试结果。各项指标已经具有相当的说服力了，这里就不在赘述了。

##选哪些

看过上述result后，选出了一个初步备选列表（排除需要购买的工具和仅能通过API使用的工具）：

1. boilerpipe（java）

https://code.google.com/p/boilerpipe/

python-boilerpipe（python）

 https://github.com/misja/python-boilerpipe

2. goose（java）

https://github.com/GravityLabs/goose/

python-goose（python）

https://github.com/grangier/python-goose

3. readability（python）

https://github.com/kingwkb/readability

4. newspaper（python）

https://github.com/codelucas/newspaper

##测试

下一篇文章将会记录我本人使用上面几种工具的测试代码和测试结果。