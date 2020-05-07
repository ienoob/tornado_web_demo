#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import copy
import os
import sys
from collections import OrderedDict
from contextlib import contextmanager

from lockfile import LockFile
from lockfile import LockTimeout

PY3 = sys.version_info >= (3,)

if PY3:
    try:
        from configparser import ConfigParser
    except ImportError:
        ConfigParser = object()
else:
    from ConfigParser import ConfigParser


@contextmanager
def safe_flush_file(file_path):
    lock_f = '%s' % os.path.basename(file_path)
    lock = LockFile(lock_f)
    while not lock.i_am_locking():
        try:
            lock.acquire(timeout=5)
        except LockTimeout:
            lock.break_lock()
        finally:
            lock.acquire()
    with open(file_path, 'w') as cf:
        try:
            yield cf
        finally:
            cf.close()
    lock.release()


class ConfigParserValidate(object):
    """配置信息验证插件"""

    @staticmethod
    def validate():
        return True


class ConfigParserWithDefault(ConfigParser):
    """配置文件解释器"""

    def __init__(self, defaults, *args, **kwargs):
        self.defaults = defaults if isinstance(defaults, (dict, )) else {}
        ConfigParser.__init__(self, *args, **kwargs)
        self.is_validated = False

    def _validate(self):
        self.is_validated = ConfigParserValidate.validate()

    def get(self, section, key, **kwargs):
        section = str(section)
        key = str(key)
        defaults = self.defaults

        if self.has_option(section, key):
            return ConfigParser.get(self, section, key, **kwargs)

        if section in defaults and key in defaults[section]:
            return defaults[section][key]

        raise Exception(
            "[{section}/{key}] not found in config".format(**locals()))

    def get_boolean(self, section, key):
        val = str(self.get(section, key)).strip()
        if '#' in val:
            val = val.split('#')[0].strip()
        if val.lower() == "true":
            return True
        return False

    def get_int(self, section, key):
        return int(self.get(section, key))

    def get_float(self, section, key):
        return float(self.get(section, key))

    def read(self, file_name):
        ConfigParser.read(self, file_name)
        self._validate()

    def convert_dict(self, display_source=False):
        cfg = copy.deepcopy(self._sections)

        for options in cfg.values():
            options.pop('__name__', None)

        if display_source:
            for section in cfg:
                for k, v in cfg[section].items():
                    cfg[section][k] = (v, 'current')

        for section in sorted(self.defaults):
            for key in sorted(self.defaults[section].keys()):
                if key not in cfg.setdefault(section, OrderedDict()):
                    opt = str(self.defaults[section][key])
                    if display_source:
                        cfg[section][key] = (opt, 'default')
                    else:
                        cfg[section][key] = opt

        return cfg


class ConfigurationUtil(object):
    """配置文件解释读-操作写操作代理"""

    def __init__(self, file_path, defaults=None):
        self.__conf = None
        self.__file_path = None

        if not os.path.exists(file_path):
            raise Exception('Not found conf file %s' % file_path)

        if file_path is not None:
            self.file = file_path
            self.conf = self._create_conf_obj(defaults)

    def _create_conf_obj(self, defaults):
        _conf = ConfigParserWithDefault(defaults)
        _conf.read(self.file)
        return _conf

    @property
    def file(self):
        return self.__file_path

    @file.setter
    def file(self, file_path):
        self.__file_path = file_path

    @property
    def conf(self):
        return self.__conf

    @conf.setter
    def conf(self, value):
        self.__conf = value

    def get(self, section, key, **kwargs):
        return self.conf.get(section, key, **kwargs)

    def get_boolean(self, section, key):
        return self.conf.get_boolean(section, key)

    def get_float(self, section, key):
        return self.conf.getfloat(section, key)

    def get_int(self, section, key):
        return self.conf.getint(section, key)

    def add_section(self, section):
        return self.conf.add_section(section)

    def has_section(self, section):
        return self.conf.has_section(section)

    def has_option(self, section, key):
        return self.conf.has_option(section, key)

    def remove_section(self, section):
        return self.conf.remove_option(section)

    def remove_option(self, section, option):
        return self.conf.remove_option(section, option)

    def convert_dict(self, display_source=False):
        return self.conf.convert_dict(display_source=display_source)

    def set(self, section, option, value):
        return self.conf.set(section, option, value)

    def flush(self):
        with safe_flush_file(self.file) as conf_file:
            self.conf.write(conf_file)

    @staticmethod
    def dump(file_path, defaults):
        all_vars = {k: v for d in [globals(), locals()] for k, v in d.items()}
        data = defaults.format(**all_vars)

        with safe_flush_file(file_path) as _f:
            _f.write(data)

