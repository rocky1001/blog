Title: 基于RESTful API开发的一个简单的WEB APP
Date: 2015-11-03 15:26
Category: work
Tags: python, django, restful, web
Summary: 在工作中开发了一款DEMO性质的WEB APP, APP本身的功能比较简单, 比较有意思的是整个WEB APP是前后端完全分离的, 后端以REST接口方式提供前端所需的所有数据.
Slug: a-simple-web-app-under-restful

在一个小Demo项目中,需要: 

前后端配合完成数据配置(CRUD), 数据展示(前端主要用ECharts对数据进行图表展示); 

后端完成数据的收集(实际上就是一个HTTP Server, 接收数据源POST请求提交的数据, 进行存储), 并对原始数据进行汇总和统计;

后端还需要提供RESTful风格的API, 与前端传递数据.

之前做的大部分开发工作, 包括使用的框架(Struts, Spring MVC, Django, Flask等), 

都包含了前端view(或是template)部分的工作, 因此对于这种前后端完全分离的项目还是第一次实践.

不过, RESTful API在内外部对接时倒是用过很多次了, 因此这篇文章不会过多地涉及RESTful API的格式规范等内容.  
(也可以参见[这篇文章](http://www.vinaysahni.com/best-practices-for-a-pragmatic-restful-api "best-practices-for-a-pragmatic-restful-api"), 说的比较详细, 而且具有实际应用价值).

##RESTful API接口文档

既然是前后端完全分离, 基于RESTful API协作, 

那么一个接口全面, 定义详细, 最好再带上demo的**API文档**就是必不可少的了,

这也是前后端分别开发的重要依据.

编写这个API文档可不容易, 主要挑战集中在:

1. 尽量考虑到全面的接口功能, 如有遗漏要尽快完善并重新发布文档
2. 文档格式规范, 尤其是交互使用的json数据格式
3. 每个接口最好配上一个demo request/response
4. 随着开发的进行和需求的变化, 文档的变动会**非常频繁**, 需要及时维护
  
在这种架构下, 一个数据表的CRUD操作就会涉及到3-4个API接口, 同时每个接口需要有准确合理的数据和返回值,

虽然是个小Demo项目, API接口文档可足足写了11页.

##优缺点的思考


###优点

在前后端分离的架构下, 

基于RESTful API接口文档, 前后端开发人员可以**完全独立**地进行开发工作, 将另一端假想作已经存在的实体即可.

并根据接口文档的修改, 随时调整自己负责的代码.

这样前后端的开发非常独立, 不会受另一端的bug, 进度等等问题的影响.

同时, 两端的开发人员只需要关心自己那一侧的功能和代码即可, 

不用像之前在MVC框架下开发时, 

前端人员要了解不同的框架中模板语言的用法, 

后端人员则要了解javascript等的用法.

###缺点

对开发人员严格按照接口文档进行代码开发的要求很高;

相对于之前的框架式开发, 前端代码量会有些增加(主要在REST接口数据组织处理部分).

