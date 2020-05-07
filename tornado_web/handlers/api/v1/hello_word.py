#!/usr/bin/env python
# -*- coding:utf-8 -*-
from tornado import gen, web
from tornado_web.web import TWRequestHandler
from tornado_web.utils.decorator import request_decorator


# 节点信息
class HelloHandler(TWRequestHandler):

    def get(self):
        data = self.get_db_operation()
        self.finish(data)

    @request_decorator
    def get_db_operation(self):

        data = {"response": {"info": "hello world"}}
        return data
