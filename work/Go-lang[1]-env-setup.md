Title: Go lang初试[1]-安装
Date: 2015-08-19 17:06
Category: Work
Tags: go, env, setup
Summary: 摘录了《Go语言编程》中对于Go env的安装配置内容.
Slug: Go-lang[1]-env-setup

早就听说了go lang的大名，最近有时间研究一下。

目前正在看的书是七牛的许式伟等编写的《Go语言编程》。

书写的很好：在最开始就清楚地写明了go lang出现的意义，以及一些语言方面一些好的特性；

下面的内容基本是该书内容的摘要，方便有需要的人直接使用。

##go env安装和配置

go lang的官网（https://golang.org）就算用了梯子，访问仍然挺慢的。不过国内有个爱好者的站点（http://golangtc.com/），相关资源在这个国内站上也可以下载到。

1. 先在这里下载os对应的安装包：http://golangtc.com/download

目前最新的版本是go1.4rc1

2. 配置环境变量

首先需要设置环境变量GOROOT 到go根路径；

其次在PATH中添加GOROOT/bin；

最后在命令行中分别输入：

```go
go version
````

（若仅将go的bin写进PATH，不设置GOROOT，上面的命令仍然会输出正常打印）

```go
go env
````
（若仅将go的bin写进PATH，不设置GOROOT，在win7下面输入 go env 后会提示：go: cannot find GOROOT directory: c:\go）

检查是否正常输出结果，没有报错。



##IDE 设置

1. notepad++ 

《Go语言编程》中关于notepad++设置的描述已经过时了。相关设置可以参考这篇博文，不过这篇文章也有点过时了。下面更新一下：

    *在这里下载go lang支持包go.zip；（题外话：这个地址还能下载到供notepad++使用的其他语言的支持包，例如google的protobuf等等） 

    *将go.zip包中的userDefineLang_Go.xml 更名为userDefineLang.xml，并将文件内容中，开始和最后对<NotepadPlus>的注释放开，然后把文件放到"%USER%\AppData\Roaming\Notepad++"路径下(WIN7)，若同名文件已存在，则需要进行合并；——此时，语法高亮已经可用了

    *将go.zip包中的go.xml文件copy至notepad++安装目录下的plugins\APIs目录（例如：D:\Program Files\Notepad++\plugins\APIs）;——此时，关键字自动补全就可用了（可能需要在npp的设置->首选项->自动完成 中打开自动完成功能）

    *配置NppExec插件，可以在npp中方便地运行程序。

2. eclipse

google有开发eclipse适用的插件：goclipse，但是对版本要求较高，见下：

Requirements:

Eclipse 4.3 (Kepler) or later (http://www.eclipse.org/).

A 1.7 Java VM or later (http://www.java.com/). Otherwise GoClipse will silently fail to start.

下一篇总结下go lang的语法特性。