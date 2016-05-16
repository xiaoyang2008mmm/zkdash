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
	   (r"/add_node/",		Add_Node),
	   (r"/batch_delete/",		Batch_Delete),
	   (r"/login/",			Login_Handler),
	   (r"/logout/", 		Logout_Handler), 
	   (r"/zk_page/", 		Zk_Page), 
	   (r"/snapshot_page/", 	Snapshot_Page), 
	   (r"/m_snapshot/", 		M_Snapshot), 
	   (r"/check_snapshot/", 	Check_Snapshot), 
	]
#HANDLERS +=[(r"/chart/", ChartHandler)]
