from views.views import *
import os.path

STATIC_PATH   = os.path.join(os.path.dirname(__file__), "../static")
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "../templates")
HANDLERS =[
	   (r"/",			Base_Handler),
	   (r"/config_mangager/",	Config_Mangager),
	   (r"/keyjson/",		Key_Json),
	]
#HANDLERS +=[(r"/chart/", ChartHandler)]
