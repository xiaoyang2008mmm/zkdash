# -*- coding: utf-8 -*- 
import tornado.httpserver, os 
import tornado.ioloop 
import tornado.web
from handlers.handlers import HANDLERS , STATIC_PATH , TEMPLATE_PATH

from tornado.options import define, options, parse_command_line

define("port", default=88, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
	handlers=HANDLERS
	settings = {                                                        
       	    "static_path": STATIC_PATH ,
     	    "template_path": TEMPLATE_PATH,
     	    "login_url": "/login/",                                                 
            "debug": True,                                                      
     	    "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",                          
	    #"xsrf_cookies":True,                                                  
	}                                                                   
                                                                    

     	tornado.web.Application.__init__(self, handlers, **settings)
	    	

def main():
    parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
