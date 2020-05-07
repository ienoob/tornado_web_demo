#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import print_function
import traceback
from tornado_web.utils.exception import TWException


# rest 请求处理装饰器
def request_decorator(func):

    def wrapper_method(*args, **kwargs):
        message = {"error": True, "response": {}}
        try:
            message = func(*args, **kwargs)
            if isinstance(message, dict):
                message["error"] = False
            else:
                raise Exception()
        except TWException as e:
            message["error"] = True
            message["error_message"] = e.error_message
        except Exception as e:
            print(e)
            traceback.print_exc()
            message["error_message"] = "π_π"
        finally:
            return message
    return wrapper_method
