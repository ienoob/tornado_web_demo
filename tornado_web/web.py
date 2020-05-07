#!/usr/bin/env python
# -*- coding:utf-8 -*-

from tornado.web import RequestHandler
from tornado.web import Application


class TWRequestHandler(RequestHandler):
    pass


class TWApplication(Application):

    def __init__(self, conf, handlers=None, default_host=None, transforms=None, **settings):
        super(TWApplication, self).__init__(handlers=handlers,
                                            default_host=default_host,
                                            transforms=transforms,
                                            **settings)
