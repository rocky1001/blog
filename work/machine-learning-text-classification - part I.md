Title: 机器学习之文本分类 - 第一部分
Date: 2016-01-28 15:27
Category: work
Tags: python, machine learning, sklearn, text classification
Summary: 机器学习应用之文本分类算法的实现
Slug: machine-learning-text-classification - part I

近期工作中需要用到一些文本自动分类的工具, 因此学习并实践了机器学习中的一些文本分类算法.

这个系列的文章分为两篇, 本文是第一篇: 文本分类算法及其实现.

下一篇将会对已经实现的本文分类器尝试进行一些效果优化.

##概述及背景

###概述
机器学习作为Level 3层级的人工智能(见<<人工智能狂潮>>第二章内容), 是近年来的一个热点方向.

而机器学习的本质基本上就是对数据进行 **分类** , (对离散型数据; 而对连续型数据叫做"回归").

###背景
近期在进行人群标签计算时, 期望根据每个人的浏览或者点击URL的记录, 为这个人打上所谓的"标签",

这时, 比较简单粗暴的做法可以把URL中的二级域名直接映射到标签(例如auto.163.com -> "汽车"),  
然后把所有访问过这个URL的人都打上相同的标签;

稍高级一点的做法是, 预先准备好一个[词语->标签]的关联关系表(例如["奥迪A4"->"中级车"]),  
然后抓取URL的title, keywords, description和正文content(若可能),  
用词语表去抓取内容中查找, 取出现次数最多的词语对应的标签作为URL的标签,  
再汇总每个人访问的所有URL上面的标签, 得到这个人的标签.

更高级一些的做法是使用机器学习中的文本分类算法, 进行URL内容的自动分类.  
本篇文章介绍了这种分类办法.

##主要流程

1. 准备训练数据集(N个分类标签, 每个分类下有1-M个文档数据作为分类的支持数据)
2. 对训练数据进行分词
3. 分词结果计算TFIDF矩阵
4. 进行文本分类器训练
5. 保存训练得到的文本分类器模型
6. 再次加载上述模型，进行待预测文本数据的分类预测

在现有开源机器学习框架(sklearn)的辅助之下, 

上述流程中大量的工作集中在第1和第2步;

其次才是第4步, 选择和调优文本分类器模型.

###训练数据

训练数据我抓取了两套:

1. 网易新闻分频道的新闻数据
2. 汽车之家分级别的车型文章数据

数据的结构如下图所示:
<div class="picture">
![网易新闻分类训练数据]({filename}/images/work/netease_training_data.png "网易新闻分类训练数据")  
</div> 
<div class="picture">
![汽车之家分类训练数据]({filename}/images/work/autohome_training_data.png "汽车之家分类训练数据")  
</div> 

###分词

分词工具直接使用了大名鼎鼎的jieba分词, 配合上自己整理的专有名词字典  
(主要是针对汽车之家的数据, 车系名称基本都是专有名词),

可以得到不错的分词效果, 测试代码:
```python
# coding=utf-8
import jieba

__author__ = 'rockychi1001@gmail.com'

jieba_dict = ur'jieba_customer_dict.txt'
jieba.load_userdict(jieba_dict)

def jieba_tokenizer(x): return jieba.cut(x)

str_data = r'英菲尼迪英菲尼迪q50l2015款'
word_segs = jieba.cut(str_data).lower()
for word in word_segs:
    print word
```
分词结果:
```shell
英菲尼迪
英菲尼迪q50l
2015
款
```
可见, 在字典的帮助下, 正确地分出了"英菲尼迪q50l"这个车系名称.

在训练数据和分词工具(包括词典)都准备好了之后, 可以说已经成功了一半了.

###文本分类模型的训练
文本分类属于有监督的机器学习(Supervised Learning), 

在sklearn的官网上, 对该流程给出了详细的[流程图说明], 如下图所示:(http://www.astroml.org/sklearn_tutorial/general_concepts.html "")(到API级别)
<div class="picture">
![有监督学习流程图]({filename}/images/work/ML_SL_flow_chart_1.png "有监督学习流程图")  
</div> 
<div class="picture">
![有监督学习流程API]({filename}/images/work/ML_SL_flow_chart_2.png "有监督学习流程API")  
</div> 

此外, sklearn还提供了常用的文本分类算法类, 有如下一些:
```python
from sklearn.linear_model import RidgeClassifier
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import Perceptron
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestCentroid
from sklearn.ensemble import RandomForestClassifier
```

那么现在问题来了: 如何对这些文本分类算法进行评估, 从而选择一个效果最好的呢?

sklearn已经为我们想到了, 并且给出了[demo代码](http://scikit-learn.org/stable/auto_examples/text/document_classification_20newsgroups.html#example-text-document-classification-20newsgroups-py "文本分类算法对比demo代码").
 
下面是我简单修改的demo代码(已经[开源](https://github.com/rocky1001/Machine-Learning/blob/master/text_classifier/text_classifier_evaluation.py "分类算法评估代码")), 

在同一组训练数据集上, 使用各种常用文本分类算法进行的一个简单测试对比：
<div class="picture">
![汽车之家训练数据不同分类算法结果对比]({filename}/images/work/text_classifier_comparison.png "汽车之家训练数据不同分类算法结果对比")  
</div> 

从测试结果来看, LinearSVC分类算法的效果最好, 下面的测试结果就是基于LinearSVC算法给出的.

###测试
在选定算法并完成分类模型的训练后, 就可以拿一些待预测的数据, 用训练好的模型去做一下分类了.

这里, 除了使用原始训练集划分的测试集(总量的20%)进行测试之外, 我还抓取了几百个汽车类新闻和图片的URL内容(不在训练数据集内的), 并做了手工分类(分了一早上, 眼睛都看花了 XD );

用训练好的模型进行分类测试, 并将模型分类结果与我手工分类的结果进行了比较, 得到的结果如下:
```shell
LinearSVC(C=1.0, class_weight=None, dual=True, fit_intercept=True,
          intercept_scaling=1, loss='squared_hinge', max_iter=1000,
          multi_class='ovr', penalty='l2', random_state=None, tol=0.0001,
          verbose=0)
-------------------------------------------------------
                precision    recall  f1-score   support

          a       0.74      0.95      0.83        56
         a0       0.88      0.88      0.88         8
        a00       0.00      0.00      0.00         0
          b       0.99      0.94      0.97       592
          c       0.92      0.86      0.89        14
          d       0.00      0.00      0.00         0
         mb       0.00      0.00      0.00         0
        mpv       0.40      1.00      0.57         4
          p       0.92      0.87      0.89        38
         qk       0.94      1.00      0.97        15
          s       0.75      0.92      0.83        13
       suva       0.62      0.80      0.70        10

avg / total       0.95      0.94      0.94       750
-------------------------------------------------------
```

可见, 预测的平均精确度有95%, 文本分类器取得了较好的效果.

本文使用的全部代码和部分测试数据集, 已经在我的github上[开源](https://github.com/rocky1001/Machine-Learning/tree/master/text_classifier "文本分类算法初试"), 欢迎查看.
