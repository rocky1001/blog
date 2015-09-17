Title: HBase的rowkey设计以及列(column)上的索引
Date: 2015-09-17 11:10
Category: work
Tags: hbase, index, column, apache, phoenix
Summary: 使用HBase时,设计rowkey应注意的问题,以及除了可以使用rowkey查询数据外,如何高效地使用column value查找相应的数据.
Slug: hbase-rowkey-design-and-column-index

工作中HBase的应用越来越多, 写篇文章记录下HBase应用中的常见问题.

##rowkey设计

官方推荐的[row key设计](http://hbase.apache.org/0.94/book/rowkey.design.html "row key设计(官方文档,字字珠玑,推荐阅读)")的做法是:

1. 减小row和column的长度(包括row key的名称,column family的名称,column的名称等)
2. (有可能的话)使用数字类型(long等)代替字符类型(string)作为数据进行存储(因为long型占用的存储空间更小)
3. 将所有可能用于查询的字段全部拼接到HBase的row key中(同时row key要尽量短,这里有个平衡取舍的问题)
4. row key的首字节要尽量分散,这会影响到数据分区(region split)和读取效率(避免hot region problem)
5. 由于rowkey默认是按照正序排序的(由小到大),对于需要查看最新数据的应用,时间类型的key需要倒排使用  
     可以用(Long.MAX_VALUE - timestamp)这种方式,  
     也可以用reverse(timestamp)的方式.  

在使用时,直接使用rowkey中的字段(单个或范围)即可进行高效查询.

但是,如果想要使用column value去查询数据(这种需求在结构化数据查询中非常多见),该怎么办呢?

##column索引

传统关系型数据库中,解决上述问题的办法是给要查询的列建立索引.

HBase中的处理方式也是类似的.

###解决方案1(IBM商业产品,非开源)

IBM的InfoSphere BigInsights 产品中,支持直接对HBase数据表创建索引.

相关资料见[这里](http://www-01.ibm.com/support/knowledgecenter/SSPT3X_2.1.2/com.ibm.swg.im.infosphere.biginsights.bigsql.doc/doc/bsql_create_index.html?lang=zh "").

###解决方案2(华为产品,已开源)

华为给出了自己的开源解决方案[hindex](https://github.com/Huawei-Hadoop/hindex)(介绍文档在[这里](http://events.linuxfoundation.org/sites/events/files/slides/ApacheCon_hindex_0.pdf "")),支持对HBase数据表创建索引.

###解决方案3(Apache-Phoenix,开源项目)

[Apache Phoenix](https://phoenix.apache.org/index.html "")是:

1. 一个架构在HBase之上的关系型数据库层
2. 目的是**将HBase封装成为一个关系型数据库使用**
3. 可以接受SQL查询,并转换为HBase的scan查询方式,然后再将scan的查询结果封装为JDBC结果集(result sets)返回

题外话:

看了上述描述后,是不是觉得跟"Hive on HBase"有点像? Quora上面的[这个问题](https://www.quora.com/How-is-Apache-Phoenix-different-from-Hive-Hbase-integration "")可以解释两者的区别.

这里还有一篇Phoenix跟相关产品(Hive,Impala)的性能对比:[Performance](https://phoenix.apache.org/performance.html "Phoenix performance")

从评测文章看到Phoenix的性能要好于Hive和Impala.

回到正题:

从Phoenix的[语法说明](https://phoenix.apache.org/language/index.html "Phoenix grammar")中可以看到,

Phoenix通过SQL直接支持数据的CRUD操作,当然也包括了**[创建索引](https://phoenix.apache.org/language/index.html#create_index "")**的命令.

eg:  
CREATE INDEX my_idx ON sales.opportunity(last_updated_date DESC)

根据文档描述,创建完成索引后,随着数据的变化,索引会被自动更新.

并且在后续的查询中也就可以使用索引来提高查询效率了.

###结论
最终决定在这个项目中,尝试使用Phoenix作为HBase的封装,完成所有与HBase的交互动作.

后续会有文章分享在项目中应用Phoenix的过程和问题.
