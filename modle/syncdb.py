# -*- coding: utf-8 -*- 
from peewee import *
import sys

sys.path.append('../lib')

from parserconf import get_mysql_server

database = MySQLDatabase(**get_mysql_server(file="../conf/mysql.conf"))

class UnknownField(object):
    pass

class BaseModel(Model):
    class Meta:
        database = database

class ZdSnapshot(BaseModel):
    #id = IntegerField(primary_key=True, constraints=[SQL("AUTO_INCREMENT")])
    cluster_name = CharField(max_length=64, null=True)
    path = CharField(max_length=512, null=True)
    data = CharField(null=True)
    #create_time = DateTimeField(null=True)

    class Meta(object):

        """表配置信息
        """
        db_table = "zd_snapshot"



if __name__ == "__main__":
    try:
        ZdSnapshot.create_table()    
    except peewee.OperationalError:
        print "ZdSnapshot table already exists!"

