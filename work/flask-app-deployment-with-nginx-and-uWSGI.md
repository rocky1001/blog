Title: 使用nginx+uWSGI部署Flask WEB应用
Date: 2015-11-25 18:10
Category: work
Tags: python, web, nginx, uWSGI, flask
Summary: 描述了如何使用 nginx+uWSGI 发布一个flask开发的python web应用.
Slug: flask-app-deployment-with-nginx-and-uWSGI

首先, 在网上随处可见的nginx+uWSGI+flask配置文档(参见[这里](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-14-04 "How To Serve Flask Applications with uWSGI and Nginx on Ubuntu 14.04"), [这里](https://www.digitalocean.com/community/tutorials/how-to-deploy-flask-web-applications-using-uwsgi-behind-nginx-on-centos-6-4 "How To Deploy Flask Web Applications Using uWSGI Behind Nginx on CentOS 6.4"), 还有[这里](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-centos-7 "How To Serve Flask Applications with uWSGI and Nginx on CentOS 7")), 

以及flask官方文档的uWSGI配置[说明](http://flask.pocoo.org/docs/0.10/deploying/uwsgi/ "")的前提下,

为什么还会有这样一篇文章?

因为在网上找到的都是片面的介绍, 或者并没有给出**完整成套**的配置文件, 

在经过 [ 查找资料 -> 验证筛选资料 -> 摸索着自行配置 ] 这一痛苦阶段之后,

这里将可用的一整套配置文件完整地分享出来, 供有需要的人参考.

##整体架构

nginx作为反向代理, 将收到所有请求转发到后端uWSGI server;

uWSGI作为web server, 是flask app的入口;

flask作为web framework, 是web app的功能和逻辑的具体实现.

##nginx配置
这里没有给出nginx.conf通用配置文件, 实际上使用nginx安装后的默认配置文件就可以满足要求;

下面是uwsgi应用所需的nginx配置文件:  
uwsgi-flask.conf
````
upstream flask {
    server unix://tmp/uwsgi-flask.sock; # using a file socket
}

server {
    listen 80;
    server_name xxx.net;
    client_max_body_size 1M;

    location / {
        access_log  logs/uwsgi-flask.log;
        uwsgi_pass flask;
        include uwsgi_params;
    }
````

上述配置文件放在nginx的conf目录下, 并在nginx.conf中引用该配置文件所在目录即可.

##uWSGI配置
uWSGI可以使用命令行参数直接启动, 但是显然不够直观并且不好维护, 

因此这里采用的是启动时指定配置文件的方式,

下面是uWSGI启动用所需的配置文件:  
uwsgi-flask.ini
````
[uwsgi]
master=true
processes = 4

uwsgi-socket=/tmp/uwsgi-flask.sock    #uwsgi sock file path, should be same with nginx config

chdir=/opt/uwsgi-flask    #flask app root path
module=flask_wsgi    #flask app main function
callable=app    #flask instance name

pidfile=/var/run/uwsgi-flask.pid    #uwsgi pid path
daemonize=/var/log/uwsgi-flask/uwsgi.log    #uwsgi daemon log path
check-static=/opt/uwsgi-flask    #flask app root path

chown-socket=www:www
chmod-socket=664
uid=www
gid=www

vacuum = true
die-on-term = truegroups
````

##flask结构及代码
一个简单的flask app的目录结构如下面的树状列表所示:
````
uwsgi-flask/
|-- __init__.py
|-- app
|   |-- __init__.py
|   |-- views_xxx.py
|   |-- views_yyy.py
|   `-- models.py
|-- configs
|   |-- __init__.py
|   `-- config.py
|-- flask_wsgi.py
|-- static
|   |-- xxx.gif
|   `-- yyy.js
`-- templates
    |-- xxx.html
    `-- zzz.html
````

上面的文件中, flask_wsgi.py是作为uWSGI调用flask app的入口文件存在的, 

flask_wsgi.py的内容如下:
````python
# coding=utf-8
from flask import Flask
from app.views_xxx import view_x
from app.views_yyy import view_y

__author__ = 'rockychi1001@gmail.com'

app = Flask(__name__)
app.register_blueprint(view_x)
app.register_blueprint(view_y)

if __name__ == "__main__":
    app.run()
````

**flask_wsgi**和**app**这两个名字全部配置在了uWSGI的配置文件中.

另外, 上述代码里又应用了Blueprint(说明见[这里](http://flask.pocoo.org/docs/0.10/blueprints/ "")),  
使得功能不同的view function可以分开为不同的view源文件.

views_xxx.py的内容如下:
````python
# coding=utf-8
from flask import abort, Flask, Blueprint, make_response, render_template, send_from_directory, render_template_string
from flask import request, redirect

__author__ = 'rockychi1001@gmail.com'

view_x = Blueprint('view_x',
                   __name__,
                   template_folder=config.TEMPLATES_DIR)
                   

@view_x.route('/', defaults={'s_file': None})
@view_x.route('/<path:s_file>')
def root(s_file):
    if s_file:
        return send_from_directory(config.STATIC_DIR, s_file)
    else:
        return render_template('xxx.html')
````

views_yyy.py的内容如下:
````python
# coding=utf-8
from flask import abort, Flask, Blueprint, make_response, render_template, send_from_directory, render_template_string
from flask import request, redirect

__author__ = 'rockychi1001@gmail.com'

view_y = Blueprint('view_y',
                   __name__,
                   template_folder=config.TEMPLATES_DIR)
                   

@view_y.route('/info')
def info():
    token = request.args.get('token')
    if token != TOKEN_MD5:
        abort(400)
   
    return json.dumps({'num': 0, 'date': '', 'tags': ''})
````

上面就是除了app自身配置文件外(实际上就是常量字符串), 必需的应用配置及必要的代码了.
