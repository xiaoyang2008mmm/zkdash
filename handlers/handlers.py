from views.views import *
import os.path

STATIC_PATH   = os.path.join(os.path.dirname(__file__), "../static")
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "../templates")
HANDLERS =[
	   (r"/",			Base_Handler),
	   (r"/config_mangager/",	Config_Mangager),
	   (r"/get_base_node/",		Get_Base_Node),
	   (r"/get_node_value/",	Get_Node_Value),
	   (r"/mod_node_value/",	Mod_Node_Value),
	   (r"/post_delete/",		Post_Delete),
	   (r"/node_path/",		Node_Path),
	]
#HANDLERS +=[(r"/chart/", ChartHandler)]
