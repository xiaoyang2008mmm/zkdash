from views.views import *
import os.path

STATIC_PATH   = os.path.join(os.path.dirname(__file__), "../static")
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "../templates")
HANDLERS =[
	   (r"/",			Base_Handler),
	   (r"/config_mangager/",	Config_Mangager),
	   (r"/get_base_node/",	Get_Base_Node),
	   (r"/node_path/",		Node_Path),
	]
#HANDLERS +=[(r"/chart/", ChartHandler)]
