Title: 高性能Web App实践之Lua初试[2]
Date: 2016-04-26 18:31
Category: work
Tags: lua
Summary: 为了解决工作中遇到的高性能Web App实现问题，考虑采用openresty和lua的方案，本篇为系列文章的第二篇，Lua的语法与使用.
Slug: high-performence-web-app[2]-lua-hello-world

OpenResty使用Lua作为嵌入式脚本语言，处理在nginx.conf中不方便实现的复杂业务逻辑、数据库（sql/nosql）交互等操作。

本篇为这个系列文章的第二篇，介绍lua的版本，语法特性等内容。


##历史与版本



##语法要点

###基本语法

Lua是类C的，是大小写字符敏感的

Lua脚本的语句的分号是可选的

字符串你可以用单引号，也可以用双引号，还支持C类型的转义

Lua的数字只有double型，64bits，你不必担心Lua处理浮点数会慢（除非大于100,000,000,000,000），或是会有精度问题

布尔类型只有nil和false是 false，数字0啊，‘’空字符串（’\0’）都是true

lua中的变量如果没有特殊说明，全是全局变量，那怕是语句块或是函数里。变量前加local关键字的是局部变量。

###控制语句


###函数


###封装的数据结构
Table

Lua的下标不是从0开始的，是从1开始的


###全局变量
Lua把所有的全局变量放在了一个叫“_G”的Table里


###模块
设置环境变量LUA_PATH="/module_path/?.lua;;"

模块有两种定义方式：  
1. 在代码开始写明：module("[module name]", package.seeall)
2. 在module代码结尾显式地return一个module(table等)对象

require

loadfile



##log记录要求


