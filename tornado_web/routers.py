#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import with_statement

from tornado_web.handlers.api.v1.hello_word import HelloHandler

api_urls = [
    (r"/api/v1/hello", HelloHandler),
]

router_urls = api_urls