#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals



AUTHOR = 'andrey'
SITENAME = '123'
SITEURL = 'https://neandreyblog.herokuapp.com/'

# Define some project paths that have special meanings in Pelican
PATH = 'content'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = 'en'
#DEFAULT_DATE = 'fs'
#DEFAULT_DATE_FORMAT = '%a %d %B %Y'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None


USER_LOGO_URL = SITEURL + '/static/images/logo.png'

#TAGLINE = 'hello andrey ... '
#ROUND_USER_LOGO = True
#Theme
#THEME = "pelican-svbhack"

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
