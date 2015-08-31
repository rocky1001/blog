Title: 网页正文内容提取工具测试记录
Date: 2015-08-19 17:02
Category: Work
Tags: text extraction, tools, test, python, java
Summary: 对于几种比较知名的网页正文内容提取工具的测试和对比记录.
Slug: html-text-extraction-tools-test

接前一篇概述。

在开始之前，先简单说一下网页正文提取会遇到的一些问题：

1. 网页编码

国内网页大部分都是使用gb2312编码，但是也有用GBK，UTF-8等编码的网站。

为了避免结果呈现为乱码，网页的编码转换是一个需要考虑的问题。

下面进入正题。

##boilerpipe

1. 配置及测试代码

配置：

该工具的配置非常简单，把tar中的核心jar包以及lib下面引用的两个jar包扔进工程即可。

测试代码：

````java
String urlString = "http://auto.163.com/14/1110/23/AANO1BGL00084TUP.html";
private static String testBoilerpipe(String urlString) throws BoilerpipeProcessingException, IOException {
  final ExtractorBase extractor = CommonExtractors.ARTICLE_EXTRACTOR;
  // final ExtractorBase extractor = CommonExtractors.DEFAULT_EXTRACTOR;
  // final ExtractorBase extractor = CommonExtractors.CANOLA_EXTRACTOR;
  // final ExtractorBase extractor = CommonExtractors.LARGEST_CONTENT_EXTRACTOR;
  return extractor.getText(new URL(urlString));
}
````

2. 对编码的处理

方法一：修改HTMLFecther，在最后加上如下代码：

````java
final byte[] data = bos.toByteArray(); //stays the same
byte[] utf8 = new String(data, cs.displayName()).getBytes("UTF-8"); //new one (convertion)
cs = Charset.forName("UTF-8"); //set the charset to UFT-8
return new HTMLDocument(utf8, cs); // edited line
````

方法二：不修改boilerpipe，使用getText的override方法：

````java
URL url = new URL("http://some-page-with-utf8-encodeing.tld");
InputSource is = new InputSource();
is.setEncoding("UTF-8");
is.setByteStream(url.openStream());
String text = ArticleExtractor.INSTANCE.getText(is);
````

注：使用测试代码抓取的中文页面，暂时没有遇到编码问题。上面这两个方法来自stackoverflow，仅作参考。

3. 简单测试结果，待补充

对于有整块正文内容的页面，例如：

http://server.chinabyte.com/399/12587899.shtml

http://news.163.com/14/1110/10/AAMC8KDJ00014AED.html

等，使用boilerpipe的ARTICLE_EXTRACTOR，效果还不错；

但是对于图文混排内容，例如：

http://auto.163.com/14/1110/23/AANO1BGL00084TUP.html

效果非常不好。