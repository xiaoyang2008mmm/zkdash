import  zookeeper
zk=zookeeper.init('10.46.162.118:2181') 

data = [] 
def get_node(node_key):
    if node_key == "/":
        for node in zookeeper.get_children(zk,node_key):
             key =  "/" + node 
             if (zookeeper.get(zk,key)[1])['numChildren'] > 0:
                  get_node(key)
    	     print key
	     data.append({'name': key})
	     print data
    else:
        for node in zookeeper.get_children(zk,node_key):
             key =  node_key + "/" + node 
             if (zookeeper.get(zk,key)[1])['numChildren'] > 0:
                  get_node(key)
    	     print key

get_node('/')


zookeeper.close(zk)
