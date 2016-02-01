Title: 关于爬虫的那些事 - 第二部分
Date: 2016-01-27 16:30
Category: work
Tags: web crawler, web spider
Summary: 介绍我实现的简单的网络爬虫.
Slug: everything-I-know-about-web-crawler - part II

这个系列的文章分为两篇, 这里是第二部分：给出一些爬虫的具体实现.

##基于爬虫框架的实现
基于爬虫框架的实现非常简单, 一般就是自定义一个爬虫业务逻辑处理类, 继承框架提供的父类即可.

在业务逻辑类中, 需要写代码对页面中自己感兴趣的HTML标签的数据进行提取和存储.

下面是一个scrapy框架下的实现:
```python
# coding=utf-8
from scrapy import Request

from scrapy_crawler.items import WebItem

__author__ = 'rockyqi1001@gmail.com'

from scrapy.spiders import Spider
from scrapy.selector import Selector
import logging


class WebSpider(Spider):
    name = "scrapy_test"

    start_urls = [
        "http://news.163.com/13/0708/10/938MALOV00014AED.html",
        "http://news.163.com/13/0708/11/938Q3F1N00014Q4P.html",
    ]

    # def start_requests(self):
    #     with open('urls_3k.txt', 'r') as urls:
    #         for url in urls:
    #             yield Request(url, self.parse)

    def parse(self, response):
        """
        The lines below is a spider contract. For more info see:
        http://doc.scrapy.org/en/latest/topics/contracts.html
        @url http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/
        @scrapes name
        """
        logging.debug('response.encoding=' + response.encoding)

        sel = Selector(response)
        item = WebItem()
        item['url'] = response.url
        item['title'] = sel.xpath('//title/text()').extract()
        item['keywords'] = sel.xpath(
            "//meta[@name='keywords']/@content | //meta[@name='Keywords']/@content | //meta[@name='keyword']/@content").extract()
        item['description'] = sel.xpath(
            "//meta[@name='description']/@content | //meta[@name='Description']/@content | //meta[@name='descriptions']/@content").extract()

        logging.debug('title=' + item['title'][0])
        return item
```
这个爬虫从网易新闻的页面中提取了title, keywords和description数据.

##单独实现的爬虫
###基于requests和beautifulsoup的爬虫
自己实现的爬虫中, 有这样几个技术点:

* 可以使用mysql或redis存储URL队列, 状态(是否已爬取)和结果(爬取结果)
* 对于中文网页内容的编解码处理(中文网页的编码不是很统一, 大致有gb2312, utf-8等几种)

第一点不必多说, 属于基础内容; 这里重点讲解下第二点, 对于编解码的处理.  
废话不多说, 先看代码:
```python
HTTP_PROXY = {
    "http": "http://192.168.81.28:1081"
}

REQ_HEADERS = {
    'Connection': 'keep-alive',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36',
    'DNT': '1',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4,en-US;q=0.2',
    'Cache-Control': 'max-age=0',
}


def get_http_bs(url, use_proxy=False):
    if not url:
        return
    if use_proxy:
        resp = requests.get(url, headers=REQ_HEADERS, proxies=HTTP_PROXY, verify=False)
    else:
        resp = requests.get(url, headers=REQ_HEADERS, verify=False)
    if resp.ok and resp.content is not None:
        charset = requests.utils.get_encodings_from_content(resp.content)
        if len(charset) > 0:
            resp.encoding = charset[0]
            bs = BeautifulSoup(resp.text)
        else:
            bs = BeautifulSoup(resp.content, from_encoding='gb18030')
        return bs
    else:
        print 'Error when request:%s' % url
        if resp:
            print resp.status
            print resp.content
        raise Exception('Connection failed.')
        
def _get_page_detail_data(bs):
    if not bs:
        return

    if bs.title:
        title = bs.title.get_text().strip()
    else:
        title = u''

    summary = bs.find('p', class_='ep-summary')
    if summary:
        summary = summary.get_text()
    else:
        summary = u''

    content_list = list()
    for content in bs.find_all('div', id='endText'):
        content_list.append(content.get_text().strip())
    if content_list:
        content_data = u'\n'.join(content_list)
    else:
        content_data = u''

    return title, [title, summary, content_data]
```
get_http_bs方法接受url字符串作为参数, 并完成对url的抓取和编码,   
最终返回beautifulsoup对象, 供后续解析代码直接使用.

_get_page_detail_data方法接受上一步产生的bs对象作为参数, 并对url中的标签进行解析.  
代码所示为对网易新闻(2016-01页面布局)正文页的标题, 摘要和正文内容进行提取的例子.

其中与编码有关的两行关键代码是:
```python
charset = requests.utils.get_encodings_from_content(resp.content)
bs = BeautifulSoup(resp.content, from_encoding='gb18030')
```
最早实现爬虫时, 我在中文乱码问题上卡了很久, 找了很多资料并且经过测试后, 

使用上述代码完成了正确的中文网页文件编码.

###基于selenium或phantomjs的爬虫
对于需要解析页面上面的js加载内容的爬虫(例如, 天猫或者京东的商品价格),

可以使用selenium或者phantomjs实现, 下面是demo代码:
```python
# using chrome driver to start chrome and do price_crawl
CHROME_DRIVER_PATH = 'XXX/google/chromedriver.exe'

chromeOptions = webdriver.ChromeOptions()
# disable image loading
prefs = {"profile.managed_default_content_settings.images": 2}
chromeOptions.add_experimental_option("prefs", prefs)

# disable flash
chromeOptions.add_argument("--disable-bundled-ppapi-flash")
chromeOptions.add_argument("--disable-plugins-discovery")
chromeOptions.add_argument("--disable-internal-flash")

DRIVER = None

def init():
    if not DRIVER:
        DRIVER = webdriver.Chrome(CHROME_DRIVER_PATH, chrome_options=chromeOptions)

def get_http_bs(url, use_proxy=False):
    init()
    DRIVER.get(url)
    html_data = DRIVER.page_source
    # if resp.content is not None:
    if html_data is not None:
        charset = requests.utils.get_encodings_from_content(html_data)
        if len(charset) > 0:
            bs = BeautifulSoup(html_data, from_encoding=charset)
        else:
            bs = BeautifulSoup(html_data, from_encoding='gb18030')
        return bs
```
调用上面的get_http_bs, 会打开一个chrome浏览器, 并在浏览器中访问输入的url, 然后返回编码好的bs对象供解析使用.

上面代码中设置多项chromeOptions, 目的是禁止浏览器加载目标url中的图片和flash等数据, 提高url抓取速度.

如果不想打开浏览器, 可以使用phantomjs工具进行url中的js解析, 代码如下:
```python
PHANTOMJS_DRIVER_PATH = 'XXX/phantomjs-2.0.0/bin/phantomjs.exe'
DRIVER = webdriver.PhantomJS(PHANTOMJS_DRIVER_PATH)
```
