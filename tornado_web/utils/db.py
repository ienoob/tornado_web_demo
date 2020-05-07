#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

class MySQLDBUtil(object):
    """数据库管理

    功能需求满足：
        创建一个可用的数据库连接
        检查数据库实例是否存在
        创建数据库实例
        删除数据库实例
    """

    SUPPORT_DB_TYPES = ('mysql', )
    INFORMATION_SCHEMA_DB = 'information_schema'
    BUILD_IN_DB = ('information_schema', 'performance_schema', 'mysql')

    def __init__(self, db_type='mysql', host=None, port=9806,
                 user=None, password=None, db_name=None,
                 charset='utf8', encoding='utf-8', debugger=False):
        if db_type not in self.SUPPORT_DB_TYPES:
            raise Exception("db_type is not supported.")

        self._db_type = db_type
        self._host = host if host is not None else '127.0.0.1'
        self._port = port
        self._user = user
        self._password = password
        self._db_name = db_name
        self._charset = charset
        self._encoding = str(encoding)

        self.debugger = debugger
        self._connection = None

    def create_connection(self, include_db=True):
        if self._connection is not None:
            return
        if include_db:
            if self._db_name is None:
                raise Exception("error missing db name.")
            _engine = self._create_engine_with_db()
        else:
            _engine = self._create_engine_without_db()

        self._connection = _engine.connect()

    def close_connection(self):
        if self._connection is None:
            return
        try:
            self._connection.close()
        except:
            pass
        else:
            self._connection = None

    def get_connection(self, include_db=False):
        if self._connection is None:
            self.create_connection(include_db)
        return self._connection

    def _create_engine_with_db(self):
        url = '%s://%s:%s@%s:%s/%s?charset=%s' % (
            self._db_type, self._user, self._password,
            self._host, self._port, self._db_name, self._charset)

        return create_engine(url,
                             encoding=str(self._encoding), echo=self.debugger)

    def _create_engine_without_db(self):
        url = '%s://%s:%s@%s:%s/?charset=%s' % (
            self._db_type, self._user, self._password,
            self._host, self._port, self._charset)

        return create_engine(url,
                             encoding=str(self._encoding), echo=self.debugger)

    def is_exist_database(self, db_name=None):
        name = db_name if db_name is not None else self._db_name
        if name is None:
            raise Exception("error missing db name.")

        _sql = "SELECT `SCHEMA_NAME` FROM " \
               "information_schema.SCHEMATA WHERE `SCHEMA_NAME`='%s'" % \
               str(name)

        try:
            res = self.get_connection(False).execute(_sql)
        except SQLAlchemyError:
            return False
        else:
            for r in res:
                return True
            return False
        finally:
            self.close_connection()

    def create_database(self, db_name=None, recreate_force=True):
        """创建数据库实例"""
        name = db_name if db_name is not None else self._db_name
        if name is None:
            raise Exception("error missing db name.")

        _sql = "CREATE DATABASE `%s` DEFAULT " \
               "CHARACTER SET utf8 COLLATE utf8_general_ci;" % \
               str(name)

        try:
            if recreate_force:
                try:
                    self.drop_database(name)
                except:
                    pass
            try:
                self.get_connection(False).execute(_sql)  # 3
            except SQLAlchemyError as _exp:
                raise Exception('Create database failure: %s' % str(_exp))
        except:
            self.close_connection()
            raise

    def drop_database(self, db_name=None):
        """删除数据库实例"""
        name = db_name if db_name is not None else self._db_name
        if name is None:
            raise Exception("error missing db name.")

        if name in self.BUILD_IN_DB:
            raise Exception("error cannot drop build-in database.")

        _sql = "DROP DATABASE %s;" % str(name)
        try:
            try:
                self.get_connection(False).execute(_sql)
            except SQLAlchemyError as _exp:
                raise Exception('Drop database failure: %s' % str(_exp))
        except:
            raise
        finally:
            self.close_connection()

    def execute(self, sql):
        """执行SQL"""
        try:
            res = self.get_connection(True).execute(sql)
        except SQLAlchemyError as _exp:
            raise Exception('execute sql failure: %s' % str(_exp))
        else:
            return res

    def __del__(self):
        self.close_connection()


