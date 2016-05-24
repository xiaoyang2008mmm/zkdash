# -*- coding: utf-8 -*-
from peewee import MySQLDatabase
from peewee import OperationalError


class RetryDBMixin(object):

    __slots__ = ()

    def execute_sql(self, sql, params=None, require_commit=True):
        try:
            cursor = super(RetryDBMixin, self).execute_sql(
                sql, params, require_commit)
        except OperationalError:
            if not self.is_closed():
                # 手动关闭连接
                self.close()
            cursor = self.get_cursor()
            cursor.execute(sql, params or ())
            if require_commit and self.get_autocommit():
                self.commit()
        return cursor


class MyRetryDB(RetryDBMixin, MySQLDatabase):
        pass
