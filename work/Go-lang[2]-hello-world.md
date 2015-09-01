Title: Go lang初试[2]-hello world
Date: 2015-08-19 17:15
Category: work
Tags: go, hello world
Summary: Go lang: hello world.
Slug: Go-lang[2]-hello-world

##第一个go lang程序——hello world

````go
package main
 
import "fmt"
 
func main(){
    p("rocky")
}
 
/* block comment */
func p(name string){
    fmt.Println("Hello," + name)
}
 
// single line comment
// func p(){
    // fmt.Println("Hello world!")
// }
````

##一些简单的语法特性

上面的简单的代码，用到了go lang的如下一些特性：

1. 代码第一行写明package；上例中，使用一个文件单独运行的程序必须放在package main下面，否则在go run运行时会报错：”go run: cannot run non-main package“

2. import 包名必须带引号；多个包名可以使用多次import；也可以将包名用引号括起来后，用换行符连接，然后在最外层包裹圆括号；

3. import不能引用代码中没有使用的包，否则编译时会报错：”imported and not used: xxx“

4. ”{“必须紧跟代码，不能在新行中出现；

5. main作为程序入口，不能携带参数，命令行参数使用os.Args变量获取；

6. 注释有块注释/* */和单行注释// 两种；

7. 定义func格式： func func_name(输入参数——可省略，括号需要保留)(返回参数——可以有多个，参数和括号都可省略){} ；

8. func定义不支持重载（overload）

##hello world中的“坑”

别小看了上面这几行代码，坑着实不少：

1. package 不是main，导致无法运行

2. import fmt没有用双引号 "" 包裹包名称，导致无法运行

3. 对go run / go install / go build 等的理解和使用