Title: 网易微博api应用与开发
Date: 2015-08-20 10:12
Category: Work
Tags: netease, microblog, api
Summary: 介绍如何使用网易微博api进行开发.

之前做过与网易微博对接的一个项目，使用了网易微博提供的java版本的api，在这里做个记录和分享。  
当然,网易微博,腾讯微博等目前都属于日薄西山的产品了,再讨论与这两个微博的对接意义不大,  
以下内容仅作为与新浪微博对接开发时的参考使用吧.

##准备工作

要使用网易微博的api，准备工作有两步：
  
###申请app token

在 http://open.t.163.com/ 申请 “应用创建”，按里面的提示一步步填写（中间需要输入一个网易通行证的用户名和密码），最终获取到如下一些数据(用于OAuth鉴权):

Consumer Key：D6NAMbu5XXXXXXXX  
Consumer Secret：zDHZ6IgVDxKYD6DWK9C5Lm77XXXXXXXX  
Acess token：7162f116054cdf20f3a6d357XXXXXXXX  
Acess token secret：d06a2a3d89edbab2f9f55429XXXXXXXX

###下载网易微博api

http://code.google.com/p/t-163-open-java-api/  
上面这个地址是网易微博官方api源码的发布地址(t163_java_api_v1.1.zip).

如果觉得使用源码进行开发不方便，也可以使用下面的我打包好的jar包(该jar包是使用2011.5月的源码打包生成的).  
t4j-163.jar

##代码编写：

首先可以参考一下t4j\example\OAuthGetToken.java这个示例.

自己编写时，需要做以下几步：  
````java
//1.创建blog对象
TBlog tblog = new TBlog();
try {
//2.set 申请得到的consumer参数
tblog.setOAuthConsumer("D6NAMbu5XXXXXXXX", "zDHZ6IgVDxKYD6DWK9C5Lm77XXXXXXXX");
//set 申请得到的token参数
AccessToken accessToken = new AccessToken("7162f116054cdf20f3a6d357XXXXXXXX", "d06a2a3d89edbab2f9f55429XXXXXXXX");
//3.向blog对象设置token参数
tblog.setToken(accessToken.getToken(), accessToken.getTokenSecret());
//4.此时该blog对象就已经可用了，可以进行具体的业务逻辑处理了。
User user = tblog.verifyCredentials();
//测试登录用户名
System.out.println("登录的用户： " + user.getName());
System.out.println("我的主页 home timeline： " + user.getName());
//发送微博消息
tblog.updateStatus("来自java sdk——使用网易微博api发送的微博。");
} catch (TBlogException e) {
// TODO Auto-generated catch block
e.printStackTrace();
}
````