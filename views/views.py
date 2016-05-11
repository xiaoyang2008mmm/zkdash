# -*- coding: utf-8 -*- 
import tornado.web , os , json
import  zookeeper

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



class Key_Json(BaseHandler):
    def get(self):
	"""
	obj = [{'name': "父节点1 - 展开",
	    	    'children': [{'name': "父节点11 - 折叠"}]
              }]
	"""
	#obj = [{'name': 'qconf','children': [{'name': "__qconf_register_hosts", 'children': [{'name': "BJ-Gitlab-162-19"}]  }]  }]
	#obj = [{'name': '/qconf', 'children': [{'name': '/qconf/key1', 'children': [{'name': 'key2'}, {'name': 'key3'}]}, {'name': '/qconf/__qconf_register_hosts', 'children': [{'name': 'BJ-Gitlab-162-19'}]}]}]
	data = self.get_node('/live_business')
	print data
	obj = [data]
	data = json.dumps(obj)
	self.write(data)


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
