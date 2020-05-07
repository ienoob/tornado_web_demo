#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr


class TWTableModel(object):
    """TLTableModel表基础统一性声明"""

    def __init__(self, **kwargs):
        """表的统一性质的基础声明初始化"""
        for k, v in kwargs.items():
            setattr(self, k, v)

        super(TWTableModel, self).__init__()

    @declared_attr
    def _id(self):
        """所有表的主键f_id定义,使用uuid唯一码"""
        return Column(String(32), primary_key=True)

    def update(self, **kwargs):
        """更新记录内容"""
        for k, v in kwargs.items():
            if v is not None:
                setattr(self, k, v)


TWDeclarativeBase = declarative_base(cls=TWTableModel)