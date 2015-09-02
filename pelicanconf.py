#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'rockychi1001@gmail.com'
SITENAME = u"/home/rocky"
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = u'zh'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
        )

# Social widget
SOCIAL = (
          ('github', 'https://github.com/rocky1001'),
          ('twitter', 'https://twitter.com/rockyqi1001'),
          ('weibo', 'http://weibo.com/u/2069459137'),
         )

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

# static paths will be copied without parsing their contents
STATIC_PATHS = [
    'images',
    'files',
]

# Plugin
PLUGINS=['plugins.sitemap', 'plugins.gzip_cache']
# SiteMap
SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.5,
        'indexes': 0.5,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly'
    }
}

# Google Analytics
GOOGLE_ANALYTICS = 'UA-xxx'

# Disqus comment integration
DISQUS_SITENAME = 'rockyqi'

# Theme
#THEME = './themes/bootstrap3'

THEME = './themes/coderocks'
DISPLAY_PAGES_ON_MENU = True
DISPLAY_CATEGORIES_ON_MENU = True
DISPLAY_CATEGORIES_ON_SUBMENU = False
DISPLAY_CATEGORIES_ON_POSTINFO = True
DISPLAY_AUTHOR_ON_POSTINFO = False
PAGES_SORT_ATTRIBUTE = 'Date'

DISPLAY_SEARCH_FORM = True
SEARCH_SITEURL = 'rockyqi.net'
