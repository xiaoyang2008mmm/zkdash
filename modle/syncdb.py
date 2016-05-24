# -*- coding: utf-8 -*- 
from peewee import *
from base import ZKDASH_DB


class ZdSnapshot(ZKDASH_DB.Model):
    id = IntegerField(primary_key=True, constraints=[SQL("AUTO_INCREMENT")])
    cluster_name = CharField(max_length=64, null=True)
    path = CharField(max_length=512, null=True)
    data = CharField(null=True)
    create_time = DateTimeField(null=True)

    class Meta(object):

        """表配置信息
        """
        db_table = "zd_snapshot"

class ZdZookeeper(ZKDASH_DB.Model):


    id = IntegerField(primary_key=True, constraints=[SQL("AUTO_INCREMENT")])
    cluster_name = CharField(max_length=128,null=True)
    hosts = CharField(max_length=128,null=True)
    business = CharField(max_length=255,null=True)
    users = CharField(max_length=255,null=True)

    class Meta(object):

        db_table = "zd_zookeeper"




if __name__ == "__main__":
    try:
        ZdSnapshot.create_table()    
    except OperationalError:
        print "ZdSnapshot table already exists!"
    try:
        ZdZookeeper.create_table()    
    except OperationalError:
        print "ZdZookeeper table already exists!"
