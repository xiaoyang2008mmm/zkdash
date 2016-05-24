#!/usr/bin/env python
# -*- coding: utf-8 -*-

from peewee import Field

from database import Database


import sys

try:
    sys.path.append('../lib')
    sys.path.append('./lib')
    from lib.parserconf import get_mysql_server
except:
    print "导入lib库失败"



try:
    ZKDASH_DB = Database(**get_mysql_server(file="../conf/mysql.conf"))
except:
    ZKDASH_DB = Database(**get_mysql_server(file="./conf/mysql.conf"))


class EnumField(Field):
    """自定义枚举类型字段, peewee中不提供枚举类型
    """
    db_field = 'enum'

    def __init__(self, enum_value=None, *args, **kwargs):
        """枚举初始化
        """
        self.enum_value = enum_value
        super(EnumField, self).__init__(*args, **kwargs)

    def get_modifiers(self):
        """使用传递的枚举值
        """
        return self.enum_value and [self.enum_value] or None
