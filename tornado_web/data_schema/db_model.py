#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals


from sqlalchemy import Column, String, DateTime, Float, Integer, SmallInteger
from tornado_web.data_schema.base import TWDeclarativeBase


class TWVersionsModel(TWDeclarativeBase):
    """产品版本信息"""

    __tablename__ = 't_versions'

    publish_time = Column(Float, doc='发布时间')
    version = Column(String(24), doc='版本号')
