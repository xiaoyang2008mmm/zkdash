# -*- coding: utf-8 -*- 
import tornado.web , os
class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
       return self.application.db

class Base_Handler(BaseHandler):
    def get(self):
	self.render("base.html")

