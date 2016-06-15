#coding=utf-8
import  zookeeper
#要修改的地方
zk=zookeeper.init('10.46.162.118:2181')
zk_new=zookeeper.init('10.24.198.220:2181')
key = '/live_business/Store/SpecialUserSlot'
#要修改的地方
 

data = []
def get_node(node_key):
    if node_key == "/":
        for node in zookeeper.get_children(zk,node_key):
             key =  "/" + node
             if (zookeeper.get(zk,key)[1])['numChildren'] > 0:
                  get_node(key)
                  print key 
             else:
                  print key 
    else:
        for node in zookeeper.get_children(zk,node_key):
             key =  node_key + "/" + node
             if (zookeeper.get(zk,key)[1])['numChildren'] > 0:
                  get_node(key)
                  data.append(key)
             else:
                  data.append(key)
        
    return data
 


get_node(key)
data.append(key) 
data.sort() 
 
def sync_zk(data):
    for items in data:
        new_value = (zookeeper.get(zk,items))[0]
    	if not zookeeper.exists(zk_new,items):
    	    zookeeper.create(zk_new,items,new_value,[{"perms":0x1f,"scheme":"world","id":"anyone"}],0)



sync_zk(data)
	
zookeeper.close(zk)
zookeeper.close(zk_new)




