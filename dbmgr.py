#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys
import warnings

from sqlalchemy import create_engine
from tornado.options import define
from tornado.options import options
from alembic.config import Config
from alembic import command

try:
    from alembic.migration import MigrationContext
except ImportError:
    MigrationContext = None

reload(sys)
sys.setdefaultencoding('u8')

from tornado_web.utils.db import MySQLDBUtil
from tornado_web.utils.conf import ConfigurationUtil

warnings.filterwarnings("ignore")
_the_path = os.path.dirname(__file__)

support_models = ['setup', 'teardown']
define("model", type=str, default='setup',
       help="Laker database model manager with setup or teardown.")


class DBManager(object):

    def __init__(self, conf):
        _engine_args = {'pool_size': 10, 'pool_recycle': 3600}
        self.db_conf = conf
        self.url = 'sqlite:///foo.db'
        self.engine = create_engine(self.url, **_engine_args)

    def reset_db(self):
        if MigrationContext:
            from tornado_web.data_schema import db_model
            db_model.TLDeclarativeBase.metadata.drop_all(self.engine)
            mc = MigrationContext.configure(self.engine)
            if mc._version.exists(self.engine):
                mc._version.drop(self.engine)
            self.init_db()

    def upgrade_db(self):
        directory = os.path.join(_the_path, 'migrations')
        config = Config(os.path.join(_the_path, 'alembic.ini'))
        config.set_main_option('script_location', directory)
        config.set_main_option('sqlalchemy.url', self.url)
        command.upgrade(config, 'heads')

    def init_db(self):
        from tornado_web.data_schema import db_model

        db_model.TLDeclarativeBase.metadata.create_all(self.engine)
        self.upgrade_db()

    def create_db(self):
        _ = MySQLDBUtil(db_type='mysql',
                        host=self.db_conf['host'],
                        port=self.db_conf['port'],
                        user=self.db_conf['user'],
                        password=self.db_conf['password'],
                        db_name=self.db_conf['db'],
                        charset='utf8',
                        encoding='utf-8',
                        debugger=self.db_conf['debugger'])
        _.create_database(db_name=self.db_conf['db'], recreate_force=True)
        self.init_db()

    def drop_db(self):
        _ = MySQLDBUtil(db_type='mysql',
                        host=self.db_conf['host'],
                        port=self.db_conf['port'],
                        user=self.db_conf['user'],
                        password=self.db_conf['password'],
                        db_name=self.db_conf['db'],
                        charset='utf8',
                        encoding='utf-8',
                        debugger=self.db_conf['debugger'])
        _.drop_database(db_name=self.db_conf['db'])


if __name__ == '__main__':
    print('Laker database model manager start...')

    options.parse_command_line()
    if options.model not in support_models:
        options.print_help()
        sys.exit(1)

    _conf = ConfigurationUtil(os.path.join(_the_path, 'config.conf'), defaults={})
    _db_conf_section = 'mysql'
    _dbm = DBManager({'host': _conf.get(_db_conf_section, 'host'),
                      'user': _conf.get(_db_conf_section, 'user'),
                      'password': _conf.get(_db_conf_section, 'password'),
                      'port': _conf.get_int(_db_conf_section, 'port'),
                      'db': _conf.get(_db_conf_section, 'db'),
                      'debugger': _conf.get_boolean(_db_conf_section, 'debugger')})

    if options.model == 'setup':
        try:
            _dbm.create_db()
            sys.exit(0)
        except Exception as _exp:
            print('Laker database model manager setup error: %s' % str(_exp))
            sys.exit(1)
    else:
        try:
            _dbm.drop_db()
            sys.exit(0)
        except Exception as _exp:
            print('Laker database model manager teardown error: %s' % str(_exp))
            sys.exit(1)
