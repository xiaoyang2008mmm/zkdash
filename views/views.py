# -*- coding: utf-8 -*- 
import tornado.web , os , json
import  zookeeper,time
from lib.zk import get_base
from lib.email_auth import Mail
from lib.parserconf import *
import urlparse 
from urllib import urlencode
import functools
from  modle.syncdb import *
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

    def GetNowTime(self):
    	return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
    def zk_connect(self,cluster_name):
	zk_host = (ZdZookeeper.select().where(ZdZookeeper.cluster_name == cluster_name).get()).hosts
	return zk_host

class Base_Handler(BaseHandler):
    '''
    base.html获取当前用户
    '''
    def get(self):
	current_user=self.get_current_user()
	self.render("base.html",current_user=current_user)



class Config_Mangager(BaseHandler):
    def get(self):
	query_result = ZdZookeeper.select()
	_dict = {"all_cluster_name" : query_result}
        self.render("config_mangager.html", **_dict)


class Get_Base_Node(BaseHandler):
    def get(self):
	self.write(get_base())




class Node_Path(BaseHandler):
    def post(self):
	request_dict = self.request.arguments
	node_key = (request_dict['node_path'])[0]
	cluster_name  = (request_dict['cluster_name'])[0]

        zk=zookeeper.init(self.zk_connect(cluster_name))


        def get_node(node_key):
            data=[]
            if node_key == "/":
                for node in zookeeper.get_children(zk,node_key):
                     key =  "/" + node
                     if (zookeeper.get(zk,key)[1])['numChildren'] > 0:
                          data.append(get_node(key))
                          #get_node(key)
                     else:
                          data.append({'name': node})
            else:
                for node in zookeeper.get_children(zk,node_key):
                     key =  node_key + "/" + node
                     if (zookeeper.get(zk,key)[1])['numChildren'] > 0:
                          data.append(get_node(key))
                     else:
                          data.append({'name': node})
        
        
            node_dict = {'name':node_key}
            if not len(data):
                data=['None']
            node_dict['children'] = data
            return node_dict


	if  node_key.startswith('/'):
            data = get_node(node_key)
            obj = [data]
            data = json.dumps(obj)
            self.write(data)
	else:
            self.write("节点必须以/开头")
        zookeeper.close(zk)
class Get_Node_Value(BaseHandler):
    def post(self):
	request_dict = self.request.arguments
	node_id = (request_dict['choose_node'])[0]
        cluster_name  = (request_dict['cluster_name'])[0]
        zk=zookeeper.init(self.zk_connect(cluster_name))
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
    """登录验证"""
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
    """退出"""
    def get(self):
	self.set_secure_cookie("user"," ")
     	self.clear_cookie("user")
     	self.redirect('/login/', permanent=True)
class Zk_Page(BaseHandler):
    def get(self):
	query_result = ZdZookeeper.select()
	_dict = {"all_zk_hosts" : query_result}
        self.render("zk_page.html", **_dict)
class Snapshot_Page(BaseHandler):
    def get(self):
	self.render("snapshot__page.html")
class M_Snapshot(BaseHandler):
    """生成快照"""
    def post(self):
	request_dict = self.request.arguments
	node_tree = (request_dict['node_tree'])[0]
        zk=zookeeper.init(self.zk_Server())
        _value = (zookeeper.get(zk,node_tree))[0]
	create_time = time.time()
	table = ZdSnapshot(cluster_name="test",path=node_tree , data=_value ,create_time = self.GetNowTime())
	table.save()
        zookeeper.close(zk)
        print (_value)
	self.write("生成快照成功!!!!!")
class Check_Snapshot(BaseHandler):
    """查看快照"""
    def get(self,key_node):
	print key_node
	data = []
	all = []
	query = ZdSnapshot.select().where(ZdSnapshot.path == key_node)
	for i in query:
	    data.append(i.id)
	    data.append(i.cluster_name)
	    data.append(i.path)
	    data.append(i.data)
	    data.append(i.create_time)
	    all.append(data)
	    data = []
	print all
	_dict = {"history_snapshot" : all}
	self.render("see_snapshot.html", **_dict)

class Validate_Snapshot(BaseHandler):
    """验证node的快照是否存在"""
    def post(self):
	request_dict = self.request.arguments
	node_tree = (request_dict['node_key'])[0]
	try:
	    ZdSnapshot.get(ZdSnapshot.path == node_tree)
	    self.write("OK")
	except:
	    self.write("ERROR")
		
class Batch_Make_Snapshot(BaseHandler):
    """批量生成快照"""
    def post(self):
	request_dict = self.request.arguments
	node_key = (request_dict['node_tree'])[0]

	self.get_node(node_key)

	self.write("生成快照成功!!!!!")

    def get_node(self,node_key):
	"""获取子节点生成快照存到MySQL"""
        zk=zookeeper.init(self.zk_Server())
        if node_key == "/":
            for node in zookeeper.get_children(zk,node_key):
                 key =  "/" + node
                 if (zookeeper.get(zk,key)[1])['numChildren'] > 0:
                      self.get_node(key)
                 else:
        	      value = (zookeeper.get(zk,key))[0]
		      create_time = time.time()
		      table = ZdSnapshot(cluster_name="test",path=key , data=value ,create_time=self.GetNowTime())
		      table.save()
        else:
            for node in zookeeper.get_children(zk,node_key):
                 key =  node_key + "/" + node
                 if (zookeeper.get(zk,key)[1])['numChildren'] > 0:
                      self.get_node(key)
                 else:
        	      value = (zookeeper.get(zk,key))[0]
		      create_time = time.time()
		      table = ZdSnapshot(cluster_name="test",path=key , data=value ,create_time=self.GetNowTime())
		      table.save()
        zookeeper.close(zk)
    


class Cluster_Operation(BaseHandler):
    """ZK集群主机信息到MySQL数据库"""
    def post(self):
        request_dict = self.request.arguments
        operation = (request_dict['operation'])[0]
	if operation == "cluster_add":
	    cluster_conf = (request_dict['cluster_conf'])[0]
	    cluster_name = (request_dict['cluster_name'])[0]
	    cluster_lable = (request_dict['cluster_lable'])[0] 
	    table = ZdZookeeper(cluster_name=cluster_name ,hosts=cluster_conf , business=cluster_lable)
	    table.save()
	    self.write("保存成功!!!!!")
	if operation == "cluster_delete":
	    c_name = (request_dict['cluster_name'])[0]
	    query = ZdZookeeper.get(ZdZookeeper.cluster_name == c_name ) 
	    query.delete_instance()
	    self.write("删除成功!!!!!")