class SQliteDBUtil(object):
    """数据库管理

    功能需求满足：
        创建一个可用的数据库连接
        检查数据库实例是否存在
        创建数据库实例
        删除数据库实例
    """

    SUPPORT_DB_TYPES = ('sqlite', )
    INFORMATION_SCHEMA_DB = 'information_schema'
    BUILD_IN_DB = ('information_schema', 'performance_schema', 'sqlite')

    def __init__(self, db_type='sqlite', db_name="foo.db", debugger=False):
        if db_type not in self.SUPPORT_DB_TYPES:
            raise Exception("db_type is not supported.")

        self._db_type = db_type
        self._db_name = db_name

        self.debugger = debugger
        self._connection = None

    def create_connection(self, include_db=True):
        if self._connection is not None:
            return
        if include_db:
            if self._db_name is None:
                raise Exception("error missing db name.")
            _engine = self._create_engine_with_db()
        else:
            _engine = self._create_engine_without_db()

        self._connection = _engine.connect()

    def close_connection(self):
        if self._connection is None:
            return
        try:
            self._connection.close()
        except:
            pass
        else:
            self._connection = None

    def get_connection(self, include_db=False):
        if self._connection is None:
            self.create_connection(include_db)
        return self._connection

    def _create_engine_with_db(self):
        url = '%s:///%s' % self._db_name

        return create_engine(url,
                             encoding=str("utf-8"), echo=self.debugger)

    def _create_engine_without_db(self):
        url = '%s:///' % (
            self._db_type)

        return create_engine(url,
                             encoding=str("utf-8"), echo=self.debugger)

    def is_exist_database(self, db_name=None):
        name = db_name if db_name is not None else self._db_name
        if name is None:
            raise Exception("error missing db name.")

        _sql = "SELECT `SCHEMA_NAME` FROM " \
               "information_schema.SCHEMATA WHERE `SCHEMA_NAME`='%s'" % \
               str(name)

        try:
            res = self.get_connection(False).execute(_sql)
        except SQLAlchemyError:
            return False
        else:
            for r in res:
                return True
            return False
        finally:
            self.close_connection()

    def create_database(self, db_name=None, recreate_force=True):
        """创建数据库实例"""
        name = db_name if db_name is not None else self._db_name
        if name is None:
            raise Exception("error missing db name.")

        _sql = "CREATE DATABASE `%s` DEFAULT " \
               "CHARACTER SET utf8 COLLATE utf8_general_ci;" % \
               str(name)

        try:
            if recreate_force:
                try:
                    self.drop_database(name)
                except:
                    pass
            try:
                self.get_connection(False).execute(_sql)  # 3
            except SQLAlchemyError as _exp:
                raise Exception('Create database failure: %s' % str(_exp))
        except:
            self.close_connection()
            raise

    def drop_database(self, db_name=None):
        """删除数据库实例"""
        name = db_name if db_name is not None else self._db_name
        if name is None:
            raise Exception("error missing db name.")

        if name in self.BUILD_IN_DB:
            raise Exception("error cannot drop build-in database.")

        _sql = "DROP DATABASE %s;" % str(name)
        try:
            try:
                self.get_connection(False).execute(_sql)
            except SQLAlchemyError as _exp:
                raise Exception('Drop database failure: %s' % str(_exp))
        except:
            raise
        finally:
            self.close_connection()

    def execute(self, sql):
        """执行SQL"""
        try:
            res = self.get_connection(True).execute(sql)
        except SQLAlchemyError as _exp:
            raise Exception('execute sql failure: %s' % str(_exp))
        else:
            return res

    def __del__(self):
        self.close_connection()


if __name__ == "__main__":
    dbm = SQliteDBUtil(db_type='sqlite', db_name='TTT', debugger=False)

    dbm.create_database(True)
    # print(dbm.is_exist_database())
    # dbm.execute("CREATE TABLE `test` (`id` int, PRIMARY KEY (`id`));")
