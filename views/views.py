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
class Get_Node_Value(BaseHandler):
    def post(self):
	request_dict = self.request.arguments
	node_id = (request_dict['choose_node'])[0]
	zk=zookeeper.init('10.46.162.118:2181')
	_value = (zookeeper.get(zk,node_id))[0]
	zookeeper.close(zk)
	self.write(_value)
class Mod_Node_Value(BaseHandler):
    def post(self):
	request_dict = self.request.arguments
	node_value = (request_dict['node_value'])[0]
	node_name = (request_dict['node_name'])[0]
	zk=zookeeper.init('10.46.162.118:2181')
	zookeeper.set(zk,node_name,node_value)
	zookeeper.close(zk)
	self.write("修改成功")
class Post_Delete(BaseHandler):
    def post(self):
	request_dict = self.request.arguments
	node_key = (request_dict['node_key'])[0]
	print node_key
	zk=zookeeper.init('10.46.162.118:2181')
	zookeeper.delete(zk,node_key)
	zookeeper.close(zk)
	self.write("删除成功")
