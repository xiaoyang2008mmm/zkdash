# -*- coding: utf-8 -*- 
import tornado.web , os , json
import  zookeeper,time
from lib.zk import get_base
from lib.email_auth import Mail
from lib.parserconf import *
import urlparse 
from urllib import urlencode
import functools
class BaseHandler(tornado.web.RequestHandler):
    def prepare(self):
	if not self.request.uri.startswith(self.get_login_url()) and self.current_user is  None:
	    self.redirect(self.get_login_url())
	
    @property
    def zk_Server(self):
	return get_zk_server
    def db(self):
       return self.application.db
    def get_current_user(self):
       return self.get_secure_cookie("user")

class Base_Handler(BaseHandler):
    '''
    base.html获取当前用户
    '''
    def get(self):
	current_user=self.get_current_user()
	self.render("base.html",current_user=current_user)



class Config_Mangager(BaseHandler):
    def get(self):
	self.render("config_mangager.html")

class Get_Base_Node(BaseHandler):
    def get(self):
	self.write(get_base())


class Key_Json(BaseHandler):

    def get_node(self,node_key):
	zk=zookeeper.init(self.zk_Server())
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
	zk=zookeeper.init(self.zk_Server())
	_value = (zookeeper.get(zk,node_id))[0]
	zookeeper.close(zk)
	self.write(_value)
class Mod_Node_Value(BaseHandler):
    def post(self):
	request_dict = self.request.arguments
	node_value = (request_dict['node_value'])[0]
	node_name = (request_dict['node_name'])[0]
	zk=zookeeper.init(self.zk_Server())
	zookeeper.set(zk,node_name,node_value)
	zookeeper.close(zk)
	self.write("修改成功")
class Post_Delete(BaseHandler):
    def post(self):
	request_dict = self.request.arguments
	node_key = (request_dict['node_key'])[0]
	zk=zookeeper.init(self.zk_Server())
	try:
	   zookeeper.delete(zk,node_key)
	   msg = '删除成功'
	except:
	   msg = '无法删除节点'
	finally:
	   zookeeper.close(zk)
	self.write(msg)
class Add_Node(BaseHandler):
    def post(self):
	request_dict = self.request.arguments
	print request_dict
	zk=zookeeper.init(self.zk_Server())
	new_node = (request_dict['New_post_node'])[0]
	new_value = (request_dict['new_node_value'])[0]
	print new_node
	if zookeeper.exists(zk,new_node):
	    zookeeper.close(zk)
	    self.write("此节点存在")
	else:
	    zookeeper.create(zk,new_node,new_value,[{"perms":0x1f,"scheme":"world","id":"anyone"}],0)	
	    zookeeper.close(zk)
	    self.write("增加成功")
class Batch_Delete(BaseHandler):
    def post(self):
	request_dict = self.request.arguments
	node_key = (request_dict['node_key'])[0]
	zk=zookeeper.init(self.zk_Server())


        data = []
        def get_node_tree(node_key):
            if node_key == "/":
                for node in zookeeper.get_children(zk,node_key):
                     key =  "/" + node
                     if (zookeeper.get(zk,key)[1])['numChildren'] > 0:
                          get_node_tree(key)
                          print key
                     else:
                          print key
            else:
                for node in zookeeper.get_children(zk,node_key):
                     key =  node_key + "/" + node
                     if (zookeeper.get(zk,key)[1])['numChildren'] > 0:
                          get_node_tree(key)
                          data.append(key)
                     else:
                          data.append(key)
        
            return data

	get_node_tree(node_key)
	data.append(node_key)

	for items in data:
	    zookeeper.delete(zk,items)
        zookeeper.close(zk)                                                                                                                          
        self.write("删除成功")

class Login_Handler(BaseHandler):
    def get(self):
        self.render('login.html') 
    def post(self):
	name = self.get_argument("login_username").encode("utf-8")
	password = self.get_argument("login_password").encode("utf-8")
        mail = Mail('smtp.exmail.qq.com', name, password)
        auth_result = mail.send()
        if auth_result == "OK":
	   self.set_secure_cookie("user", name.split("@")[0])
    	   self.write("ok")
	else:
    	   self.write("验证失败")

class Logout_Handler(BaseHandler):
    def get(self):
	self.set_secure_cookie("user"," ")
     	self.clear_cookie("user")
     	self.redirect('/login/', permanent=True)
class Zk_Page(BaseHandler):
    def get(self):
	self.render("zk_page.html")
class Snapshot_Page(BaseHandler):
    def get(self):
	self.render("snapshot__page.html")
class M_Snapshot(BaseHandler):
    def post(self):
	request_dict = self.request.arguments
	node_tree = (request_dict['node_tree'])[0]
        zk=zookeeper.init(self.zk_Server())
        _value = (zookeeper.get(zk,node_tree))[0]
	create_time = time.time()
        zookeeper.close(zk)
        print (_value)
	self.write("生成快照成功!!!!!")
