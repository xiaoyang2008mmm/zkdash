# -*- coding: utf-8 -*- 
import tornado.web , os , json
import  zookeeper
from lib.zk import get_base

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
       return self.application.db

class Base_Handler(BaseHandler):
    def get(self):
	self.render("base.html")



class Config_Mangager(BaseHandler):
    def get(self):
	self.render("config_mangager.html")

class Get_Base_Node(BaseHandler):
    def get(self):
	self.write(get_base())


class Key_Json(BaseHandler):

    def get_node(self,node_key):
	zk=zookeeper.init('10.46.162.118:2181')
        if node_key == "/":
            for node in zookeeper.get_children(zk,node_key):
                 key =  "/" + node
                 if (zookeeper.get(zk,key)[1])['numChildren'] > 0:
                      self.get_node(key)
        else:
            data=[]
            for node in zookeeper.get_children(zk,node_key):
                 key =  node_key + "/" + node
                 if (zookeeper.get(zk,key)[1])['numChildren'] > 0:
                      data.append(self.get_node(key))
                 else:
                      data.append({'name': node})
    
        node = {'name':node_key}
        node['children'] = data
	zookeeper.close(zk)
    
        return node
class Node_Path(Key_Json):
    def post(self):
	request_dict = self.request.arguments
	node_key = (request_dict['node_path'])[0]
	if  node_key.startswith('/'):
	    try:
                data = self.get_node(node_key)
                obj = [data]
                data = json.dumps(obj)
                self.write(data)
	    except:
                self.write("node不存在")
	else:
            self.write("节点必须以/开头")
