import  zookeeper
zk=zookeeper.init('10.46.162.118:2181') 

def get_node(node_key):
    if node_key == "/":
        for node in zookeeper.get_children(zk,node_key):
             key =  "/" + node 
             if (zookeeper.get(zk,key)[1])['numChildren'] > 0:
                  get_node(key)
    else:
	data=[]
        for node in zookeeper.get_children(zk,node_key):
             key =  node_key + "/" + node 
             if (zookeeper.get(zk,key)[1])['numChildren'] > 0:
	          data.append(get_node(key))
	     else:
	          data.append({'name': node})
		
    node = {'name':node_key} 
    node['children'] = data
    return node

print get_node('/')


zookeeper.close(zk)
