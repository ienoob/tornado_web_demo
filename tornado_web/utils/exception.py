#!/usr/bin/env python
# -*- coding:utf-8 -*-


# 自定义异常
class TWException(Exception):

    def __init__(self, error_code, error_message):
        super(TWException, self).__init__()
        self.error_code = error_code
        self.error_message = error_message