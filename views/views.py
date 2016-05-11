# -*- coding: utf-8 -*- 
import tornado.web , os , json
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
	obj = [{'name': "父节点1 - 展开",'children': [{'name': "父节点11 - 折叠",'children': [{'name': "叶子节点111"},]},]},]
	data = json.dumps(obj)
	self.write(data)
